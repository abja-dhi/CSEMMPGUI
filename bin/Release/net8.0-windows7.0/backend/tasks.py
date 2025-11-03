import os
import xml.etree.ElementTree as ET
import traceback
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import matplotlib.pyplot as plt
from typing import List
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates

from pyEMMP import ADCP as ADCPDataset
from pyEMMP import OBS as OBSDataset
from pyEMMP import WaterSample as WaterSampleDataset
from pyEMMP import Pd0Decoder, Utils, Constants, PlottingShell, TransectViewer2D, TransectViewer3D, XMLUtils, CRSHelper, DfsuUtils2D, ShapefileLayer, Dfs2_to_Dfsu
from pyEMMP import create_temp_html, plot_hd_vs_adcp_transect, mt_model_transect_comparison, plot_mixed_mt_hd_transect, make_ssc_currents_animation
from pyEMMP import NTU2SSC, BKS2SSC, BKS2NTU, PlotNTU2SSC, PlotBKS2SSC, PlotBKS2SSCTrans, PlotBKS2NTU, PlotBKS2NTUTrans

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

def ViSeaSample2CSV(filepath):
    try:
        df = pd.read_csv(filepath, sep="\s+")
        df["Date"] = pd.to_datetime(df["Date"], origin="1899-12-30", unit="D").dt.strftime("%B %d, %Y %H:%M:%S")
        df.to_csv(filepath.replace(".txt", ".csv"), index=False)
        return {"Results": "Success"}
    except Exception as e:
        return {"Error": str(e)}
    
def Dfs2ToDfsu(in_path, out_path):
    result = Dfs2_to_Dfsu(in_path, out_path, show_qt_progress=True)
    if isinstance(result, str):
        return {"Error": result}
    else:
        return {"Result": "Success"}

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

def NTU2SSCModel(project: ET.Element, sscmodel: ET.Element) -> dict:
    ssc_params = NTU2SSC(project, sscmodel)
    return ssc_params

def PlotNTU2SSCRegression(project: ET.Element, sscmodelid: str, title: str = None):
    result = PlotNTU2SSC(project, sscmodelid, title)
    return result

def BKS2SSCModel(project: ET.Element, sscmodel: ET.Element) -> dict:
    ssc_params = BKS2SSC(project, sscmodel)
    return ssc_params

def PlotBKS2SSCRegression(project: ET.Element, sscmodelid: str, title: str = None):
    result = PlotBKS2SSC(project, sscmodelid, title)
    return result

def PlotBKS2SSCTransect(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask):
    result = PlotBKS2SSCTrans(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask)
    return result

def BKS2NTUModel(project: ET.Element, sscmodel: ET.Element) -> dict:
    ssc_params = BKS2NTU(project, sscmodel)
    return ssc_params

def PlotBKS2NTURegression(project: ET.Element, sscmodelid: str, title: str = None):
    result = PlotBKS2NTU(project, sscmodelid, title)
    return result

def PlotBKS2NTUTransect(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask):
    result = PlotBKS2NTUTrans(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask)
    return result

def PlotPlatformOrientation(project: ET.Element, instrument_id: str, title: str):
    try:
        proj_xml = XMLUtils(project)
        cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=instrument_id, add_ssc=False)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name = cfg['name'])
        adcp.plot.platform_orientation(title=title)
        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": str(e)}

def PlotFourBeamFlood(project: ET.Element, instrument_id: str, field_name: str, xAxisMode: str, yAxisMode: str, cmap: str, vmin: float, vmax: float, title: str, mask: bool):
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
        proj_xml = XMLUtils(project)
        cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=instrument_id, add_ssc=True)
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
            mask = mask,
            x_axis_mode = xAxisMode.lower()
            )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def PlotSingleBeamFlood(project, instrument_id, beam_sel, field_name, xAxisMode, yAxisMode, cmap, vmin, vmax, title, mask):
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
        proj_xml = XMLUtils(project)
        cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=instrument_id, add_ssc=True)
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
            mask = mask,
            x_axis_mode = xAxisMode.lower()
            )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        tb_str = traceback.format_exc()
        return {"Error": tb_str + "\n" + str(e)}

def PlotVelocityFlood(project: ET.Element, instrument_id: str, field_name: str, coord: str, xAxisMode: str, yAxisMode: str, cmap: str, vmin: float, vmax: float, title: str, mask: bool):
    try:
        proj_xml = XMLUtils(project)
        cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name = cfg['name'])

        adcp.plot.velocity_flood_plot(
            field_name = field_name.lower(),
            coord = coord.lower(),
            y_axis_mode = yAxisMode.lower(),
            cmap = cmap,
            vmin = vmin,
            vmax = vmax,
            n_time_ticks = 6,
            title = title, 
            mask = mask,
            x_axis_mode = xAxisMode.lower()
            )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def PlotTransectVelocities(project, instrument_id, bin_sel, scale, title, cmap, vmin, vmax, line_width, line_alpha, hist_bins):
    try:
        proj_xml = XMLUtils(project)
        cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=instrument_id, add_ssc=True)
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

def PlotBeamGeometryAnimation(project, instrument_id, export_gif, gif_path):
    try:
        proj_xml = XMLUtils(project)
        cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name=cfg['name'])
        fig, ani = adcp.plot.beam_geometry_animation(export_gif=export_gif, gif_path=gif_path)
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def PlotTransectAnimation(project, instrument_id, cmap, vmin, vmax, save_gif, gif_path):
    try:
        proj_xml = XMLUtils(project)
        cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=instrument_id, add_ssc=True)
        if 'Error' in cfg.keys():
            return cfg
        adcp = ADCPDataset(cfg, name=cfg['name'])
        fig, ani = adcp.plot.transect_animation(
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            show_pos_trail = True,
            show_beam_trail = True,
            pos_trail_len= 200,
            beam_trail_len = 200,
            interval_ms= 10,
            save_gif = save_gif,
            gif_name=gif_path
        )
        plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        return {"Error": str(e)}

def PlotModelMesh(epsg, filename, title):
    try:
        pass
    except Exception as e:
        return {"Error": str(e)}

def CallMapViewer2D(project: str):
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
        proj_xml = XMLUtils(project)
        settings, map_settings = proj_xml.parse_settings()
        crs_helper = CRSHelper(project_crs=settings["epsg"])
        output_dir = os.path.join(os.environ.get("APPDATA"), "PlumeTrack")
        os.makedirs(output_dir, exist_ok=True)
        name = settings["name"]
        out_fname = os.path.join(output_dir, f"MapViewer2D_{name}.html")
        if len(map_settings["Map2D"]["surveys"]) == 0:
            create_temp_html(out_fname)
        else:      
            adcps = []
            for s in map_settings["Map2D"]["surveys"]:
                surv = proj_xml.find_element(elem_id=s, _type="Survey")
                surv_name = surv.attrib.get("name", s)
                for acfg in proj_xml.get_cfgs_from_survey(surv_name, s, "VesselMountedADCP"):
                    adcps.append(ADCPDataset(acfg, name=acfg['name']))
            cfg = {
                "shp_layers": map_settings["Shapefiles"],
                "cmap": map_settings["Map2D"]["cmap"],
                "field_name": field_name_map[map_settings["Map2D"]["field_name"]],
                "vmin": map_settings["Map2D"]["vmin"],
                "vmax": map_settings["Map2D"]["vmax"],
                "pad_deg": map_settings["Map2D"]["pad_deg"],
                "grid_lines": map_settings["Map2D"]["grid_lines"],
                "grid_opacity": map_settings["Map2D"]["grid_opacity"],
                "grid_color": map_settings["Map2D"]["grid_color"],
                "grid_width": map_settings["Map2D"]["grid_width"],
                "bgcolor": map_settings["Map2D"]["bgcolor"],
                "axis_ticks": map_settings["Map2D"]["axis_ticks"],
                "tick_fontsize": map_settings["Map2D"]["tick_fontsize"],
                "tick_decimals": map_settings["Map2D"]["tick_decimals"],
                "axis_label_fontsize": map_settings["Map2D"]["axis_label_fontsize"],
                "axis_label_color": map_settings["Map2D"]["axis_label_color"],
                "hover_fontsize": map_settings["Map2D"]["hover_fontsize"],
                "transect_line_width": map_settings["Map2D"]["transect_line_width"],
                "vertical_agg": map_settings["Map2D"]["vertical_agg"],
            }
            viewer = TransectViewer2D(adcps=adcps, crs_helper=crs_helper, inputs=cfg)
            fig = viewer.render()
            viewer.save_html(out_fname, auto_open=False)
        return {"Result": out_fname}
    except:
        return {"Error": traceback.format_exc()}

def CallMapViewer3D(project: str):
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
        proj_xml = XMLUtils(project)
        settings, map_settings = proj_xml.parse_settings()
        crs_helper = CRSHelper(project_crs=settings["epsg"])
        output_dir = os.path.join(os.environ.get("APPDATA"), "PlumeTrack")
        os.makedirs(output_dir, exist_ok=True)
        name = settings["name"]
        out_fname = os.path.join(output_dir, f"MapViewer3D_{name}.html")
        if len(map_settings["Map3D"]["surveys"]) == 0:
            create_temp_html(out_fname)
        else:
            adcps = []
            survey_lookup = {}
            for s in map_settings["Map3D"]["surveys"]:
                surv = proj_xml.find_element(elem_id=s, _type="Survey")
                surv_name = surv.attrib.get("name", s)
                surv_id = surv.attrib.get("id", s)
                for acfg in proj_xml.get_cfgs_from_survey(surv_name, s, "VesselMountedADCP"):
                    adcps.append(ADCPDataset(acfg, name=acfg['name']))
                    survey_lookup[acfg['name']] = {"survey": surv_name, "survey_id": surv_id}
            
            cfg = {
                "cmap": map_settings["Map3D"]["cmap"],
                "field_name": field_name_map[map_settings["Map3D"]["field_name"]],
                "vmin": map_settings["Map3D"]["vmin"],
                "vmax": map_settings["Map3D"]["vmax"],
                "pad_deg": map_settings["Map3D"]["pad_deg"],
                "grid_lines": map_settings["Map3D"]["grid_lines"],
                "grid_opacity": map_settings["Map3D"]["grid_opacity"],
                "grid_color": map_settings["Map3D"]["grid_color"],
                "grid_width": map_settings["Map3D"]["grid_width"],
                "bgcolor": map_settings["Map3D"]["bgcolor"],
                "axis_ticks": map_settings["Map3D"]["axis_ticks"],
                "tick_fontsize": map_settings["Map3D"]["tick_fontsize"],
                "tick_decimals": map_settings["Map3D"]["tick_decimals"],
                "axis_label_fontsize": map_settings["Map3D"]["axis_label_fontsize"],
                "axis_label_color": map_settings["Map3D"]["axis_label_color"],
                "hover_fontsize": map_settings["Map3D"]["hover_fontsize"],
                "zscale": map_settings["Map3D"]["z_scale"],
            }
            viewer = TransectViewer3D(adcps=adcps, crs_helper=crs_helper, inputs=cfg, survey_lookup=survey_lookup, shapefile_layers=map_settings["Shapefiles"])
            fig = viewer.render()
            viewer.save_html(out_fname, auto_open=False)

        return {"Result": out_fname}
    except:
        return {"Error": traceback.format_exc()}

def HDComparison(project, model_id, adcp_id,
                 adcp_series_mode, adcp_series_target, adcp_transect_color, adcp_quiver_scale, adcp_quiver_width, adcp_quiver_headwidth, adcp_quiver_headlength, adcp_quiver_color,
                 model_field_pixel_size_m, model_field_quiver_stride_n, model_quiver_scale, model_quiver_width, model_quiver_headwidth, model_quiver_headlength, model_quiver_color, model_quiver_mode, model_levels, model_vmin, model_vmax, model_cmap_name, model_bottom_thresh,
                 cbar_tick_decimals, axis_tick_decimals, pad_m, distance_bin_m, bar_width_scale):
    try:
        proj_xml = XMLUtils(project)
        settings, map_settings = proj_xml.parse_settings()
        crs_helper = CRSHelper(project_crs=settings["epsg"])
        adcp_cfg = proj_xml.get_cfg_by_instrument(instrument_type="VesselMountedADCP", instrument_id=adcp_id, add_ssc=True)
        adcp = ADCPDataset(adcp_cfg, name = adcp_cfg['name'])
        hd_model_element = proj_xml.find_element(elem_id=model_id, _type="HDModel")
        hd_model_path = hd_model_element.find("Path").text
        u_item_number = int(hd_model_element.find("UItemNumber").text)
        v_item_number = int(hd_model_element.find("VItemNumber").text)
        hd_model = DfsuUtils2D(hd_model_path, crs_helper=crs_helper)
        
        fig, axes = plot_hd_vs_adcp_transect(
            hd_model=hd_model,
            adcp=adcp,
            crs_helper=crs_helper,
            u_item_number=u_item_number,
            v_item_number=v_item_number,
            adcp_series_mode=adcp_series_mode,
            adcp_series_target=adcp_series_target,
            adcp_transect_color=adcp_transect_color,
            adcp_quiver_scale=adcp_quiver_scale,
            adcp_quiver_width=adcp_quiver_width,
            adcp_quiver_headwidth=adcp_quiver_headwidth,
            adcp_quiver_headlength=adcp_quiver_headlength,
            adcp_quiver_color=adcp_quiver_color,
            model_field_pixel_size_m=model_field_pixel_size_m,
            model_field_quiver_stride_n=model_field_quiver_stride_n,
            model_quiver_scale=model_quiver_scale,
            model_quiver_width=model_quiver_width,
            model_quiver_headwidth=model_quiver_headwidth,
            model_quiver_headlength=model_quiver_headlength,
            model_quiver_color=model_quiver_color,
            model_quiver_mode=model_quiver_mode,
            model_levels=model_levels,
            model_vmin=model_vmin,
            model_vmax=model_vmax,
            model_cmap_name=model_cmap_name,
            model_bottom_thresh=model_bottom_thresh,
            cbar_tick_decimals=cbar_tick_decimals,
            axis_tick_decimals=axis_tick_decimals,
            pad_m=pad_m,
            distance_bin_m=distance_bin_m,
            bar_width_scale=bar_width_scale,
            shapefile_layers=map_settings["Shapefiles"],
        )

        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": traceback.format_exc() + "\n" + str(e)}

def MTComparison(project, model_id, adcp_id,
                 adcp_series_mode, adcp_series_target, adcp_transect_color,
                 ssc_scale, ssc_levels, ssc_vmin, ssc_vmax, ssc_cmap_name, ssc_bottom_thresh, ssc_pixel_size_m,
                 cbar_tick_decimals, axis_tick_decimals, pad_m, distance_bin_m, bar_width_scale):
    try:
        proj_xml = XMLUtils(project)
        settings, map_settings = proj_xml.parse_settings()
        crs_helper = CRSHelper(project_crs=settings["epsg"])
        adcp_cfg = proj_xml.get_cfg_by_instrument(instrument_type="VesselMountedADCP", instrument_id=adcp_id, add_ssc=True)
        adcp = ADCPDataset(adcp_cfg, name = adcp_cfg['name'])
        mt_model_element = proj_xml.find_element(elem_id=model_id, _type="MTModel")
        mt_model_path = mt_model_element.find("Path").text
        ssc_item_number = int(mt_model_element.find("ItemNumber").text)
        mt_model = DfsuUtils2D(mt_model_path, crs_helper=crs_helper)
        if ssc_scale.lower() == "logarithmic":
            ssc_scale = "log"
        fig, axes = mt_model_transect_comparison(
            mt_model=mt_model,
            adcp=adcp,
            crs_helper=crs_helper,
            ssc_item_number=ssc_item_number,
            adcp_series_mode=adcp_series_mode,
            adcp_series_target=adcp_series_target,
            adcp_transect_color=adcp_transect_color,
            ssc_scale=ssc_scale,
            ssc_levels=ssc_levels,
            ssc_vmin=ssc_vmin,
            ssc_vmax=ssc_vmax,
            ssc_cmap_name=ssc_cmap_name,
            ssc_bottom_thresh=ssc_bottom_thresh,
            ssc_pixel_size_m=ssc_pixel_size_m,
            cbar_tick_decimals=cbar_tick_decimals,
            axis_tick_decimals=axis_tick_decimals,
            pad_m=pad_m,
            distance_bin_m=distance_bin_m,
            bar_width_scale=bar_width_scale,
            shapefile_layers=map_settings["Shapefiles"],
        )

        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": traceback.format_exc() + "\n" + str(e)}

def HDMTComparison(project, hd_model_id, mt_model_id, adcp_id,
                                 adcp_transect_lw, adcp_series_mode, adcp_series_target, adcp_quiver_every_n, adcp_quiver_width, adcp_quiver_headwidth, adcp_quiver_headlength, adcp_quiver_scale,
                                 ssc_scale, ssc_levels, ssc_vmin, ssc_vmax, ssc_cmap_name, ssc_bottom_thresh,
                                 model_field_pixel_size_m, model_field_quiver_stride_n, model_quiver_scale, model_quiver_width, model_quiver_headwidth, model_quiver_headlength, model_quiver_color, model_quiver_mode,
                                 cbar_tick_decimals, axis_tick_decimals, pad_m):
    try:
        proj_xml = XMLUtils(project)
        settings, map_settings = proj_xml.parse_settings()
        crs_helper = CRSHelper(project_crs=settings["epsg"])
        adcp_cfg = proj_xml.get_cfg_by_instrument(instrument_type="VesselMountedADCP", instrument_id=adcp_id, add_ssc=True)
        adcp = ADCPDataset(adcp_cfg, name = adcp_cfg['name'])
        mt_model_element = proj_xml.find_element(elem_id=mt_model_id, _type="MTModel")
        mt_model_path = mt_model_element.find("Path").text
        ssc_item_number = int(mt_model_element.find("ItemNumber").text)
        mt_model = DfsuUtils2D(mt_model_path, crs_helper=crs_helper)
        hd_model_element = proj_xml.find_element(elem_id=hd_model_id, _type="HDModel")
        hd_model_path = hd_model_element.find("Path").text
        u_item_number = int(hd_model_element.find("UItemNumber").text)
        v_item_number = int(hd_model_element.find("VItemNumber").text)
        hd_model = DfsuUtils2D(hd_model_path, crs_helper=crs_helper)
        if ssc_scale.lower() == "logarithmic":
            ssc_scale = "log"
        fig, (ax_map, ax_meta) = plot_mixed_mt_hd_transect(
            hd_model=hd_model,
            mt_model=mt_model,
            adcp=adcp,
            crs_helper=crs_helper,
            u_item_number=u_item_number,
            v_item_number=v_item_number,
            ssc_item_number=ssc_item_number,
            adcp_transect_lw=adcp_transect_lw,
            adcp_series_mode=adcp_series_mode,
            adcp_series_target=adcp_series_target,
            adcp_quiver_every_n=adcp_quiver_every_n,
            adcp_quiver_width=adcp_quiver_width,
            adcp_quiver_headwidth=adcp_quiver_headwidth,
            adcp_quiver_headlength=adcp_quiver_headlength,
            adcp_quiver_scale=adcp_quiver_scale,
            ssc_scale=ssc_scale,
            ssc_levels=ssc_levels,
            ssc_vmin=ssc_vmin,
            ssc_vmax=ssc_vmax,
            ssc_cmap_name=ssc_cmap_name,
            ssc_bottom_thresh=ssc_bottom_thresh,
            model_field_pixel_size_m=model_field_pixel_size_m,
            model_field_quiver_stride_n=model_field_quiver_stride_n,
            model_quiver_scale=model_quiver_scale,
            model_quiver_width=model_quiver_width,
            model_quiver_headwidth=model_quiver_headwidth,
            model_quiver_headlength=model_quiver_headlength,
            model_quiver_color=model_quiver_color,
            model_quiver_mode=model_quiver_mode,
            cbar_tick_decimals=cbar_tick_decimals,
            axis_tick_decimals=axis_tick_decimals,
            pad_m=pad_m,
            shapefile_layers=map_settings["Shapefiles"],
        )

        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": traceback.format_exc() + "\n" + str(e)}
    

def HDMTAnimation(project, hd_model_id, mt_model_id,
                                ssc_scale, ssc_levels, ssc_vmin, ssc_vmax, ssc_cmap_name, ssc_bottom_thresh,
                                model_field_pixel_size_m, model_field_quiver_stride_n, model_quiver_scale, model_quiver_width, model_quiver_headwidth, model_quiver_headlength, model_quiver_color,
                                animation_start_index, animation_end_index, animation_time_step, animation_interval, animation_output_file,
                                cbar_tick_decimals, axis_tick_decimals, bbox_path):
    try:
        proj_xml = XMLUtils(project)
        settings, map_settings = proj_xml.parse_settings()
        crs_helper = CRSHelper(project_crs=settings["epsg"])
        mt_model_element = proj_xml.find_element(elem_id=mt_model_id, _type="MTModel")
        mt_model_path = mt_model_element.find("Path").text
        ssc_item_number = int(mt_model_element.find("ItemNumber").text)
        mt_model = DfsuUtils2D(mt_model_path, crs_helper=crs_helper)
        hd_model_element = proj_xml.find_element(elem_id=hd_model_id, _type="HDModel")
        hd_model_path = hd_model_element.find("Path").text
        u_item_number = int(hd_model_element.find("UItemNumber").text)
        v_item_number = int(hd_model_element.find("VItemNumber").text)
        hd_model = DfsuUtils2D(hd_model_path, crs_helper=crs_helper)
        bbox_layer = ShapefileLayer(path=bbox_path, crs_helper=crs_helper, kind="polygon")
        if ssc_scale.lower() == "logarithmic":
            ssc_scale = "log"
        save_output = True
        if animation_output_file is None:
            save_output = False
        fig, (ax_map, ax_meta) = make_ssc_currents_animation(
            hd_model=hd_model,
            mt_model=mt_model,
            crs_helper=crs_helper,
            u_item_number=u_item_number,
            v_item_number=v_item_number,
            ssc_item_number=ssc_item_number,
            ssc_scale=ssc_scale,
            ssc_levels=ssc_levels,
            ssc_vmin=ssc_vmin,
            ssc_vmax=ssc_vmax,
            ssc_cmap_name=ssc_cmap_name,
            ssc_bottom_thresh=ssc_bottom_thresh,
            model_field_pixel_size_m=model_field_pixel_size_m,
            model_field_quiver_stride_n=model_field_quiver_stride_n,
            model_quiver_scale=model_quiver_scale,
            model_quiver_width=model_quiver_width,
            model_quiver_headwidth=model_quiver_headwidth,
            model_quiver_headlength=model_quiver_headlength,
            model_quiver_color=model_quiver_color,
            animation_time_start_idx=animation_start_index,
            animation_time_end_idx=animation_end_index,
            animation_time_step=animation_time_step,
            animation_interval_ms=animation_interval,
            animation_out_path=animation_output_file,
            cbar_tick_decimals=cbar_tick_decimals,
            axis_tick_decimals=axis_tick_decimals,
            shapefile_layers=map_settings["Shapefiles"],
            bbox_layer=bbox_layer,
            save_output=save_output

        )

        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": traceback.format_exc() + "\n" + str(e)}