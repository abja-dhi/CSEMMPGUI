import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import os
import traceback

from .utils_xml import XMLUtils
from .adcp import ADCP as ADCPDataset
from .utils_crs import CRSHelper
from .mapview2D import TransectViewer2D, create_temp_html
from .utils_dfsu2d import DfsuUtils2D
from .plotting import PlottingShell
from .comparison_hd_mt import plot_mixed_mt_hd_transect
from .obs import OBS as OBSDataset
from .sscmodel import NTU2SSC, BKS2SSC, BKS2NTU, PlotBKS2NTU, PlotBKS2NTUTrans

project = r"C:\Users\abja\AppData\Roaming\PlumeTrack\Clean Project F3 2 Oct 2024.mtproj"


proj_xml = XMLUtils(project)
cfg = proj_xml.get_cfg_by_instrument(instrument_id="12", instrument_type="VesselMountedADCP", add_ssc=True)
adcp = ADCPDataset(cfg, name=cfg['name'])


# ssc_model = proj_xml.find_element(elem_id="29", _type="BKS2NTU")

# ssc_params = BKS2NTU(project, ssc_model)



# result = PlotBKS2NTUTrans(project, sscmodelid="29", beam_sel="1", field_name="SSC", yAxisMode="Bin", cmap="jet", title="", mask="True", vmin=0.1, vmax=2)
quit()





def HDMTComparison(project, hd_model_id, mt_model_id, adcp_id, scale, vmin, vmax, cmap, cmap_bottom_threshold, pixel_size_m, pad_m, colorbar_tick_decimals, axis_tick_decimals, model_quiver_mode, quiver_every_n, quiver_scale, quiver_color_model, transect_line_width, field_pixel_size, field_quiver_stride_n, bin_configuration, bin_target):
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
    fig, (ax_map, ax_meta) = plot_mixed_mt_hd_transect(
        mt_model=mt_model,
        hd_model=hd_model,
        adcp=adcp,
        crs_helper=crs_helper,
        mt_item_number=ssc_item_number,
        u_item_number=u_item_number,
        v_item_number=v_item_number,
        cmap_name=cmap,
        vmin=vmin,
        vmax=vmax,
        cmap_bottom_thresh=cmap_bottom_threshold,
        levels=(0.01, 0.1, 1, 10, 100),
        scale=scale,
        pixel_size_m=pixel_size_m,
        pad_m=pad_m,
        model_quiver_mode=model_quiver_mode,
        quiver_every_n=quiver_every_n,
        quiver_scale=quiver_scale,
        quiver_color_model=quiver_color_model,
        adcp_transect_lw=transect_line_width,
        field_pixel_size_m=field_pixel_size,
        field_quiver_stride_n=field_quiver_stride_n,
        tick_decimals=colorbar_tick_decimals,
        tick_decimal_precision=axis_tick_decimals,
        adcp_series_mode=bin_configuration.lower(),
        adcp_series_target=bin_target,
        shapefile_layers=map_settings["Shapefiles"],
        FIG_W=6.5,
        FIG_H=9.0,
        LEFT=0.06,
        RIGHT=0.90,
        TOP=0.98, 
        BOTTOM=0.00,
        HSPACE=0.22,
        CB_WIDTH=0.012,
        CB_GAP=0.008,
        META_TOP_Y=0.95,
        META_SECTION_GAP=0.20,
        META_LINE_GAP=0.16,
        META_LEFT_OVERSHOOT=0.0,
        META_COL_START=0.02, META_COL_END=0.70, META_COLS=3,
    )
    plt.show()
    return {"Result": "Success"}
    
project = r"C:\Users\abja\AppData\Roaming\PlumeTrack\Clean Project F3 2 Oct 2024.mtproj"

result = HDMTComparison(
    project=project,
    hd_model_id="23",
    mt_model_id="24",
    adcp_id="12",
    scale="log",
    vmin=None,
    vmax=None,
    cmap="jet",
    cmap_bottom_threshold=0.01,
    pixel_size_m=10,
    pad_m=2000,
    colorbar_tick_decimals=2,
    axis_tick_decimals=3,
    model_quiver_mode="field",
    quiver_every_n=20,
    quiver_scale=3,
    quiver_color_model="black",
    transect_line_width=1.8,
    field_pixel_size=100,
    field_quiver_stride_n=3,
    bin_configuration="bin",
    bin_target='mean',
)
plt.show()