
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 13:42:15 2025

@author: anba
"""
import xml.etree.ElementTree as ET
from pathlib import Path  # required by CreateADCPDict
from logging import root
import xml.etree.ElementTree as ET
from adcp import ADCP as ADCPDataset
from typing import List
from obs import OBS as OBSDataset
from watersample import WaterSample as WaterSampleDataset
import numpy as np
import pandas as pd
from pathlib import Path

from utils import Constants
class XMLUtils:
    """Utilities for parsing project XML and building instrument configs."""

    def __init__(self, xml_file: str):
        # parse once; expose root as self.project
        self.tree = ET.parse(xml_file)
        self.project: ET.Element = self.tree.getroot()

    def ParseSSCModel(self, project: ET.Element, sscmodel: ET.Element) -> dict:
        ssc_params = {}
        mode = sscmodel.find("Mode").text
        if mode == "Manual":
            A = float(sscmodel.find("A").text)
            B = float(sscmodel.find("B").text)
            ssc_params['A'] = A
            ssc_params['B'] = B
            return ssc_params
        elif mode == "Auto":
            adcps = []
            obss = []
            watersamples = []
            for inst in sscmodel.findall("Instrument"):
                inst_id = inst.find("ID").text
                inst_type = inst.find("Type").text
                if inst_type == "VesselMountedADCP":
                    cfg = self.CreateADCPDict(project, inst_id, add_ssc=False)
                    print(f"ADCP {cfg['name']} found")
                    adcps.append(ADCPDataset(cfg, name=cfg['name']))
                elif inst_type == "OBSVerticalProfile":
                    cfg = self.CreateOBSDict(project, inst_id)
                    print(f"OBS {cfg['name']} found")
                    obss.append(OBSDataset(cfg))
                elif inst_type == "WaterSample":
                    print("watersamples found")
                    watersamples.append(WaterSampleDataset(self.find_element(project, inst_id, "WaterSample")))

            df_adcp = combine_adcps(adcps)
            df_adcp["depth"] = -df_adcp["depth"]  # Convert to positive down
            df_adcp = df_adcp.sort_values("datetime")
            df_obs = combine_obs(obss)
            df_water = combine_watersamples(watersamples)

            # df_water_obs = nearest_merge_depth_first(df_water, df_obs, on_time="datetime", on_depth="depth", col_name="ntu", time_tolerance="2min", depth_tolerance=2)

            df_water_adcp, df_water = nearest_merge_depth_first(
                df_water, df_adcp, on_time="datetime", on_depth="depth",
                col_name="bks", time_tolerance="2min", depth_tolerance=2
            )
            ssc = df_water["ssc"].to_numpy()
            bks = df_water_adcp["bks"].to_numpy()

            from sklearn.linear_model import LinearRegression
            X = bks.reshape(-1, 1)
            Y = ssc.reshape(-1, 1)
            dt = (df_water_adcp["datetime"] - df_water["datetime"]).dt.total_seconds().abs()
            reg = LinearRegression(fit_intercept=False).fit(X, Y, sample_weight=1/(dt+1))
            B = reg.coef_
            A = reg.intercept_

            ssc_params['A'] = A
            ssc_params['B'] = B
            print(ssc_params)
            return ssc_params

    def CreateADCPDict(self, project: ET.Element, instrument_id: str, add_ssc: bool = True):
        instrument = self.find_element(project, instrument_id, "VesselMountedADCP")
        parent_map = {child: parent for parent in project.iter() for child in parent}
        if instrument is not None:
            parent = parent_map.get(instrument)
            if parent is not None and parent.tag == "Survey":
                water = parent.find("Water")
                sediment = parent.find("Sediment")
        settings = project.find("Settings")
        epsg = settings.find("EPSG").text if settings is not None and settings.find("EPSG") is not None else "4326"
        pd0 = instrument.find("Pd0")
        configuration = pd0.find("Configuration")
        crp_offset = configuration.find("CRPOffset")
        rssis = configuration.find("RSSICoefficients")
        transect_shift = configuration.find("TransectShift")
        masking = pd0.find("Masking")
        maskEchoIntensity = masking.find("MaskEchoIntensity")
        maskPercentGood = masking.find("MaskPercentGood")
        maskCorrelationMagnitude = masking.find("MaskCorrelationMagnitude")
        maskCurrentSpeed = masking.find("MaskCurrentSpeed")
        maskErrorVelocity = masking.find("MaskErrorVelocity")
        maskAbsoluteBackscatter = masking.find("MaskAbsoluteBackscatter")
        position = instrument.find("PositionData")
        columns = position.find("Columns")

        filename = pd0.find("Path").text
        name = instrument.attrib.get("name", Path(filename).stem)
        sscmodelid = pd0.find("SSCModelID").text

        if maskPercentGood.attrib["Enabled"] == "true":
            pg_min = float(self.get_value(maskPercentGood, "Min", 0))
        else:
            pg_min = 0
        if maskCurrentSpeed.attrib["Enabled"] == "true":
            vel_min = float(self.get_value(maskCurrentSpeed, "Min", Constants._LOW_NUMBER))
            vel_max = float(self.get_value(maskCurrentSpeed, "Max", Constants._HIGH_NUMBER))
        else:
            vel_min = Constants._LOW_NUMBER
            vel_max = Constants._HIGH_NUMBER
        if maskEchoIntensity.attrib["Enabled"] == "true":
            echo_min = float(self.get_value(maskEchoIntensity, "Min", 0))
            echo_max = float(self.get_value(maskEchoIntensity, "Max", 255))
        else:
            echo_min = 0
            echo_max = 255
        if maskCorrelationMagnitude.attrib["Enabled"] == "true":
            cormag_min = self.get_value(maskCorrelationMagnitude, "Min", None)
            cormag_min = float(cormag_min) if cormag_min is not None else None
            cormag_max = self.get_value(maskCorrelationMagnitude, "Max", None)
            cormag_max = float(cormag_max) if cormag_max is not None else None
        else:
            cormag_min = None
            cormag_max = None
        if maskAbsoluteBackscatter.attrib["Enabled"] == "true":
            absback_min = float(self.get_value(maskAbsoluteBackscatter, "Min", 0))
            absback_max = float(self.get_value(maskAbsoluteBackscatter, "Max", 255))
        else:
            absback_min = 0
            absback_max = 255
        if maskErrorVelocity.attrib["Enabled"] == "true":
            err_vel_max = self.get_value(maskErrorVelocity, "Max", "auto")
            if err_vel_max != "auto":
                err_vel_max = float(err_vel_max)
        else:
            err_vel_max = "auto"
        start_datetime = self.get_value(masking, "StartDateTime", None)
        end_datetime = self.get_value(masking, "EndDateTime", None)
        first_good_ensemble = self.get_value(masking, "FirstEnsemble", None)
        first_good_ensemble = int(first_good_ensemble) if first_good_ensemble is not None else None
        last_good_ensemble = self.get_value(masking, "LastEnsemble", None)
        last_good_ensemble = int(last_good_ensemble) if last_good_ensemble is not None else None
        magnetic_declination = float(self.get_value(configuration, "MagneticDeclination", 0))
        utc_offset = self.get_value(configuration, "UTCOffset", None)
        utc_offset = float(utc_offset) if utc_offset is not None else None
        crp_rotation_angle = float(self.get_value(configuration, "RotationAngle", 0.0))
        crp_offset_x = float(self.get_value(crp_offset, "X", 0))
        crp_offset_y = float(self.get_value(crp_offset, "Y", 0))
        crp_offset_z = float(self.get_value(crp_offset, "Z", 0))
        transect_shift_x = float(self.get_value(transect_shift, "X", 0))
        transect_shift_y = float(self.get_value(transect_shift, "Y", 0))
        transect_shift_z = float(self.get_value(transect_shift, "Z", 0))
        transect_shift_t = float(self.get_value(transect_shift, "T", 0))

        position_fname = self.get_value(position, "Path", "")
        X_mode = "Variable"
        Y_mode = "Variable"
        Depth_mode = "Constant"
        Pitch_mode = "Constant"
        Roll_mode = "Constant"
        Heading_mode = "Variable"
        DateTime_mode = "Variable"
        X_value = self.get_value(position, "XColumn", "Longitude")
        Y_value = self.get_value(position, "YColumn", "Latitude")
        Depth_value = 0
        Pitch_value = 0
        Roll_value = 0
        Heading_value = self.get_value(position, "HeadingColumn", "Course")
        DateTime_value = self.get_value(position, "DateTimeColumn", "DateTime")
        header = int(self.get_value(position, "Header", 0))
        sep = self.get_value(position, "Sep", ",")

        pos_cfg = {
            'filename': position_fname,
            'epsg': epsg,
            'X_mode': X_mode,
            'Y_mode': Y_mode,
            'Depth_mode': Depth_mode,
            'Pitch_mode': Pitch_mode,
            'Roll_mode': Roll_mode,
            'Heading_mode': Heading_mode,
            'DateTime_mode': DateTime_mode,
            'X_value': X_value,
            'Y_value': Y_value,
            'Depth_value': Depth_value,
            'Pitch_value': Pitch_value,
            'Roll_value': Roll_value,
            'Heading_value': Heading_value,
            'DateTime_value': DateTime_value,
            'header': header,
            'sep': sep,
        }

        water_density = float(water.attrib.get("Density", "1023"))
        salinity = float(water.attrib.get("Salinity", "32"))
        temperature = water.attrib.get("Temperature", None)
        if temperature is not None and temperature.strip() != "":
            temperature = float(temperature)
        pH = float(water.attrib.get("pH", "8.1"))
        water_properties = {
            'density': water_density,
            'salinity': salinity,
            'temperature': temperature,
            'pH': pH
        }

        sediment_density = float(sediment.attrib.get("Density", "2650"))
        diameter = float(sediment.attrib.get("Diameter", "2.5e-4"))
        sediment_properties = {
            'particle_density': sediment_density,
            'particle_diameter': diameter
        }

        C = float(self.get_value(configuration, "C", -139.0))
        P_dbw = float(self.get_value(configuration, "Pdbw", 9))
        E_r = float(self.get_value(rssis, "Er", 39))
        rssi_beam1 = float(self.get_value(rssis, "Beam1", 0.41))
        rssi_beam2 = float(self.get_value(rssis, "Beam2", 0.41))
        rssi_beam3 = float(self.get_value(rssis, "Beam3", 0.41))
        rssi_beam4 = float(self.get_value(rssis, "Beam4", 0.41))

        abs_params = {
            'C': C,
            'P_dbw': P_dbw,
            'E_r': E_r,
            'rssi_beam1': rssi_beam1,
            'rssi_beam2': rssi_beam2,
            'rssi_beam3': rssi_beam3,
            'rssi_beam4': rssi_beam4
        }

        if add_ssc:
            sscmodel = self.find_element(project, sscmodelid, 'SSCModel')
            if sscmodel is not None:
                ssc_params = self.ParseSSCModel(project, sscmodel)
            else:
                ssc_params = {'A': None, 'B': None}
        else:
            ssc_params = {'A': None, 'B': None}

        cfg = {
            'filename': filename,
            'name': name,
            'pg_min': pg_min,
            'vel_min': vel_min,
            'vel_max': vel_max,
            'echo_min': echo_min,
            'echo_max': echo_max,
            'cormag_min': cormag_min,
            'cormag_max': cormag_max,
            'err_vel_max': err_vel_max,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'first_good_ensemble': first_good_ensemble,
            'last_good_ensemble': last_good_ensemble,
            'abs_min': absback_min,
            'abs_max': absback_max,
            'magnetic_declination': magnetic_declination,
            'utc_offset': utc_offset,
            'crp_rotation_angle': crp_rotation_angle,
            'crp_offset_x': crp_offset_x,
            'crp_offset_y': crp_offset_y,
            'crp_offset_z': crp_offset_z,
            'transect_shift_x': transect_shift_x,
            'transect_shift_y': transect_shift_y,
            'transect_shift_z': transect_shift_z,
            'transect_shift_t': transect_shift_t,
            'pos_cfg': pos_cfg,
            'water_properties': water_properties,
            'sediment_properties': sediment_properties,
            'abs_params': abs_params,
            'ssc_params': ssc_params,
        }

        return cfg

    def CreateOBSDict(self, project: ET.Element, instrument_id: str, add_ssc =True):
        instrument = self.find_element(project, instrument_id, "OBSVerticalProfile")
        parent_map = {child: parent for parent in project.iter() for child in parent}
        if instrument is not None:
            parent = parent_map.get(instrument)
            if parent is not None and parent.tag == "Survey":
                water = parent.find("Water")
                sediment = parent.find("Sediment")
                
        obs =  instrument.find("FileInfo")       
        sscmodelid = obs.find("SSCModelID").text       
        if add_ssc:
            sscmodel = self.find_element(project, sscmodelid, 'SSCModel')
            if sscmodel is not None:
                ssc_params = self.ParseSSCModel(project, sscmodel)
            else:
                ssc_params = {'A': None, 'B': None}
        else:
            ssc_params = {'A': None, 'B': None}
            
        settings = project.find("Settings")
        epsg = settings.find("EPSG").text if settings is not None and settings.find("EPSG") is not None else "4326"
        name = instrument.attrib.get("name", "OBSProfile")
        fileinfo = instrument.find("FileInfo")
        filename = fileinfo.find("Path").text
        header = int(fileinfo.find("Header").text)
        sep = fileinfo.find("Sep").text
        date_col = fileinfo.find("DateColumn").text
        time_col = fileinfo.find("TimeColumn").text
        depth_col = fileinfo.find("DepthColumn").text
        ntu_col = fileinfo.find("NTUColumn").text
        masking = instrument.find("Masking")
        maskDateTime = masking.find("MaskDateTime")
        if maskDateTime.attrib["Enabled"] == "true":
            start_datetime = self.get_value(maskDateTime, "Start", Constants._FAR_PAST_DATETIME)
            end_datetime = self.get_value(maskDateTime, "End", Constants._FAR_FUTURE_DATETIME)
        else:
            start_datetime = Constants._FAR_PAST_DATETIME
            end_datetime = Constants._FAR_FUTURE_DATETIME
        maskDepth = masking.find("MaskDepth")
        if maskDepth.attrib["Enabled"] == "true":
            maskDepthMin = self.get_value(maskDepth, "Min", Constants._LOW_NUMBER)
            maskDepthMax = self.get_value(maskDepth, "Max", Constants._HIGH_NUMBER)
        else:
            maskDepthMin = Constants._LOW_NUMBER
            maskDepthMax = Constants._HIGH_NUMBER
        maskNTU = masking.find("MaskNTU")
        if maskNTU.attrib["Enabled"] == "true":
            maskNTUMin = self.get_value(maskNTU, "Min", Constants._LOW_NUMBER)
            maskNTUMax = self.get_value(maskNTU, "Max", Constants._HIGH_NUMBER)
        else:
            maskNTUMin = Constants._LOW_NUMBER
            maskNTUMax = Constants._HIGH_NUMBER

        cfg = {
            'name': name,
            'epsg': epsg,
            'filename': filename,
            'header': header,
            'sep': sep,
            'date_col': date_col,
            'time_col': time_col,
            'depth_col': depth_col,
            'ntu_col': ntu_col,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'depthMin': maskDepthMin,
            'depthMax': maskDepthMax,
            'ntuMin': maskNTUMin,
            'ntuMax': maskNTUMax,
            'ssc_params':ssc_params
        }

        return cfg
    
    def CreateWaterSampleDict(self, project: ET.Element, instrument_id: str) -> dict:
        """Single WaterSample cfg dict with tolerant tag lookup."""
        instrument = self.find_element(project, instrument_id, "WaterSample")
        if instrument is None:
            raise ValueError(f"WaterSample id={instrument_id} not found")
    
        fileinfo = instrument.find("FileInfo") or instrument
    
        def first_text(elem: ET.Element, tags: list[str], default):
            for t in tags:
                v = elem.find(t)
                if v is not None and v.text and v.text.strip():
                    return v.text
            return default
    
        filename = first_text(fileinfo, ["Path", "File", "Filename"], "")
        header = int(first_text(fileinfo, ["Header"], 0))
        sep = first_text(fileinfo, ["Sep", "Delimiter"], ",")
        # columns, try several common names
        datetime_col = first_text(fileinfo, ["DateTimeColumn", "DatetimeColumn"], None)
        date_col = first_text(fileinfo, ["DateColumn"], None)
        time_col = first_text(fileinfo, ["TimeColumn"], None)
        depth_col = first_text(fileinfo, ["DepthColumn", "ZColumn"], None)
        ssc_col = first_text(fileinfo, ["SSCColumn", "TSSColumn", "ConcentrationColumn"], "SSC")
    
        # optional masking
        masking = instrument.find("Masking")
        if masking is not None:
            maskDateTime = masking.find("MaskDateTime")
            if maskDateTime is not None and maskDateTime.attrib.get("Enabled") == "true":
                start_datetime = self.get_value(maskDateTime, "Start", Constants._FAR_PAST_DATETIME)
                end_datetime = self.get_value(maskDateTime, "End", Constants._FAR_FUTURE_DATETIME)
            else:
                start_datetime = Constants._FAR_PAST_DATETIME
                end_datetime = Constants._FAR_FUTURE_DATETIME
    
            maskDepth = masking.find("MaskDepth")
            if maskDepth is not None and maskDepth.attrib.get("Enabled") == "true":
                depth_min = float(self.get_value(maskDepth, "Min", Constants._LOW_NUMBER))
                depth_max = float(self.get_value(maskDepth, "Max", Constants._HIGH_NUMBER))
            else:
                depth_min = Constants._LOW_NUMBER
                depth_max = Constants._HIGH_NUMBER
    
            maskSSC = masking.find("MaskSSC") or masking.find("MaskConcentration")
            if maskSSC is not None and maskSSC.attrib.get("Enabled") == "true":
                ssc_min = float(self.get_value(maskSSC, "Min", Constants._LOW_NUMBER))
                ssc_max = float(self.get_value(maskSSC, "Max", Constants._HIGH_NUMBER))
            else:
                ssc_min = Constants._LOW_NUMBER
                ssc_max = Constants._HIGH_NUMBER
        else:
            start_datetime = Constants._FAR_PAST_DATETIME
            end_datetime = Constants._FAR_FUTURE_DATETIME
            depth_min = Constants._LOW_NUMBER
            depth_max = Constants._HIGH_NUMBER
            ssc_min = Constants._LOW_NUMBER
            ssc_max = Constants._HIGH_NUMBER
    
        cfg = {
            "filename": filename,
            "header": header,
            "sep": sep,
            "datetime_col": datetime_col,
            "date_col": date_col,
            "time_col": time_col,
            "depth_col": depth_col,
            "ssc_col": ssc_col,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "depthMin": depth_min,
            "depthMax": depth_max,
            "sscMin": ssc_min,
            "sscMax": ssc_max,

        }
        return cfg    
    
    def CreateADCPDicts(self, adcp_elements: list[ET.Element], add_ssc: bool = True) -> list[dict]:
        """
        Build config dicts for a list of ADCP elements.
    
        Parameters
        ----------
        adcp_elements : list[ET.Element]
            Elements with type="VesselMountedADCP".
        add_ssc : bool
            If True, include SSC params via ParseSSCModel.
    
        Returns
        -------
        list[dict]
            One cfg dict per input element.
        """
        cfgs: list[dict] = []
        for inst in adcp_elements:
            if inst is None:
                continue
            inst_id = inst.attrib.get("id")
            if not inst_id:
                continue
            cfgs.append(self.CreateADCPDict(self.project, inst_id, add_ssc=add_ssc))
        return cfgs
        
    def CreateOBSDicts(self, obs_elements: list[ET.Element], add_ssc = True) -> list[dict]:
        """Batch: build OBS cfg dicts from OBS elements."""
        cfgs: list[dict] = []
        for inst in obs_elements:
            inst_id = inst.attrib.get("id")
            if inst_id:
                cfgs.append(self.CreateOBSDict(self.project, inst_id, add_ssc = add_ssc))
        return cfgs
    


    def CreateWaterSampleDicts(self, ws_elements: list[ET.Element]) -> list[dict]:
        """Batch: build WaterSample cfg dicts from WaterSample elements."""
        cfgs: list[dict] = []
        for inst in ws_elements:
            inst_id = inst.attrib.get("id")
            if inst_id:
                cfgs.append(self.CreateWaterSampleDict(self.project, inst_id))
        return cfgs

    def get_value(self, element: ET.Element, tag: str, default):
        found = element.find(tag)
        if found is None or found.text is None or found.text.strip() == "":
            return default
        return found.text

    def find_element(self, root: ET.Element, id: str, _type: str) -> ET.Element:
        for el in root.findall(f".//*[@id='{id}']"):
            if el.attrib.get("type") == _type:
                return el
        return None
    
    def find_elements(self, type_name: str | None = None,
                      elem_id: str | None = None,
                      tag: str = "*") -> list[ET.Element]:
        """
        Return elements filtered by @type, @id, and optional tag.
    
        Parameters
        ----------
        type_name : str or None
            Match elements with attribute type==type_name.
        elem_id : str or None
            Match elements with attribute id==elem_id.
        tag : str
            Limit search to this tag name. Use "*" for any tag.
    
        Returns
        -------
        list[xml.etree.ElementTree.Element]
            Matching elements.
        """
        predicates = []
        if type_name:
            predicates.append(f"@type='{type_name}'")
        if elem_id:
            predicates.append(f"@id='{elem_id}'")
        pred = f"[{' and '.join(predicates)}]" if predicates else ""
        return list(self.project.findall(f".//{tag}{pred}"))    
    
    def find_adcps(self) -> list[ET.Element]:
        """All elements with type='VesselMountedADCP'."""
        return self.find_elements(type_name="VesselMountedADCP")
    
    def find_obss(self) -> list[ET.Element]:
        """All elements with type='OBSVerticalProfile'."""
        return self.find_elements(type_name="OBSVerticalProfile")
    
    def find_watersamples(self) -> list[ET.Element]:
        """All elements with type='WaterSample'."""
        return self.find_elements(type_name="WaterSample")
    
    def get_adcp_cfgs(self) ->list:
        adcp_cfgs = self.CreateADCPDicts(adcp_elements = self.find_adcps(), add_ssc = True)
        return adcp_cfgs
    
    def get_obs_cfgs(self) ->list:
        obs_cfgs = self.CreateOBSDicts(obs_elements = self.find_obss())
        return obs_cfgs
        
    def get_ws_cfgs(self) ->list:
        ws_cfgs = self.CreateWaterSampleDicts(ws_elements = self.find_watersamples())
        return ws_cfgs    
    







#%%

# xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
# project = XMLUtils(xml_path)

# adcp_cfgs = project.get_adcp_cfgs()
# obs_cfgs = project.get_obs_cfgs()
# ws_cfgs = project.get_ws_cfgs()
# adcp = ADCPDataset(adcp_cfgs[0],name = '1')

#tree = ET.parse(source=xml_path)








