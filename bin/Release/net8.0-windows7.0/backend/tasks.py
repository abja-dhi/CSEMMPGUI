import xml.etree.ElementTree as ET
import traceback
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import matplotlib.pyplot as plt
from typing import List
from sklearn.linear_model import LinearRegression

# from .project import Project
# from .survey import Survey
# from .model import Model
from .adcp import ADCP as ADCPDataset
from .pd0 import Pd0Decoder
from .utils import Utils, Constants
from .obs import OBS as OBSDataset
from .watersample import WaterSample as WaterSampleDataset


def GenerateOutputXML(xml):
    result = ET.Element("Result")
    for key, value in xml.items():
        ET.SubElement(result, key).text = str(value)
    return ET.tostring(result, encoding='unicode')

def LoadPd0(filepath):
    pd0 = Pd0Decoder(filepath, cfg={})
    pd0.close()
    n_ensembles = pd0._n_ensembles
    return {"NEnsembles": n_ensembles}

def Extern2CSVSingle(filepath):
    result = Utils.extern_to_csv_single(filepath)
    if not result:
        return {"Error": result} # 1: already converted, 0: success, -1: failed
    else:
        return {"Result": "Success"}
    
def Extern2CSVBatch(folderpath):
    result = Utils.extern_to_csv_batch(folderpath)
    n_success = result[0]
    n_failed = result[1]
    n_already_converted = result[2]
    return {"NSuccess": n_success, "NFailed": n_failed, "NAlreadyConverted": n_already_converted}

def Dfs2ToDfsu(filepath):
    result = Utils.dfs2_to_dfsu(filepath)

def ViSeaSample2CSV(filepath):
    try:
        df = pd.read_csv(filepath, sep="\s+")
        df["Date"] = pd.to_datetime(df["Date"], origin="1899-12-30", unit="D").dt.strftime("%B %d, %Y %H:%M:%S")
        df.to_csv(filepath.replace(".txt", ".csv"), index=False)
        return {"Results": "Success"}
    except Exception as e:
        return {"Error": str(e)}

def GetColumnsFromCSV(filepath, header=0, sep=','):
    try:
        if sep == "WhiteSpaces":
            df = pd.read_csv(filepath, header=header, sep="\s+")
        elif sep == "Tab":
            df = pd.read_csv(filepath, header=header, sep="\t")
        else:
            df = pd.read_csv(filepath, header=header, sep=sep, skiprows=header-1)
        columns = df.columns.tolist()
        output = {"NColumns": len(columns)}
        for i, col in enumerate(columns):
            output[f"Column{i}"] = col
        return output
    except:
        return {"NColumns": 0}

def ReadCSV(Root, SubElement, filepath, header, sep, items, columns):
    try:
        if sep == "WhiteSpaces":
            df = pd.read_csv(filepath, header=header, sep="\s+")
        else:
            df = pd.read_csv(filepath, header=header, sep=sep)
        root = ET.Element(Root)
        for i, row in df.iterrows():
            subelement = ET.SubElement(root, SubElement)
            for j, item in enumerate(items):
                if columns[j] == -1:
                    subelement.set(item, "")
                else:
                    subelement.set(item, str(row[columns[j]]))
        result = ET.tostring(root, encoding='unicode')
        return {"Result": result}
    except:
        return {"Error": "An error occurred while reading the CSV file!"}

def PlotPlatformOrientation(project: ET.Element, instrument_id: str, title: str):
    try:
        cfg = CreateADCPDict(project, instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name = cfg['name'])
        adcp.plot.platform_orientation(title=title)
        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": str(e)}

def PlotFourBeamFlood(project: ET.Element, instrument_id: str, field_name: str, yAxisMode: str, cmap: str, vmin: float, vmax: float, title: str, mask: bool):
    field_name_map = {
        "Echo Intensity": "echo_intensity",
        "Correlation Magnitude": "correlation_magnitude",
        "Percent Good": "percent_good",
        "Absolute Backscatter": "absolute_backscatter",
        "Alpha S": "alpha_s",
        "Alpha W": "alpha_w",
        "Signal to Noise Ratio": "signal_to_noise_ratio",
        "SSC": "suspended_solids_concentration",
    }
    try:
        cfg = CreateADCPDict(project, instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name = cfg['name'])

        adcp.plot.four_beam_flood_plot(
            field_name = field_name_map[field_name],
            y_axis_mode = yAxisMode.lower(),
            cmap = cmap,
            vmin = vmin,
            vmax = vmax,
            n_time_ticks = 6,
            title = title, 
            mask = mask
            )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def PlotSingleBeamFlood(project, instrument_id, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask):
    field_name_map = {
        "Velocity": "velocity",
        "Echo Intensity": "echo_intensity",
        "Correlation Magnitude": "correlation_magnitude",
        "Percent Good": "percent_good",
        "Absolute Backscatter": "absolute_backscatter",
        "Alpha S": "alpha_s",
        "Alpha W": "alpha_w",
        "Signal to Noise Ratio": "signal_to_noise_ratio",
        "SSC": "suspended_solids_concentration",
    }
    try:
        cfg = CreateADCPDict(project, instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name = cfg['name'])
        adcp.plot.single_beam_flood_plot(
            beam = beam_sel,
            field_name = field_name_map[field_name],
            y_axis_mode = yAxisMode.lower(),
            cmap = cmap,
            vmin = vmin,
            vmax = vmax,
            n_time_ticks = 6,
            title = title, 
            mask = mask
            )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        tb_str = traceback.format_exc()
        return {"Error": tb_str + "\n" + str(e)}

def PlotTransectVelocities(project, instrument_id, bin_sel, scale, title, cmap, vmin, vmax, line_width, line_alpha, hist_bins):
    try:
        cfg = CreateADCPDict(project, instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name = cfg['name'])
        adcp.plot.transect_velocities(
            bin_sel = bin_sel,
            every_n = 1,
            scale = scale,
            title = title,
            cmap = cmap,
            vmin = vmin,
            vmax = vmax,
            line_width = line_width,
            line_alpha = line_alpha,
            hist_bins = hist_bins
        )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def PlotBeamGeometryAnimation(project, instrument_id):
    try:
        cfg = CreateADCPDict(project, instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name=cfg['name'])
        adcp.plot.beam_geometry_animation()
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def PlotTransectAnimation(project, instrument_id, cmap, vmin, vmax):
    try:
        cfg = CreateADCPDict(project, instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name=cfg['name'])
        adcp.plot.transect_animation(
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            show_pos_trail = True,
            show_beam_trail = True,
            pos_trail_len= 200,
            beam_trail_len = 200,
            interval_ms= 10,
            save_gif = False,
        )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def InstrumentSummaryADCP(filepath):
    """
    Generate a formatted summary report of ADCP instrument configuration and timing.

    Parameters
    ----------
    filepath : str
        Full path to the PD0 binary data file.

    Returns
    -------
    str
        Formatted plain-text summary of key ADCP parameters including timing,
        beam configuration, resolution, hardware metadata, and quality control settings.
    """
    pd0 = Pd0Decoder(filepath, cfg={})
    report = pd0.instrument_summary()
    return {"Config": report}

def PlotModelMesh(epsg, filename, title):
    try:
        pass
    except Exception as e:
        return {"Error": str(e)}

def BKS2SSCModel(project: ET.Element, sscmodel: ET.Element) -> dict:
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
        adcpIDs = []
        watersamples = []
        watersampleIDs = []
        for inst in sscmodel.findall("Instrument"):
            inst_id = inst.find("ID").text
            inst_type = inst.find("Type").text
            if inst_type == "VesselMountedADCP":
                cfg = CreateADCPDict(project, inst_id, add_ssc=False)
                adcps.append(ADCPDataset(cfg, name=cfg['name']))
                adcpIDs.append(inst_id)
            elif inst_type == "WaterSample":
                watersamples.append(WaterSampleDataset(find_element(project, inst_id, "WaterSample")))
                watersampleIDs.append(inst_id)
        if len(watersamples) == 0:
            return {"Error": "No water samples found for SSC calibration"}
        if len(adcps) == 0:
            return {"Error": "No ADCP data found for SSC calibration"}
        df_adcp = combine_adcps(adcps, adcpIDs)
        df_adcp["depth"] = -df_adcp["depth"]  # Convert to positive down
        df_adcp = df_adcp.sort_values("datetime")
        df_water = combine_watersamples(watersamples, watersampleIDs)

        col_name = "bks"
        df_water_inst, df_water, df_data = nearest_merge_depth_first(df_water, df_adcp, on_time="datetime", on_depth="depth", col_name=col_name, time_tolerance="2min", depth_tolerance=2)
        ssc = np.log10(df_data["ssc"].to_numpy())
        if len(df_water_inst) == 0:
            return {"Error": "No valid water samples found for SSC calibration"}
        vals = df_data[col_name].to_numpy()
        
        X = vals.reshape(-1, 1)
        Y = ssc.reshape(-1, 1)
        dt = (df_water_inst["datetime"] - df_water["datetime"]).dt.total_seconds().abs()
        reg = LinearRegression(fit_intercept=True).fit(X, Y, sample_weight=1/(dt+1))  # add 1 to avoid division by zero
        B = reg.coef_[0]
        if isinstance(B, list) or isinstance(B, np.ndarray):
            B = B[0]
        A = reg.intercept_
        if isinstance(A, list) or isinstance(A, np.ndarray):
            A = A[0]
        ssc_params['A'] = A
        ssc_params['B'] = B
        ssc_params['RMSE'] = np.sqrt(np.mean((vals * A + B - ssc) ** 2))
        ssc_params['R2'] = reg.score(X, Y)
        ssc_params["AbsoluteBackscatter"] = vals
        ssc_params["SSC"] = ssc
        pairs = (
        df_water_inst[["id_src", "type_src", "id_tgt", "type_tgt"]]
            .drop_duplicates()
            .to_dict(orient="records")
        )

        # Format nicely: {"WaterSample": 26, "VesselMountedADCP": 13}
        typed_pairs = []
        for p in pairs:
            typed_pairs.append({
                p["type_src"]: p["id_src"],
                p["type_tgt"]: p["id_tgt"]
            })

        ssc_params["Pairs"] = str(typed_pairs)
        return ssc_params

def NTU2SSCModel(project: ET.Element, sscmodel: ET.Element) -> dict:
    ssc_params = {}
    mode = sscmodel.find("Mode").text
    if mode == "Manual":
        A = float(sscmodel.find("A").text)
        B = float(sscmodel.find("B").text)
        ssc_params['A'] = A
        ssc_params['B'] = B
        return ssc_params
    elif mode == "Auto":
        obss = []
        obsIDs = []
        watersamples = []
        watersampleIDs = []
        for inst in sscmodel.findall("Instrument"):
            inst_id = inst.find("ID").text
            inst_type = inst.find("Type").text
            if inst_type == "OBSVerticalProfile":
                cfg = CreateOBSDict(project, inst_id)
                obss.append(OBSDataset(cfg))
                obsIDs.append(inst_id)
            elif inst_type == "WaterSample":
                watersamples.append(WaterSampleDataset(find_element(project, inst_id, "WaterSample")))
                watersampleIDs.append(inst_id)
        if len(watersamples) == 0:
            return {"Error": "No water samples found for SSC calibration"}
        if len(obss) == 0:
            return {"Error": "No OBS data found for SSC calibration"}
        df_obs = combine_obs(obss, obsIDs)
        df_water = combine_watersamples(watersamples, watersampleIDs)

        col_name = "ntu"
        df_water_inst, df_water, df_data = nearest_merge_depth_first(df_water, df_obs, on_time="datetime", on_depth="depth", col_name=col_name, time_tolerance=None, depth_tolerance=None)
        ssc = df_data["ssc"].to_numpy()
        if len(df_water_inst) == 0:
            return {"Error": "No valid water samples found for SSC calibration"}
        vals = df_data[col_name].to_numpy()
        
        X = vals.reshape(-1, 1)
        Y = ssc.reshape(-1, 1)
        dt = (df_water_inst["datetime"] - df_water["datetime"]).dt.total_seconds().abs()
        reg = LinearRegression(fit_intercept=False).fit(X, Y, sample_weight=1/(dt+1))  # add 1 to avoid division by zero
        B = reg.coef_[0]
        if isinstance(B, list) or isinstance(B, np.ndarray):
            B = B[0]
        A = reg.intercept_
        if isinstance(A, list) or isinstance(A, np.ndarray):
            A = A[0]
        ssc_params['A'] = A
        ssc_params['B'] = B
        ssc_params['RMSE'] = np.sqrt(np.mean((vals * A + B - ssc) ** 2))
        ssc_params['R2'] = reg.score(X, Y)
        ssc_params["NTU"] = vals
        ssc_params["SSC"] = ssc
        pairs = (
        df_water_inst[["id_src", "type_src", "id_tgt", "type_tgt"]]
            .drop_duplicates()
            .to_dict(orient="records")
        )

        # Format nicely: {"WaterSample": 26, "VesselMountedADCP": 13}
        typed_pairs = []
        for p in pairs:
            typed_pairs.append({
                p["type_src"]: p["id_src"],
                p["type_tgt"]: p["id_tgt"]
            })

        ssc_params["Pairs"] = str(typed_pairs)
        return ssc_params
   
def CreateADCPDict(project: ET.Element, instrument_id: str, add_ssc: bool=True):
    instrument = find_element(project, instrument_id, "VesselMountedADCP")
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
        pg_min = float(get_value(maskPercentGood, "Min", 0))
    else:
        pg_min = 0
    if maskCurrentSpeed.attrib["Enabled"] == "true":
        vel_min = float(get_value(maskCurrentSpeed, "Min", Constants._LOW_NUMBER))
        vel_max = float(get_value(maskCurrentSpeed, "Max", Constants._HIGH_NUMBER))
    else:
        vel_min = Constants._LOW_NUMBER
        vel_max = Constants._HIGH_NUMBER
    if maskEchoIntensity.attrib["Enabled"] == "true":
        echo_min = float(get_value(maskEchoIntensity, "Min", 0))
        echo_max = float(get_value(maskEchoIntensity, "Max", 255))
    else:
        echo_min = 0
        echo_max = 255
    if maskCorrelationMagnitude.attrib["Enabled"] == "true":
        cormag_min = get_value(maskCorrelationMagnitude, "Min", None)
        cormag_min = float(cormag_min) if cormag_min is not None else None
        cormag_max = get_value(maskCorrelationMagnitude, "Max", None)
        cormag_max = float(cormag_max) if cormag_max is not None else None
    else:
        cormag_min = None
        cormag_max = None
    if maskAbsoluteBackscatter.attrib["Enabled"] == "true":
        absback_min = float(get_value(maskAbsoluteBackscatter, "Min", 0))
        absback_max = float(get_value(maskAbsoluteBackscatter, "Max", 255))
    else:
        absback_min = 0
        absback_max = 255
    if maskErrorVelocity.attrib["Enabled"] == "true":
        err_vel_max = get_value(maskErrorVelocity, "Max", "auto")
        if err_vel_max != "auto":
            err_vel_max = float(err_vel_max)
    else:
        err_vel_max = "auto"
    # velocity_average_window_len = get_value(masking, "VelocityAverageWindowLen", 0)
    start_datetime = get_value(masking, "StartDateTime", None)
    end_datetime = get_value(masking, "EndDateTime", None)
    first_good_ensemble = get_value(masking, "FirstEnsemble", None)
    first_good_ensemble = int(first_good_ensemble) if first_good_ensemble is not None else None
    last_good_ensemble = get_value(masking, "LastEnsemble", None)
    last_good_ensemble = int(last_good_ensemble) if last_good_ensemble is not None else None
    magnetic_declination = float(get_value(configuration, "MagneticDeclination", 0))
    utc_offset = get_value(configuration, "UTCOffset", None)
    utc_offset = float(utc_offset) if utc_offset is not None else None
    # beam_dr = float(get_value(configuration, "beam_dr", 0.1))
    # bt_bin_offset = int(get_value(configuration, "BTBinOffset", 1))
    crp_rotation_angle = float(get_value(configuration, "RotationAngle", 0.0))
    crp_offset_x = float(get_value(crp_offset, "X", 0))
    crp_offset_y = float(get_value(crp_offset, "Y", 0))
    crp_offset_z = float(get_value(crp_offset, "Z", 0))
    transect_shift_x = float(get_value(transect_shift, "X", 0))
    transect_shift_y = float(get_value(transect_shift, "Y", 0))
    transect_shift_z = float(get_value(transect_shift, "Z", 0))
    transect_shift_t = float(get_value(transect_shift, "T", 0))

    position_fname = get_value(position, "Path", "")
    X_mode = "Variable"
    Y_mode = "Variable"
    Depth_mode = "Constant"
    Pitch_mode = "Constant"
    Roll_mode = "Constant"
    Heading_mode = "Variable"
    DateTime_mode = "Variable"
    X_value = get_value(position, "XColumn", "Longitude")
    Y_value = get_value(position, "YColumn", "Latitude")
    Depth_value = 0
    Pitch_value = 0
    Roll_value = 0
    Heading_value = get_value(position, "HeadingColumn", "Course")
    DateTime_value = get_value(position, "DateTimeColumn", "DateTime")
    header = int(get_value(position, "Header", 0))
    sep = get_value(position, "Sep", ",")

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
        'density' : water_density,
        'salinity' : salinity,
        'temperature' : temperature,
        'pH' : pH
        }

    sediment_density = float(sediment.attrib.get("Density", "2650"))
    diameter = float(sediment.attrib.get("Diameter", "2.5e-4"))
    sediment_properties = {
        'particle_density': sediment_density,
        'particle_diameter': diameter
    }

    C = float(get_value(configuration, "C", -139.0))
    P_dbw = float(get_value(configuration, "Pdbw", 9))
    E_r = float(get_value(rssis, "Er", 39))
    rssi_beam1 = float(get_value(rssis, "Beam1", 0.41))
    rssi_beam2 = float(get_value(rssis, "Beam2", 0.41))
    rssi_beam3 = float(get_value(rssis, "Beam3", 0.41))
    rssi_beam4 = float(get_value(rssis, "Beam4", 0.41))

    abs_params = {'C': C,
              'P_dbw': P_dbw,
              'E_r': E_r,
              'rssi_beam1': rssi_beam1,
              'rssi_beam2': rssi_beam2,
              'rssi_beam3': rssi_beam3,
              'rssi_beam4': rssi_beam4}

    if add_ssc:
        sscmodel = find_element(project, sscmodelid, 'BKS2SSC')
        if sscmodel is not None:
            A = float(get_value(sscmodel, "A", 3.5))
            B = float(get_value(sscmodel, "B", 0.049))
            ssc_params = {'A': A, 'B': B}
        else:
            ssc_params = {'A': 3.5, 'B':.049}
    else:
        ssc_params = {'A': 3.5, 'B': 0.049}

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
        'abs_min' : absback_min,
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
        'sediment_properties':sediment_properties,
        'abs_params': abs_params,
        'ssc_params': ssc_params,
    }

    return cfg

def CreateOBSDict(project: ET.Element, instrument_id: str, add_ssc: bool=True):
    instrument = find_element(project, instrument_id, "OBSVerticalProfile")
    parent_map = {child: parent for parent in project.iter() for child in parent}
    if instrument is not None:
        parent = parent_map.get(instrument)
        if parent is not None and parent.tag == "Survey":
            water = parent.find("Water")
            sediment = parent.find("Sediment")
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
    sscmodelid = fileinfo.find("SSCModelID").text
    if add_ssc:
        sscmodel = find_element(project, sscmodelid, 'NTU2SSC')
        if sscmodel is not None:
            A = float(get_value(sscmodel, "A", 3.5))
            B = float(get_value(sscmodel, "B", 0.049))
            ssc_params = {'A': A, 'B': B}
        else:
            ssc_params = {'A': 3.5, 'B':.049}
    else:
        ssc_params = {'A': 3.5, 'B': 0.049}

    masking = instrument.find("Masking")
    maskDateTime = masking.find("MaskDateTime")
    if maskDateTime.attrib["Enabled"] == "true":
        start_datetime = get_value(maskDateTime, "Start", Constants._FAR_PAST_DATETIME)
        end_datetime = get_value(maskDateTime, "End", Constants._FAR_FUTURE_DATETIME)
    else:
        start_datetime = Constants._FAR_PAST_DATETIME
        end_datetime = Constants._FAR_FUTURE_DATETIME
    maskDepth = masking.find("MaskDepth")
    if maskDepth.attrib["Enabled"] == "true":
        maskDepthMin = get_value(maskDepth, "Min", Constants._LOW_NUMBER)
        maskDepthMax = get_value(maskDepth, "Max", Constants._HIGH_NUMBER)
    else:
        maskDepthMin = Constants._LOW_NUMBER
        maskDepthMax = Constants._HIGH_NUMBER
    maskNTU = masking.find("MaskNTU")
    if maskNTU.attrib["Enabled"] == "true":
        maskNTUMin = get_value(maskNTU, "Min", Constants._LOW_NUMBER)
        maskNTUMax = get_value(maskNTU, "Max", Constants._HIGH_NUMBER)
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
        'ssc_params': ssc_params,
        'start_datetime': start_datetime,
        'end_datetime': end_datetime,
        'depthMin': maskDepthMin,
        'depthMax': maskDepthMax,
        'ntuMin': maskNTUMin,
        'ntuMax': maskNTUMax
    }

    return cfg

def CreateWaterSampleDict(project: ET.Element, instrument_id: str):
    instrument = find_element(project, instrument_id, "WaterSample")
    parent_map = {child: parent for parent in project.iter() for child in parent}
    if instrument is not None:
        parent = parent_map.get(instrument)
        if parent is not None and parent.tag == "Survey":
            water = parent.find("Water")
            sediment = parent.find("Sediment")
    settings = project.find("Settings")
    epsg = settings.find("EPSG").text if settings is not None and settings.find("EPSG") is not None else "4326"
    name = instrument.attrib.get("name", "WaterSample")

def get_value(element: ET.Element, tag: str, default) -> str:
    found = element.find(tag)
    if found is None or found.text is None or found.text.strip() == "":
        return default
    return found.text

def find_element(root: ET.Element, id: str, _type: str) -> ET.Element:
    for el in root.findall(f".//*[@id='{id}']"):
        if el.attrib.get("type") == _type:
            return el
    return None

def combine_adcps(adcp_list: List[ADCPDataset], adcp_ids: List[str]):
    dfs = []
    for i, adcp in enumerate(adcp_list):
        datetimes = adcp.time.ensemble_datetimes
        abs_bks = adcp.get_beam_data(field_name="absolute_backscatter", mask=True)
        depths = adcp.geometry.geographic_beam_midpoint_positions.z
        abs_bks = np.nanmean(abs_bks, axis=2)  # average across beams (n_ensembels, n_bins, n_beams) -> (n_ensembles * n_bins * n_beams)
        depths = np.nanmean(depths, axis=2)  # average across beams
        datetimes = np.repeat(datetimes[:, None], abs_bks.shape[1], axis=1)
        df = pd.DataFrame({
            "datetime": datetimes.ravel(),
            "depth": depths.ravel(),
            "bks": abs_bks.ravel(),
            "id": adcp_ids[i],
            "type": "VesselMountedADCP"
        })
        dfs.append(df)
    output = pd.concat(dfs, ignore_index=True)
    output = output.dropna(subset=["bks"])
    return output

def combine_obs(obs_list: List[OBSDataset], obs_ids: List[str]):
    dfs = []
    for i, obs in enumerate(obs_list):
        df = pd.DataFrame({
            "datetime": obs.data.datetime,
            "depth": obs.data.depth,
            "ntu": obs.data.ntu,
            "id": obs_ids[i],
            "type": "OBSVerticalProfile"
        })
        dfs.append(df)
    output = pd.concat(dfs, ignore_index=True)
    output = output.dropna(subset=["ntu"])
    return output

def combine_watersamples(water_list: List[WaterSampleDataset], water_ids: List[str]):
    dfs = []
    for i, water in enumerate(water_list):
        df = pd.DataFrame({
            "datetime": water.data.datetime,
            "depth": water.data.depth,
            "ssc": water.data.ssc,
            "id": water_ids[i],
            "type": "WaterSample"
        })
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def nearest_merge_depth_first(
    source, target,
    on_time="datetime", on_depth="depth", col_name="value",
    time_tolerance=None, depth_tolerance=None
):
    """
    For each row in source, find the closest row in target.
    Priority:
      1. Minimize depth difference
      2. If tie, minimize datetime difference

    Parameters
    ----------
    source : DataFrame
        The dataframe driving the matching.
    target : DataFrame
        The dataframe to match against.
    on_time : str
        Column name for datetime.
    on_depth : str
        Column name for depth.
    col_name : str
        Column name of target value to bring back.
    time_tolerance : str or pd.Timedelta, optional
        Maximum allowed datetime difference (e.g. "5min").
    depth_tolerance : float, optional
        Maximum allowed depth difference (same units as depth).
    """
    # Cross join
    merged = source.assign(key=1).merge(
        target.assign(key=1), on="key", suffixes=("_src", "_tgt")
    ).drop(columns="key")

    # Differences
    merged["depth_diff"] = (merged[f"{on_depth}_src"] - merged[f"{on_depth}_tgt"]).abs()
    merged["time_diff"] = (merged[f"{on_time}_src"] - merged[f"{on_time}_tgt"]).abs().dt.total_seconds()

    # Apply tolerances
    if depth_tolerance is not None:
        merged = merged[merged["depth_diff"] <= depth_tolerance]
    if time_tolerance is not None:
        tol = pd.Timedelta(time_tolerance).total_seconds()
        merged = merged[merged["time_diff"] <= tol]

    if merged.empty:
        return (
            pd.DataFrame(columns=[on_time, on_depth, col_name]),
            pd.DataFrame(columns=source.columns),
            pd.DataFrame(columns=[col_name, "ssc"])
        )

    # Sort by depth first, then time
    merged = merged.sort_values(["depth_diff", "time_diff"])

    # Pick best match per source row
    nearest = (
        merged.groupby([f"{on_time}_src", f"{on_depth}_src"]).first().reset_index()
    )
    
    out = nearest[[f"{on_time}_tgt", f"{on_depth}_tgt", col_name, "id_tgt", "type_tgt", "id_src", "type_src"]].rename(
        columns={f"{on_time}_tgt": on_time, f"{on_depth}_tgt": on_depth}
    )

    # Source subset (only rows that matched)
    matched_src = source.merge(
        nearest[[f"{on_time}_src", f"{on_depth}_src"]],
        left_on=[on_time, on_depth],
        right_on=[f"{on_time}_src", f"{on_depth}_src"],
        how="inner"
    ).drop(columns=[f"{on_time}_src", f"{on_depth}_src"])

    # Third output: pair col_name (e.g. bks) with ssc
    pairs = pd.DataFrame({
        col_name: out[col_name].to_numpy(),
        "ssc": matched_src["ssc"].to_numpy()
    })

    return out, matched_src, pairs

