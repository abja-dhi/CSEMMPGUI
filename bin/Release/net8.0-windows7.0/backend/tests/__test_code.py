from pyEMMP.utils_xml import XMLUtils
from pyEMMP import ADCP as ADCPDataset
from pyEMMP import *
import matplotlib.pyplot as plt
import traceback

def PlotSingleBeamFlood(project, instrument_id, beam_sel, field_name, xAxisMode, yAxisMode, cmap, vmin, vmax, title, mask, background_ssc):
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
        cfg["background_ssc"] = background_ssc
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
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        tb_str = traceback.format_exc()
        return {"Error": tb_str + "\n" + str(e)}



project = r"C:\Users\abja\AppData\Roaming\PlumeTrack\Test Project 1.mtproj"
adcp_id = "4"
project_xml = XMLUtils(project)

result = PlotSingleBeamFlood(project=project, instrument_id=adcp_id, field_name="SSC", beam_sel="mean", xAxisMode="time", yAxisMode="depth", cmap="turbo", vmin=None, vmax=None, title="10", mask=True, background_ssc=10.0)
result = PlotSingleBeamFlood(project=project, instrument_id=adcp_id, field_name="SSC", beam_sel="mean", xAxisMode="time", yAxisMode="depth", cmap="turbo", vmin=None, vmax=None, title="0", mask=True, background_ssc=0)
result = PlotSingleBeamFlood(project=project, instrument_id=adcp_id, field_name="SSC", beam_sel="mean", xAxisMode="time", yAxisMode="depth", cmap="turbo", vmin=None, vmax=None, title="50th percentile", mask=True, background_ssc=-1)
plt.show()