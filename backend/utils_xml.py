# -*- coding: utf-8 -*-
"""
XMLUtils — optimized to avoid passing `project` around.
- Caches Settings/EPSG and a parent map.
- All finders use self.project.
- ParseSSCModel/Create*Dict methods use internal helpers.
External deps expected: ADCPDataset, OBSDataset, WaterSampleDataset,
combine_adcps, combine_obs, combine_watersamples, nearest_merge_depth_first,
sklearn, numpy, pandas, utils.Constants, PlottingShell (if plotting used elsewhere).
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

from adcp import ADCP as ADCPDataset
from obs import OBS as OBSDataset
from watersample import WaterSample as WaterSampleDataset
from utils import Constants


class XMLUtils:
    """Utilities for parsing project XML and building instrument configs."""

    def __init__(self, xml_file: str):
        # Parse once
        self.tree = ET.parse(xml_file)
        self.project: ET.Element = self.tree.getroot()
        # Cached lookups
        self._settings = self.project.find("Settings")
        self._epsg = (
            self._settings.find("EPSG").text
            if self._settings is not None and self._settings.find("EPSG") is not None
            else "4326"
        )
        self._parent_map: Optional[dict[ET.Element, ET.Element]] = None

    # ----------------------
    # Helpers
    # ----------------------
    def _get_parent_map(self) -> dict[ET.Element, ET.Element]:
        if self._parent_map is None:
            self._parent_map = {child: parent for parent in self.project.iter() for child in parent}
        return self._parent_map

    def _get_survey_context(self, instrument: ET.Element):
        parent = self._get_parent_map().get(instrument)
        if parent is not None and parent.tag == "Survey":
            return parent.find("Water"), parent.find("Sediment")
        return None, None

    def get_value(self, element: ET.Element | None, tag: str, default):
        """Safe tag text getter with default."""
        if element is None:
            return default
        found = element.find(tag)
        if found is None or found.text is None or found.text.strip() == "":
            return default
        return found.text

    # Finders use self.project
    def find_element(self, id: str, _type: str, root: ET.Element | None = None) -> ET.Element | None:
        root = self.project if root is None else root
        for el in root.findall(f".//*[@id='{id}']"):
            if el.attrib.get("type") == _type:
                return el
        return None

    def find_elements(self, type_name: str | None = None, elem_id: str | None = None, tag: str = "*") -> list[ET.Element]:
        predicates = []
        if type_name:
            predicates.append(f"@type='{type_name}'")
        if elem_id:
            predicates.append(f"@id='{elem_id}'")
        pred = f"[{ ' and '.join(predicates) }]" if predicates else ""
        return list(self.project.findall(f".//{tag}{pred}"))

    def find_adcps(self) -> list[ET.Element]:
        return self.find_elements(type_name="VesselMountedADCP")

    def find_obss(self) -> list[ET.Element]:
        return self.find_elements(type_name="OBSVerticalProfile")

    def find_watersamples(self) -> list[ET.Element]:
        return self.find_elements(type_name="WaterSample")
    # ----------------------
    # Survey-scoped cfg getters
    # ----------------------
    def _find_surveys(self) -> list[ET.Element]:
        node = self.project.find("Surveys")
        if node is not None:
            sv = list(node.findall("Survey"))
            if sv:
                return sv
        sv = list(self.project.findall("./Survey"))
        return sv if sv else list(self.project.findall(".//Survey"))

    def _resolve_survey(self, survey_key: int | str | ET.Element) -> ET.Element | None:
        if isinstance(survey_key, ET.Element):
            return survey_key
        surveys = self._find_surveys()
        if isinstance(survey_key, int):
            return surveys[survey_key - 1] if 1 <= survey_key <= len(surveys) else None
        for s in surveys:
            if s.attrib.get("id") == survey_key:
                return s
        for s in surveys:
            if s.attrib.get("name") == survey_key:
                return s
        return None

    def _find_under(self, root: ET.Element, type_name: str) -> list[ET.Element]:
        return list(root.findall(f".//*[@type='{type_name}']"))

    def get_survey_adcp_cfgs(self, survey_key, add_ssc: bool = True) -> list[dict]:
        s = self._resolve_survey(survey_key)
        if s is None:
            return []
        elements = self._find_under(s, "VesselMountedADCP")
        return self.CreateADCPDicts(elements, add_ssc=add_ssc)

    def get_survey_obs_cfgs(self, survey_key, add_ssc: bool = True) -> list[dict]:
        s = self._resolve_survey(survey_key)
        if s is None:
            return []
        elements = self._find_under(s, "OBSVerticalProfile")
        return self.CreateOBSDicts(elements, add_ssc=add_ssc)

    def get_survey_ws_cfgs(self, survey_key) -> list[dict]:
        s = self._resolve_survey(survey_key)
        if s is None:
            return []
        elements = self._find_under(s, "WaterSample")
        return self.CreateWaterSampleDicts(elements)
        if s is None:
            return []
        return list(s.iter()) if deep else list(s)

    # ----------------------
    # SSC Model
    # ----------------------
    def ParseSSCModel(self, sscmodel: ET.Element, _type: str) -> dict:
        ssc_params: dict = {}
        mode_el = sscmodel.find("Mode")
        mode = mode_el.text if mode_el is not None else "Manual"
        if mode == "Manual":
            A = float(sscmodel.find("A").text)
            B = float(sscmodel.find("B").text)
            ssc_params["A"] = A
            ssc_params["B"] = B
            return ssc_params

        # Auto mode
        adcps: list = []
        adcpIDs: list[str] = []
        obss: list = []
        obsIDs: list[str] = []
        watersamples: list = []
        watersampleIDs: list[str] = []

        for inst in sscmodel.findall("Instrument"):
            inst_id = inst.find("ID").text
            inst_type = inst.find("Type").text
            if inst_type == "VesselMountedADCP":
                cfg = self.CreateADCPDict(inst_id, add_ssc=False)
                adcps.append(ADCPDataset(cfg, name=cfg["name"]))
                adcpIDs.append(inst_id)
            elif inst_type == "OBSVerticalProfile":
                cfg = self.CreateOBSDict(inst_id, add_ssc=False)
                obss.append(OBSDataset(cfg))
                obsIDs.append(inst_id)
            elif inst_type == "WaterSample":
                watersamples.append(WaterSampleDataset(self.find_element(inst_id, "WaterSample")))
                watersampleIDs.append(inst_id)

        if len(watersamples) == 0:
            return {"Error": "No water samples found for SSC calibration"}
        if len(adcps) == 0 and _type == "VesselMountedADCP":
            return {"Error": "No ADCP data found for SSC calibration"}
        if len(obss) == 0 and _type == "OBSVerticalProfile":
            return {"Error": "No OBS data found for SSC calibration"}

        # External combiners
        df_adcp = combine_adcps(adcps, adcpIDs)
        df_adcp["depth"] = -df_adcp["depth"]  # positive down
        df_adcp = df_adcp.sort_values("datetime")
        df_obs = combine_obs(obss, obsIDs)
        df_water = combine_watersamples(watersamples, watersampleIDs)

        if _type == "VesselMountedADCP":
            col_name = "bks"
            df_water_inst, df_water = nearest_merge_depth_first(
                df_water, df_adcp,
                on_time="datetime", on_depth="depth", col_name=col_name,
                time_tolerance="2min", depth_tolerance=2,
            )
            ssc = np.log10(df_water["ssc"].to_numpy())
            intercept = True
        else:
            col_name = "ntu"
            df_water_inst, df_water = nearest_merge_depth_first(
                df_water, df_obs,
                on_time="datetime", on_depth="depth", col_name=col_name,
                time_tolerance="2min", depth_tolerance=2,
            )
            ssc = df_water["ssc"].to_numpy()
            intercept = False

        if len(df_water_inst) == 0:
            return {"Error": "No valid water samples found for SSC calibration"}

        from sklearn.linear_model import LinearRegression

        vals = df_water_inst[col_name].to_numpy()
        X = vals.reshape(-1, 1)
        Y = ssc.reshape(-1, 1)
        dt = (df_water_inst["datetime"] - df_water["datetime"]).dt.total_seconds().abs()
        reg = LinearRegression(fit_intercept=intercept).fit(X, Y, sample_weight=1 / (dt + 1))
        B = reg.coef_[0]
        A = reg.intercept_

        # Preserve user's existing RMSE/R2 conventions
        ssc_params["A"] = A
        ssc_params["B"] = B
        ssc_params["RMSE"] = float(np.sqrt(np.mean((vals * A + B - ssc) ** 2)))
        ssc_params["R2"] = float(reg.score(X, Y))
        mapper = {"bks": "Absolute Backscatter", "ntu": "NTU"}
        ssc_params[mapper[col_name]] = vals
        ssc_params["SSC"] = ssc

        pairs = (
            df_water_inst[["id_src", "type_src", "id_tgt", "type_tgt"]]
            .drop_duplicates()
            .to_dict(orient="records")
        )
        typed_pairs = [{p["type_src"]: p["id_src"], p["type_tgt"]: p["id_tgt"]} for p in pairs]
        ssc_params["Pairs"] = typed_pairs
        return ssc_params

    # ----------------------
    # ADCP
    # ----------------------
    def CreateADCPDict(self, instrument_id: str, add_ssc: bool = True):
        instrument = self.find_element(instrument_id, "VesselMountedADCP")
        if instrument is None:
            raise ValueError(f"VesselMountedADCP id={instrument_id} not found")

        water, sediment = self._get_survey_context(instrument)
        epsg = self._epsg

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
        # columns = position.find("Columns")  # unused

        filename = pd0.find("Path").text
        name = instrument.attrib.get("name", Path(filename).stem)
        sscmodelid_el = pd0.find("SSCModelID")
        sscmodelid = sscmodelid_el.text if sscmodelid_el is not None else None

        pg_min = float(self.get_value(maskPercentGood, "Min", 0)) if maskPercentGood.attrib.get("Enabled") == "true" else 0
        if maskCurrentSpeed.attrib.get("Enabled") == "true":
            vel_min = float(self.get_value(maskCurrentSpeed, "Min", Constants._LOW_NUMBER))
            vel_max = float(self.get_value(maskCurrentSpeed, "Max", Constants._HIGH_NUMBER))
        else:
            vel_min = Constants._LOW_NUMBER
            vel_max = Constants._HIGH_NUMBER
        if maskEchoIntensity.attrib.get("Enabled") == "true":
            echo_min = float(self.get_value(maskEchoIntensity, "Min", 0))
            echo_max = float(self.get_value(maskEchoIntensity, "Max", 255))
        else:
            echo_min = 0
            echo_max = 255
        if maskCorrelationMagnitude.attrib.get("Enabled") == "true":
            cormag_min = self.get_value(maskCorrelationMagnitude, "Min", None)
            cormag_min = float(cormag_min) if cormag_min is not None else None
            cormag_max = self.get_value(maskCorrelationMagnitude, "Max", None)
            cormag_max = float(cormag_max) if cormag_max is not None else None
        else:
            cormag_min = None
            cormag_max = None
        if maskAbsoluteBackscatter.attrib.get("Enabled") == "true":
            absback_min = float(self.get_value(maskAbsoluteBackscatter, "Min", 0))
            absback_max = float(self.get_value(maskAbsoluteBackscatter, "Max", 255))
        else:
            absback_min = 0
            absback_max = 255
        if maskErrorVelocity.attrib.get("Enabled") == "true":
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
        X_value = self.get_value(position, "XColumn", "Longitude")
        Y_value = self.get_value(position, "YColumn", "Latitude")
        Heading_value = self.get_value(position, "HeadingColumn", "Course")
        DateTime_value = self.get_value(position, "DateTimeColumn", "DateTime")
        header = int(self.get_value(position, "Header", 0))
        sep = self.get_value(position, "Sep", ",")

        pos_cfg = {
            "filename": position_fname,
            "epsg": self._epsg,
            "X_mode": "Variable",
            "Y_mode": "Variable",
            "Depth_mode": "Constant",
            "Pitch_mode": "Constant",
            "Roll_mode": "Constant",
            "Heading_mode": "Variable",
            "DateTime_mode": "Variable",
            "X_value": X_value,
            "Y_value": Y_value,
            "Depth_value": 0,
            "Pitch_value": 0,
            "Roll_value": 0,
            "Heading_value": Heading_value,
            "DateTime_value": DateTime_value,
            "header": header,
            "sep": sep,
        }

        # Water/Sediment properties (nil-safe)
        water_density = float((water or ET.Element("Water", {})).attrib.get("Density", "1023"))
        salinity = float((water or ET.Element("Water", {})).attrib.get("Salinity", "32"))
        temperature = (water or ET.Element("Water", {})).attrib.get("Temperature", None)
        if temperature is not None and str(temperature).strip() != "":
            temperature = float(temperature)
        pH = float((water or ET.Element("Water", {})).attrib.get("pH", "8.1"))
        water_properties = {"density": water_density, "salinity": salinity, "temperature": temperature, "pH": pH}

        sediment_density = float((sediment or ET.Element("Sediment", {})).attrib.get("Density", "2650"))
        diameter = float((sediment or ET.Element("Sediment", {})).attrib.get("Diameter", "2.5e-4"))
        sediment_properties = {"particle_density": sediment_density, "particle_diameter": diameter}

        C = float(self.get_value(configuration, "C", -139.0))
        P_dbw = float(self.get_value(configuration, "Pdbw", 9))
        E_r = float(self.get_value(rssis, "Er", 39))
        rssi_beam1 = float(self.get_value(rssis, "Beam1", 0.41))
        rssi_beam2 = float(self.get_value(rssis, "Beam2", 0.41))
        rssi_beam3 = float(self.get_value(rssis, "Beam3", 0.41))
        rssi_beam4 = float(self.get_value(rssis, "Beam4", 0.41))
        abs_params = {"C": C, "P_dbw": P_dbw, "E_r": E_r, "rssi_beam1": rssi_beam1, "rssi_beam2": rssi_beam2, "rssi_beam3": rssi_beam3, "rssi_beam4": rssi_beam4}

        if add_ssc and sscmodelid:
            sscmodel = self.find_element(sscmodelid, "SSCModel")
            ssc_params = self.ParseSSCModel(sscmodel, _type="VesselMountedADCP") if sscmodel is not None else {"A": None, "B": None}
        else:
            ssc_params = {"A": None, "B": None}

        cfg = {
            "filename": filename,
            "name": name,
            "pg_min": pg_min,
            "vel_min": vel_min,
            "vel_max": vel_max,
            "echo_min": echo_min,
            "echo_max": echo_max,
            "cormag_min": cormag_min,
            "cormag_max": cormag_max,
            "err_vel_max": err_vel_max,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "first_good_ensemble": first_good_ensemble,
            "last_good_ensemble": last_good_ensemble,
            "abs_min": absback_min,
            "abs_max": absback_max,
            "magnetic_declination": magnetic_declination,
            "utc_offset": utc_offset,
            "crp_rotation_angle": crp_rotation_angle,
            "crp_offset_x": crp_offset_x,
            "crp_offset_y": crp_offset_y,
            "crp_offset_z": crp_offset_z,
            "transect_shift_x": transect_shift_x,
            "transect_shift_y": transect_shift_y,
            "transect_shift_z": transect_shift_z,
            "transect_shift_t": transect_shift_t,
            "pos_cfg": pos_cfg,
            "water_properties": water_properties,
            "sediment_properties": sediment_properties,
            "abs_params": abs_params,
            "ssc_params": ssc_params,
        }
        return cfg

    # ----------------------
    # OBS
    # ----------------------
    def CreateOBSDict(self, instrument_id: str, add_ssc: bool = True):
        instrument = self.find_element(instrument_id, "OBSVerticalProfile")
        if instrument is None:
            raise ValueError(f"OBSVerticalProfile id={instrument_id} not found")

        water, sediment = self._get_survey_context(instrument)
        epsg = self._epsg

        fileinfo = instrument.find("FileInfo")
        name = instrument.attrib.get("name", "OBSProfile")
        filename = fileinfo.find("Path").text
        header = int(fileinfo.find("Header").text)
        sep = fileinfo.find("Sep").text
        date_col = fileinfo.find("DateColumn").text
        time_col = fileinfo.find("TimeColumn").text
        depth_col = fileinfo.find("DepthColumn").text
        ntu_col = fileinfo.find("NTUColumn").text

        masking = instrument.find("Masking")
        maskDateTime = masking.find("MaskDateTime")
        if maskDateTime.attrib.get("Enabled") == "true":
            start_datetime = self.get_value(maskDateTime, "Start", Constants._FAR_PAST_DATETIME)
            end_datetime = self.get_value(maskDateTime, "End", Constants._FAR_FUTURE_DATETIME)
        else:
            start_datetime = Constants._FAR_PAST_DATETIME
            end_datetime = Constants._FAR_FUTURE_DATETIME
        maskDepth = masking.find("MaskDepth")
        if maskDepth.attrib.get("Enabled") == "true":
            maskDepthMin = self.get_value(maskDepth, "Min", Constants._LOW_NUMBER)
            maskDepthMax = self.get_value(maskDepth, "Max", Constants._HIGH_NUMBER)
        else:
            maskDepthMin = Constants._LOW_NUMBER
            maskDepthMax = Constants._HIGH_NUMBER
        maskNTU = masking.find("MaskNTU")
        if maskNTU.attrib.get("Enabled") == "true":
            maskNTUMin = self.get_value(maskNTU, "Min", Constants._LOW_NUMBER)
            maskNTUMax = self.get_value(maskNTU, "Max", Constants._HIGH_NUMBER)
        else:
            maskNTUMin = Constants._LOW_NUMBER
            maskNTUMax = Constants._HIGH_NUMBER

        # optional SSC model id could be under FileInfo or elsewhere; tolerate absence
        sscmodelid_el = fileinfo.find("SSCModelID")
        ssc_params = {"A": None, "B": None}
        if add_ssc and sscmodelid_el is not None and sscmodelid_el.text:
            sscmodel = self.find_element(sscmodelid_el.text, "SSCModel")
            if sscmodel is not None:
                ssc_params = self.ParseSSCModel(sscmodel, _type="OBSVerticalProfile")

        cfg = {
            "name": name,
            "epsg": epsg,
            "filename": filename,
            "header": header,
            "sep": sep,
            "date_col": date_col,
            "time_col": time_col,
            "depth_col": depth_col,
            "ntu_col": ntu_col,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "depthMin": maskDepthMin,
            "depthMax": maskDepthMax,
            "ntuMin": maskNTUMin,
            "ntuMax": maskNTUMax,
            "ssc_params": ssc_params,
        }
        return cfg

    # ----------------------
    # Water Samples
    # ----------------------
    def CreateWaterSampleDict(self, instrument_id: str) -> dict:
        instrument = self.find_element(instrument_id, "WaterSample")
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
        datetime_col = first_text(fileinfo, ["DateTimeColumn", "DatetimeColumn"], None)
        date_col = first_text(fileinfo, ["DateColumn"], None)
        time_col = first_text(fileinfo, ["TimeColumn"], None)
        depth_col = first_text(fileinfo, ["DepthColumn", "ZColumn"], None)
        ssc_col = first_text(fileinfo, ["SSCColumn", "TSSColumn", "ConcentrationColumn"], "SSC")
    
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
    
        # Inline <Sample/> parsing → nested dict
        records = []
        for s in instrument.findall("Sample"):
            dt = pd.to_datetime(s.attrib.get("DateTime"), errors="coerce")
            try:
                depth_val = float(s.attrib.get("Depth")) if s.attrib.get("Depth") is not None else None
            except ValueError:
                depth_val = None
            try:
                ssc_val = float(s.attrib.get("SSC")) if s.attrib.get("SSC") is not None else None
            except ValueError:
                ssc_val = None
            records.append({
                "sample": s.attrib.get("Sample"),
                "datetime": dt,
                "depth": depth_val,
                "ssc": ssc_val,
                "notes": s.attrib.get("Notes", ""),
            })
    
        if records:
            # sort by time, keep NaT at end
            records.sort(key=lambda r: (pd.isna(r["datetime"]), r["datetime"] if not pd.isna(r["datetime"]) else pd.Timestamp.max))
    
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
            "samples": {
                "records": records,                 # list of dicts as parsed above
                "count": len(records),
                "units": {"depth": "m", "ssc": "mg/L"},
                "source": "inline" if records else "file",
            },
        }
        return cfg


    # ----------------------
    # Batch builders
    # ----------------------
    def CreateADCPDicts(self, adcp_elements: list[ET.Element], add_ssc: bool = True) -> list[dict]:
        cfgs: list[dict] = []
        for inst in adcp_elements:
            if inst is None:
                continue
            inst_id = inst.attrib.get("id")
            if not inst_id:
                continue
            cfgs.append(self.CreateADCPDict(inst_id, add_ssc=add_ssc))
        return cfgs

    def CreateOBSDicts(self, obs_elements: list[ET.Element], add_ssc: bool = True) -> list[dict]:
        cfgs: list[dict] = []
        for inst in obs_elements:
            inst_id = inst.attrib.get("id")
            if inst_id:
                cfgs.append(self.CreateOBSDict(inst_id, add_ssc=add_ssc))
        return cfgs

    def CreateWaterSampleDicts(self, ws_elements: list[ET.Element]) -> list[dict]:
        cfgs: list[dict] = []
        for inst in ws_elements:
            inst_id = inst.attrib.get("id")
            if inst_id:
                cfgs.append(self.CreateWaterSampleDict(inst_id))
        return cfgs

    # ----------------------
    # Public getters
    # ----------------------
    def get_adcp_cfgs(self) -> list[dict]:
        return self.CreateADCPDicts(adcp_elements=self.find_adcps(), add_ssc=True)

    def get_obs_cfgs(self) -> list[dict]:
        return self.CreateOBSDicts(obs_elements=self.find_obss(), add_ssc=True)

    def get_ws_cfgs(self) -> list[dict]:
        return self.CreateWaterSampleDicts(ws_elements=self.find_watersamples())



#%%

# xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
# project = XMLUtils(xml_path)

# adcp_cfgs = project.get_adcp_cfgs()
# obs_cfgs = project.get_obs_cfgs()
# ws_cfgs = project.get_ws_cfgs()
# adcp = ADCPDataset(adcp_cfgs[0],name = '1')

#tree = ET.parse(source=xml_path)




# adcp_cfgs = project.get_survey_adcp_cfgs("Survey 1")
# obs_cfgs = project.get_survey_obs_cfgs("Survey 1")
# ws_cfgs  = project.get_survey_ws_cfgs("Survey 1")





