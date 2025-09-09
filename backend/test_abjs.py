
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

# from .project import Project
# from .survey import Survey
# from .model import Model
from adcp import ADCP as ADCPDataset
from pd0 import Pd0Decoder
from utils import Utils, Constants
from obs import OBS as OBSDataset
from watersample import WaterSample as WaterSampleDataset
from plotting import PlottingShell
from transect_viewer_2d import TransectViewer2D
from transect_viewer_3d import TransectViewer3D


def create_temp_html(out_fname: str):
    content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Survey Viewer</title>
  <style>
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: white;
    }
    .message {
      font-size: 20px;
      color: black;
    }
  </style>
</head>
<body>
  <div class="message">Select surveys in the Map Settings to activate the viewer</div>
</body>
</html>"""
    with open(out_fname, "w") as f:
        f.write(content)

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

def CallMapViewer2D(settings: ET.Element, mapSettings: ET.Element):
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
    directory = settings.find("Directory").text
    name = settings.find("Name").text
    xml_path = os.path.join(directory, f"{name}.mtproj")
    map2D = mapSettings.find("Map2D")
    surveys = map2D.find("Surveys")
    output_dir = os.path.join(os.environ.get("APPDATA"), "PlumeTrack")
    os.makedirs(output_dir, exist_ok=True)
    out_fname = os.path.join(output_dir, "MapViewer2D.html")
    if surveys.text is None:
        create_temp_html(out_fname)
    else:
        surveys_list = surveys.findall("Survey")
        survey_names = [s.text for s in surveys_list if s.text is not None]
        shp = []    #TODO
        cmap = get_value(map2D, "ColorMap", "jet")
        field_name = field_name_map[get_value(map2D, "FieldName", "Absolute Backscatter")]
        vmin = get_value(map2D, "vmin", None)
        vmax = get_value(map2D, "vmax", None)
        pad_deg = get_value(map2D, "Padding", 0.03)
        grid_lines = get_value(map2D, "NGridLines", 10)
        grid_opacity = get_value(map2D, "GridOpacity", 0.2)
        grid_color = get_value(map2D, "GridColor", "#000000")
        grid_width = get_value(map2D, "GridWidth", 1)
        bgcolor = get_value(map2D, "BackgroundColor", "#FFFFFF")
        axis_ticks = get_value(map2D, "NAxisTicks", 5)
        tick_fontsize = get_value(map2D, "TickFontSize", 10)
        tick_decimals = get_value(map2D, "TickNDecimals", 2)
        axis_label_fontsize = get_value(map2D, "AxisLabelFontSize", 12)
        axis_label_color = get_value(map2D, "AxisLabelColor", "#000000")
        hover_fontsize = get_value(map2D, "HoverFontSize", 10)
        transect_line_width = get_value(map2D, "TransectLineWidth", 2)
        bin_method = get_value(map2D, "VerticalAggBinItem", "bin").lower()
        bin_value = str(get_value(map2D, "VerticalAggBinTarget", 1)).lower()
        beam_value = str(get_value(map2D, "VerticalAggBeam", "Mean")).lower()
        if bin_value != "mean":
            bin_value = float(bin_value)
        if beam_value != "mean":
            beam_value = int(beam_value)
        vertical_agg = {
            "method": bin_method,
            "target": bin_value,
            "beam": beam_value
        }
        cfg = {
            "xml": xml_path,
            "surveys": survey_names,
            "shp": shp,
            "cmap": cmap,
            "field_name": field_name,
            "vmin": vmin,
            "vmax": vmax,
            "pad_deg": pad_deg,
            "grid_lines": grid_lines,
            "grid_opacity": grid_opacity,
            "grid_color": grid_color,
            "grid_width": grid_width,
            "bgcolor": bgcolor,
            "axis_ticks": axis_ticks,
            "tick_fontsize": tick_fontsize,
            "tick_decimals": tick_decimals,
            "axis_label_fontsize": axis_label_fontsize,
            "axis_label_color": axis_label_color,
            "hover_fontsize": hover_fontsize,
            "transect_line_width": transect_line_width,
            "vertical_agg": vertical_agg,
            "out_fname": out_fname
        }
        viewer = TransectViewer2D(cfg)
        fig = viewer.render()
        viewer.save_html(auto_open=False)
    return {"Result": out_fname}
    
    

project = ET.parse(r"C:\Users\abja\AppData\Roaming\PlumeTrack\Clean Project F3 2 Oct 2024.mtproj").getroot()
settings = find_element(project, "1", "Settings")
mapSettings = find_element(project, "2", "MapSettings")
results = CallMapViewer2D(settings, mapSettings)
print(results)