# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 12:17:25 2025

@author: anba
"""
import pathlib
root = pathlib.Path(r".")  
total = 0
for path in root.rglob('*.py'):
    total += sum(1 for _ in open(path, 'r', encoding='utf-8'))


#%%
import sys,os
# Class with params on the PLOT method, not on __init__.
# Simple continuous lines. No helpers called across methods.

import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from utils_dfsu2D import DfsuUtils2D
from utils_xml import XMLUtils
from adcp import ADCP as ADCPDataset

from plotting import PlottingShell
# # %% load from project file

# xml_path = r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj"
# survey_name = "Survey 1"



#model_fpath = r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Model Files/MT20241002.dfsu"
model_fpath = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/test3.dfsu'
mt_model = DfsuUtils2D(model_fpath)  # provides extract_transect_idw(...)





# project = XMLUtils(xml_path)
# adcp_cfgs = project.get_survey_adcp_cfgs(survey_name)

# # Provide SSC calibration defaults if your ADCP class expects them.
# ssc_params = {"A": 3, "B": 0.049}
# for cfg in adcp_cfgs:
#     cfg["ssc_params"] = ssc_params
#     cfg['velocity_average_window_len'] = 3
# adcps = [ADCPDataset(cfg, name=cfg.get("name")) for cfg in adcp_cfgs]




#%%

#%% get a bunch of examaple data 


#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2024_survey_data\10. Oct\20241024_F3(E)'
#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\Surveys\2025_CESS_survey_data\5. Jul\20250709_CESS_CETUS'

#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\Surveys\2024_survey_data\10. Oct\20241002_F3(E)'
root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\Surveys\F3\2024\10. Oct\20241002_F3(E)'

#Utils.extern_to_csv_batch(r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2025_CESS_survey_data\5. Jul')

pd0_fpaths = []
pos_fpaths = []
for dirpath, _, filenames in os.walk(root):
    if 'RawDataRT' not in dirpath:
        continue
    for fname in filenames:
        fpath = os.path.join(dirpath, fname)
        if fname.endswith('r.000'):
            pd0_fpaths.append(fpath)
        elif fname.endswith('extern.csv'):
            pos_fpaths.append(fpath)
            

#% Load a dataset

i = 6 # indicator variable for dataset selection

water_properties =  {'density':1023,
                     'salinity': 32,
                     'temperature':None,
                     'pH': 8.1}

sediment_properties = {'particle_diameter':2.5e-4,
                       'particle_density':2650}


abs_params = {'C': -139.0,
              'P_dbw': 9,
              'E_r': 39,
              'rssi_beam1': 0.41,
              'rssi_beam2': 0.41,
              'rssi_beam3': 0.41,
              'rssi_beam4': 0.41,}

ssc_params = {'A': 3.5, 'B':.049}

adcps = []
for i in range(len(pos_fpaths)):
    pos_cfg = {'filename':pos_fpaths[i],
           'epsg':'4326',
           'X_mode': 'Variable',
           'Y_mode': 'Variable',
           'Depth_mode': 'Constant',
           'Pitch_mode': 'Constant',
           'Roll_mode':'Cosntant',
           'Heading_mode': 'Variable',
           'DateTime_mode': 'Variable',
           'X_value': 'Longitude',
           'Y_value': 'Latitude',
           'Depth_value': 0,
           'Pitch_value': 0,
           'Roll_value': 0,
           'Heading_value': 'Course',
           'DateTime_value': 'DateTime',
           }
    
    
    cfg = {'filename':pd0_fpaths[i],
        'name':fpath.split(os.sep)[-1].split('.000')[0],
        'pg_min' : 90,
        'vel_min' : -2.0,
        'vel_max' : 2.0,
        'echo_min' : 0,
        'echo_max' : 255,
        'cormag_min' : None,
        'cormag_max' : 255,
        'abs_min' : -100,
        'abs_max': 0,
        'err_vel_max' : 'auto',
        'velocity_average_window_len': 3,
        'start_datetime' : None,
        'end_datetime' : None,
        'first_good_ensemble' : None,
        'last_good_ensemble' : None,
        'magnetic_declination' : 0,
        'utc_offset' : None,
        'beam_dr': 0.1,
        'bt_bin_offset': 1,
        'crp_rotation_angle' : 0,
        'crp_offset_x' : 0,
        'crp_offset_y' : -3,
        'crp_offset_z' : 0,
        'transect_shift_x': 0.0,
        'transect_shift_y': 0.0,
        'transect_shift_z': 0.0,
        'transect_shift_t': 0.0,
        'pos_cfg':pos_cfg,
        'water_properties': water_properties,
        'sediment_properties':sediment_properties,
        'abs_params': abs_params,
        'ssc_params': ssc_params,
        }
     
    try:
        adcp = ADCPDataset(cfg, name = cfg['name'])
        adcps.append(adcp)
    except: None
    

#%%
model_item_num =1
t = np.asarray(pd.to_datetime(adcp.time.ensemble_datetimes).to_pydatetime())
xq = np.asarray(adcp.position.x)
yq = np.asarray(adcp.position.y)

Xq, Yq = mt_model._to_mesh_xy(xq, yq, adcp.position.epsg)
cx, cy = mt_model._centroids[:, 0], mt_model._centroids[:, 1]
fig,ax = PlottingShell.subplots()
ax.scatter(cx,cy, s = 0.1)
ax.plot(Xq,Yq, c = 'red', lw = 10)
ax.set_aspect('equal')


# vals = mt_model.extract_transect_idw(xq=xq,
#                                      yq=yq,
#                                      t=t, 
#                                      item_number=model_item_num,
#                                      input_crs = adcp.position.epsg,
#                                      )


#%%

#%%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

def timeseries_MT_comparison(
        adcps,
        mt_model,
        model_item_num,
        y_agg_mode="bin",
        target=5,
        beam="mean",
        figheight=3,
        figwidth=9,
        smooth_obs=False,
        smooth_window=5):
    """
    Time-series comparison with a right-side metadata panel (never clipped).
    Lines: lw=0.8, alpha=0.9. Legend fontsize=8. Metadata fontsize=8.
    """

    # Validate beam
    if not ((isinstance(beam, str) and beam.lower() == "mean") or isinstance(beam, (int, np.integer))):
        raise TypeError("beam must be 'mean' or a single integer.")

    # Figure with dedicated metadata column
    fig = plt.figure(figsize=(figwidth, figheight), constrained_layout=True)
    
    #fig,ax = PlottingShell.subplots(ncol = 2, width_ratios=[3.2, 1.0])
    gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[3.2, 1.0])
    ax = fig.add_subplot(gs[0, 0])
    

    meta_ax = fig.add_subplot(gs[0, 1])
    meta_ax.axis("off")

    # Title
    ax.set_title(f"Model Comparison for ADCP Transect {getattr(adcps[0], 'name', 'Unknown') if adcps else 'Unknown'}")

    # Remove top/right spines on main axes
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Mode mapping and descriptors
    mode_in = str(y_agg_mode).lower()
    mode_api = {"depth": "range", "bin": "bin", "range": "range", "hab": "hab", "mean": "mean"}.get(mode_in, mode_in)

    if mode_in in ("depth", "range"):
        mode_desc_val = f"Depth {target} (m)"
    elif mode_in == "bin":
        mode_desc_val = f"Bin {int(target)}"
    elif mode_in == "hab":
        mode_desc_val = f"{target} (m) above seabed"
    elif mode_in == "mean":
        mode_desc_val = "Depth-averaged"
    else:
        mode_desc_val = mode_in.capitalize()

    beam_desc_val = "Beam-average" if (isinstance(beam, str) and beam.lower() == "mean") else f"Beam {int(beam)}"

    have_vals = False
    y_min, y_max = np.inf, -np.inf
    w = max(1, int(smooth_window))

    global_t_min = None
    global_t_max = None
    obs_means, sim_means = [], []
    smoothing_desc_val = None  # e.g., "2-min rolling average"

    # Build and plot series
    for i, adcp in enumerate(adcps):
        # Observations (mg/L)
        if mode_in == "mean":
            ne, nb, _nm = adcp.get_beam_data("suspended_solids_concentration", mask=True).shape
            ys = []
            for b in range(1, nb + 1):
                y_b, _ = adcp.get_beam_series(
                    field_name="suspended_solids_concentration",
                    mode="bin", target=b, beam=beam, agg="mean"
                )
                ys.append(np.asarray(y_b, float))
            y_adcp = np.nanmean(np.vstack(ys), axis=0)
        else:
            y_adcp, _ = adcp.get_beam_series(
                field_name="suspended_solids_concentration",
                mode=("range" if mode_in == "depth" else mode_api),
                target=target,
                beam=beam,
                agg="mean",
            )
            y_adcp = np.asarray(y_adcp, float)

        # Model (kg/m^3 -> mg/L)
        t = np.asarray(pd.to_datetime(adcp.time.ensemble_datetimes).to_pydatetime())
        xq = np.asarray(adcp.position.x); yq = np.asarray(adcp.position.y)
        vals = mt_model.extract_transect_idw(xq=xq, yq=yq, t=t, item_number=model_item_num, input_crs = adcp.position.epsg)
        vals = vals*1000
        y_model = np.asarray(vals[0], float)

        # Align
        n = min(t.size, y_adcp.size, y_model.size)
        tt = t[:n]; yy_model = y_model[:n]; yy_adcp = y_adcp[:n]

        # Optional smoothing (x-min rolling average)
        this_smooth_desc = None
        if smooth_obs and n > 1:
            dt_sec = np.nanmedian(np.diff(tt).astype("timedelta64[s]").astype(float))
            yy_adcp = pd.Series(yy_adcp).rolling(window=w, center=True,
                                                 min_periods=max(1, w // 2)).mean().to_numpy()
            if np.isfinite(dt_sec) and dt_sec > 0:
                win_minutes = (w * dt_sec) / 60.0
                this_smooth_desc = (f"{win_minutes:.1f}-min rolling average"
                                    if win_minutes < 10 else f"{round(win_minutes):d}-min rolling average")
            else:
                this_smooth_desc = "Rolling average"
        if smoothing_desc_val is None:
            smoothing_desc_val = this_smooth_desc

        # Plot
        if i == 0:
            ax.plot(tt, yy_model, c=PlottingShell.blue1, lw=0.8, alpha=0.9, label="Simulated")
            ax.plot(tt, yy_adcp,  c=PlottingShell.red1,  lw=0.8, alpha=0.9, label="Observed")
        else:
            ax.plot(tt, yy_model, c=PlottingShell.blue1, lw=0.8, alpha=0.9)
            ax.plot(tt, yy_adcp,  c=PlottingShell.red1,  lw=0.8, alpha=0.9)

        # Extents and stats
        finite_vals = np.concatenate([yy_model[np.isfinite(yy_model)], yy_adcp[np.isfinite(yy_adcp)]])
        if finite_vals.size:
            have_vals = True
            y_min = min(y_min, float(finite_vals.min()))
            y_max = max(y_max, float(finite_vals.max()))
        obs_means.append(float(np.nanmean(yy_adcp)))
        sim_means.append(float(np.nanmean(yy_model)))

        # Time span
        if tt.size:
            global_t_min = tt[0] if global_t_min is None or tt[0] < global_t_min else global_t_min
            global_t_max = tt[-1] if global_t_max is None or tt[-1] > global_t_max else global_t_max

    # Axes cosmetics
    ax.set_ylabel("SSC (mg/L)")
    loc = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(loc)
    cfmt = mdates.ConciseDateFormatter(loc)
    ax.xaxis.set_major_formatter(cfmt)
    ax.legend(loc="upper right", frameon=False, fontsize=8)

    # Headroom for legend
    if have_vals:
        span = max(1e-9, y_max - y_min)
        ax.set_ylim(y_min - 0.05 * span, y_max + 0.18 * span)

    # Ticks: full date at START (two lines), others HH:MM:SS
    if global_t_min is not None and global_t_max is not None and global_t_max > global_t_min:
        ticks = ax.get_xticks()
        tick_dt = mdates.num2date(ticks)
        if len(tick_dt) >= 1:
            tick_dt[0] = global_t_min
            ax.set_xticks(mdates.date2num(tick_dt))
            labels = []
            for j, td in enumerate(tick_dt):
                if j == 0:
                    labels.append(f"{td.strftime('%b %d %Y')}\n{td.strftime('%H:%M')}")
                else:
                    labels.append(td.strftime("%H:%M:%S"))
            ax.set_xticklabels(labels, rotation=0, ha="center")

    # ---------------- Metadata panel (right column) ----------------
    start_txt = global_t_min.strftime("%b %d %Y %H:%M") if global_t_min else "N/A"
    end_txt   = global_t_max.strftime("%b %d %Y %H:%M") if global_t_max else "N/A"
    duration_h = ((global_t_max - global_t_min).total_seconds() / 3600.0) if (global_t_min and global_t_max) else np.nan
    mean_obs = float(np.nanmean(obs_means)) if obs_means else np.nan
    mean_sim = float(np.nanmean(sim_means)) if sim_means else np.nan

    # Titles and thin solid underlines
    sec1_title = "Observation Aggregation:"
    sec2_title = "Survey Timing:"
    sec3_title = "Summary Statistics:"
    thin = "─"  # U+2500 thin solid line
    sec1_underline = thin * len(sec1_title)
    sec2_underline = thin * len(sec2_title)
    sec3_underline = thin * len(sec3_title)

    meta_lines = [
        f"{sec1_title}",
        f"{sec1_underline}",
        f" Y-Mode: {mode_desc_val}",
        f" Beam: {beam_desc_val}",
        (f" Smoothing: {smoothing_desc_val}" if smoothing_desc_val else ""),
        "",
        f"{sec2_title}",
        f"{sec2_underline}",
        f" Start: {start_txt}",
        f" End: {end_txt}",
        f" Duration: {duration_h:.2f} h" if np.isfinite(duration_h) else " Duration: N/A",
        "",
        f"{sec3_title}",
        f"{sec3_underline}",
        f" Mean observed SSC:  {mean_obs:.3g} mg/L" if np.isfinite(mean_obs) else " Mean observed SSC: N/A",
        f" Mean simulated SSC: {mean_sim:.3g} mg/L" if np.isfinite(mean_sim) else " Mean simulated SSC: N/A",
    ]
    meta_text = "\n".join([ln for ln in meta_lines if ln is not None])

    # Top-left inside meta panel; fontsize 8; monospace for alignment
    meta_ax.text(
        0.0, 1.0, meta_text,
        va="top", ha="left",
        fontsize=8,
        family="monospace",
        transform=meta_ax.transAxes,
        wrap=True,
    )

    fig.show()
    return fig, ax








# # BIN, beam average, no smoothing
# timeseries_MT_comparison(
#     adcps, mt_model, model_item_num=1,
#     y_agg_mode="bin", target=5, beam="mean",
#     figheight=5, figwidth=7, smooth_obs=False
# )

# # BIN, single beam, smoothed
# timeseries_MT_comparison(
#     adcps, mt_model, model_item_num=1,
#     y_agg_mode="bin", target=12, beam=1,
#     smooth_obs=True, smooth_window=7
# )

# # RANGE/DEPTH, beam average, no smoothing
# timeseries_MT_comparison(
#     adcps, mt_model, model_item_num=1,
#     y_agg_mode="range", target=-3.0, beam="mean",
#     smooth_obs=False
# )

# # RANGE/DEPTH, single beam, smoothed
# timeseries_MT_comparison(
#     adcps, mt_model, model_item_num=1,
#     y_agg_mode="range", target=-3.5, beam=3,
#     smooth_obs=True, smooth_window=9
# )

# HAB, beam average, smoothed
timeseries_MT_comparison(
    adcps, mt_model, model_item_num=1,
    y_agg_mode="hab", target=2.0, beam="mean",
    smooth_obs=True, smooth_window=5
)

# # HAB, single beam, no smoothing
# timeseries_MT_comparison(
#     adcps, mt_model, model_item_num=1,
#     y_agg_mode="hab", target=1.0, beam=1,
#     smooth_obs=False
# )

# # MEAN (depth-averaged), beam average, smoothed
# timeseries_MT_comparison(
#     adcps, mt_model, model_item_num=1,
#     y_agg_mode="mean", beam="mean",
#     smooth_obs=True, smooth_window=11
# )

# MEAN (depth-averaged), single beam, no smoothing
# timeseries_MT_comparison(
#     adcps, mt_model, model_item_num=1,
#     y_agg_mode="mean", beam=2,
#     smooth_obs=False
# )



#%%
def plot_transect_distance_bars(
    adcp,
    mt_model,
    model_item_num,
    y_agg_mode="bin",     # {'bin','depth','hab','mean'}; 'depth' maps to API 'range'
    target=5,             # bin idx if 'bin'; meters if 'depth'/'range'/'hab'; ignored for 'mean'
    beam="mean",          # 'mean' or single int
    bin_width=10,         # meters; ignored if bin_edges provided
    bin_edges=None,       # array-like of bin edges in meters, optional
    figwidth=9,
    figheight=3,
):
    """
    Compare ADCP vs model SSC along a single transect using distance bins.
    Side-by-side bars per distance bin. Returns (fig, ax, table).
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # beam validation
    if isinstance(beam, (list, tuple, np.ndarray)):
        if len(beam) == 1:
            beam = int(beam[0])
        else:
            raise TypeError("beam must be 'mean' or a single integer.")
    if not ((isinstance(beam, str) and beam.lower() == "mean") or isinstance(beam, (int, np.integer))):
        raise TypeError("beam must be 'mean' or a single integer.")

    # ---- 1) ADCP series with requested vertical aggregation ----
    mode_in = str(y_agg_mode).lower()
    mode_api = {"depth": "range", "bin": "bin", "range": "range", "hab": "hab"}.get(mode_in, mode_in)

    def _adcp_series_mean():
        if mode_in == "mean":
            ne, nb, _nm = adcp.get_beam_data("suspended_solids_concentration", mask=True).shape
            ys = []
            for b in range(1, nb + 1):
                y_b, _ = adcp.get_beam_series(
                    field_name="suspended_solids_concentration",
                    mode="bin", target=b, beam=beam, agg="mean"
                )
                ys.append(np.asarray(y_b, float))
            return np.nanmean(np.vstack(ys), axis=0)
        else:
            y, _ = adcp.get_beam_series(
                field_name="suspended_solids_concentration",
                mode=mode_api, target=target, beam=beam, agg="mean"
            )
            return np.asarray(y, float)

    y_adcp = _adcp_series_mean()

    # ---- 2) Model extraction aligned to ensembles; kg/m^3 -> mg/L ----
    t = np.asarray(pd.to_datetime(adcp.time.ensemble_datetimes).to_pydatetime())
    xq = np.asarray(adcp.position.x)
    yq = np.asarray(adcp.position.y)
    d = np.asarray(adcp.position.distance, float)

    vals = mt_model.extract_transect_idw(xq=xq,
                                         yq=yq,
                                         t=t,
                                         item_number=model_item_num,
                                         input_crs = adcp.position.epsg)
    
    vals = vals*1000
    y_model = np.asarray(vals[0], float) 

    # Align lengths
    n = min(d.size, y_adcp.size, y_model.size)
    d = d[:n]; y_adcp = y_adcp[:n]; y_model = y_model[:n]

    # ---- 3) Distance binning ----
    if bin_edges is None:
        dmin, dmax = float(np.nanmin(d)), float(np.nanmax(d))
        if not np.isfinite([dmin, dmax]).all() or dmax <= dmin:
            raise ValueError("Invalid distances for binning.")
        nbins = max(1, int(np.ceil((dmax - dmin) / float(bin_width))))
        edges = np.linspace(dmin, dmax, nbins + 1)
    else:
        edges = np.asarray(bin_edges, float)
        if edges.ndim != 1 or edges.size < 2:
            raise ValueError("bin_edges must be 1D with at least 2 edges.")

    centers = 0.5 * (edges[:-1] + edges[1:])
    idx = np.digitize(d, edges) - 1
    nbins = edges.size - 1

    adcp_binned = np.full(nbins, np.nan)
    model_binned = np.full(nbins, np.nan)
    counts = np.zeros(nbins, dtype=int)

    for b in range(nbins):
        sel = (idx == b) & np.isfinite(y_adcp) & np.isfinite(y_model)
        counts[b] = int(sel.sum())
        if counts[b] > 0:
            adcp_binned[b] = float(np.nanmean(y_adcp[sel]))
            model_binned[b] = float(np.nanmean(y_model[sel]))

    empty_distances = int(np.count_nonzero(counts == 0))

    keep = counts > 0
    centers_plot = centers[keep]
    adcp_plot = adcp_binned[keep]
    model_plot = model_binned[keep]
    counts_plot = counts[keep]

    # ---- 4) Figure + metadata panel ----
    fig = plt.figure(figsize=(figwidth, figheight), constrained_layout=True)
    gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[3.2, 1.0])
    ax = fig.add_subplot(gs[0, 0])
    meta_ax = fig.add_subplot(gs[0, 1]); meta_ax.axis("off")

    # Title and spines
    ax.set_title(f"Model Comparison for ADCP Transect {getattr(adcp, 'name', 'Unknown')}", fontsize=8, pad=4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Bars
    if centers_plot.size > 1:
        base_dx = (centers_plot[1] - centers_plot[0])
        width = 0.25 * base_dx
    else:
        width = 3.0
    offset = 0.5 * width

    ax.bar(centers_plot - offset, model_plot, width=width, color=PlottingShell.blue1,
           alpha=0.9, label="Simulated", edgecolor="none")
    ax.bar(centers_plot + offset, adcp_plot,  width=width, color=PlottingShell.red1,
           alpha=0.9, label="Observed",  edgecolor="none")

    # Axis labels and ticks ≤ 8 pt
    ax.set_xlabel("Distance along transect (m)", fontsize=8, labelpad=2)
    ax.set_ylabel("SSC (mg/L)", fontsize=8, labelpad=2)
    ax.tick_params(axis="both", labelsize=8, pad=2)

    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(loc="upper right", frameon=False, fontsize=8)

    if centers_plot.size <= 12:
        ax.set_xticks(centers_plot)
        ax.set_xticklabels([f"{c:.0f}" for c in centers_plot], fontsize=8)

    # Ensure legend clearance with extra headroom
    finite_vals = np.concatenate([model_plot[np.isfinite(model_plot)], adcp_plot[np.isfinite(adcp_plot)]])
    if finite_vals.size:
        ymin = float(np.nanmin(finite_vals))
        ymax = float(np.nanmax(finite_vals))
        span = max(1e-9, ymax - ymin)
        top_pad = 0.28  # increased headroom
        ax.set_ylim(ymin - 0.05 * span, ymax + top_pad * span)

    # ---- 5) Metadata panel ----
    if mode_in in ("depth", "range"):
        mode_desc_val = f"Depth {target} (m)"
    elif mode_in == "bin":
        mode_desc_val = f"Bin {int(target)}"
    elif mode_in == "hab":
        mode_desc_val = f"{target} (m) above seabed"
    elif mode_in == "mean":
        mode_desc_val = "Depth-averaged"
    else:
        mode_desc_val = mode_in.capitalize()

    beam_desc_val = "Beam-average" if (isinstance(beam, str) and beam.lower() == "mean") else f"Beam {int(beam)}"

    start_txt = t[0].strftime("%b %d %Y %H:%M") if t.size else "N/A"
    end_txt   = t[-1].strftime("%b %d %Y %H:%M") if t.size else "N/A"
    duration_h = ((t[-1] - t[0]).total_seconds() / 3600.0) if t.size else np.nan

    mean_obs = float(np.nanmean(adcp_plot)) if adcp_plot.size else np.nan
    mean_sim = float(np.nanmean(model_plot)) if model_plot.size else np.nan

    sec1_title = "Observation Aggregation:"
    sec2_title = "Survey Timing:"
    sec3_title = "Summary Statistics:"
    thin = "─"
    sec1_underline = thin * len(sec1_title)
    sec2_underline = thin * len(sec2_title)
    sec3_underline = thin * len(sec3_title)

    meta_lines = [
        f"{sec1_title}",
        f"{sec1_underline}",
        f" Mode: {mode_desc_val}",
        f" Beam: {beam_desc_val}",
        "",
        f"{sec2_title}",
        f"{sec2_underline}",
        f" Start: {start_txt}",
        f" End: {end_txt}",
        f" Duration: {np.nan if not np.isfinite(duration_h) else round(duration_h, 2)} h",
        "",
        f"{sec3_title}",
        f"{sec3_underline}",
        f" Mean observed SSC:  {mean_obs:.3g} mg/L" if np.isfinite(mean_obs) else " Mean observed SSC: N/A",
        f" Mean simulated SSC: {mean_sim:.3g} mg/L" if np.isfinite(mean_sim) else " Mean simulated SSC: N/A",
        "",
    ]
    meta_text = "\n".join([ln for ln in meta_lines if ln is not None])

    meta_ax.text(
        0.0, 1.0, meta_text,
        va="top", ha="left",
        fontsize=8,
        family="monospace",
        transform=meta_ax.transAxes,
        wrap=True,
    )

    table = {
        "centers": centers_plot,
        "edges": edges,
        "adcp": adcp_plot,
        "model": model_plot,
        "counts": counts_plot,
    }
    return fig, ax, table




# # BIN mode, beam average
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="bin", target=5, beam="mean",
#     bin_width=10, figwidth=9, figheight=3
# )

# # BIN mode, single beam
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="bin", target=12, beam=1,
#     bin_width=10
# )

# # DEPTH/RANGE mode, ≥3 m, beam average
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="range", target=3.0, beam="mean",
#     bin_width=10
# )

# # DEPTH/RANGE mode, ≥3 m, single beam
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="depth", target=3.5, beam=2,
#     bin_width=10
# )

# # HAB mode, ≥3 m above seabed, beam average
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="hab", target=3.0, beam="mean",
#     bin_width=10
# )

# # HAB mode, ≥3 m, single beam
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="hab", target=3.2, beam=3,
#     bin_width=10
# )

# # MEAN (depth-averaged), beam average
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="mean", beam="mean",
#     bin_width=10
# )

# MEAN, single beam
plot_transect_distance_bars(
    adcp, mt_model, model_item_num=1,
    y_agg_mode="mean", beam=1,
    bin_width=10
)

# # Custom edges, depth mode with ≥3 m target
# plot_transect_distance_bars(
#     adcp, mt_model, model_item_num=1,
#     y_agg_mode="range", target=4.0, beam="mean",
#     bin_edges=[0, 40, 85, 130, 180, 240, 300]
# )

# Custom edges, HAB mode with ≥3 m target
plot_transect_distance_bars(
    adcp, mt_model, model_item_num=1,
    y_agg_mode="hab", target=5.0, beam=2,
    bin_edges=[0, 30, 60, 100, 160, 230, 300]
)


#%%
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon as MplPolygon
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

# ------------ shapefile I/O and drawing ------------

def _gdf_lonlat(path):
    try:
        import geopandas as gpd
        gdf = gpd.read_file(path)
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)
        return gdf
    except Exception:
        return None

def _pyshp_iter_geoms_lonlat(path):
    import shapefile
    from pyproj import Transformer, CRS

    sf = shapefile.Reader(path)
    transformer = None
    prj = os.path.splitext(path)[0] + ".prj"
    if os.path.exists(prj):
        try:
            with open(prj, "r") as f:
                wkt = f.read()
            crs_src = CRS.from_wkt(wkt)
            if crs_src and crs_src.to_epsg() != 4326:
                transformer = Transformer.from_crs(crs_src, CRS.from_epsg(4326), always_xy=True)
        except Exception:
            transformer = None

    for shp in sf.shapes():
        pts = np.asarray(shp.points, float)
        if transformer is not None:
            x, y = transformer.transform(pts[:, 0], pts[:, 1])
            pts = np.column_stack([x, y])

        st = shp.shapeType
        if st in (1, 11, 21):          # POINT*
            yield ("point", pts[0:1, :])
        elif st in (8, 18, 28):         # MULTIPOINT*
            yield ("point", pts)
        elif st in (3, 13, 23):         # POLYLINE*
            parts = list(shp.parts) + [len(pts)]
            for i in range(len(parts) - 1):
                seg = pts[parts[i]:parts[i + 1]]
                yield ("line", seg)
        elif st in (5, 15, 25):         # POLYGON*
            parts = list(shp.parts) + [len(pts)]
            rings = [pts[parts[i]:parts[i + 1]] for i in range(len(parts) - 1)]
            if rings:
                yield ("polygon", rings[0], rings[1:])  # (exterior, holes)

def _draw_shapefiles(ax, shp_specs):
    if not shp_specs:
        return
    for spec in shp_specs:
        path = spec.get("path")
        kind = str(spec.get("type", "line")).lower()
        if not path or not os.path.exists(path):
            print(f"[shapefile] not found: {path}")
            continue

        # unified style getters
        line_color = spec.get("color", spec.get("edgecolor", "#333333"))
        line_width = float(spec.get("width", spec.get("linewidth", 0.8)))
        line_alpha = float(spec.get("alpha", 1.0))
        # NEW: fill color/alpha (aliases supported); default fill_alpha=1 per request
        fill_color = spec.get("fill_color", spec.get("fillcolor", None))
        fill_alpha = float(spec.get("fill_alpha", 1.0))

        gdf = _gdf_lonlat(path)
        if gdf is not None:
            geoms = gdf.geometry
            if kind == "point":
                col = line_color
                ms  = float(spec.get("markersize", 6))
                lbl = spec.get("label")
                fs  = float(spec.get("label_fontsize", 10))
                lc  = spec.get("label_color", col)
                for geom in geoms:
                    if geom is None:
                        continue
                    rp = geom.representative_point()
                    xs = np.atleast_1d(rp.x); ys = np.atleast_1d(rp.y)
                    ax.scatter(xs, ys, s=ms**2, c=col, marker="o",
                               edgecolors="k", linewidths=0.4, zorder=3)
                    if lbl:
                        ax.text(xs[0], ys[0], str(lbl), fontsize=fs, color=lc,
                                ha="left", va="bottom",
                                bbox=dict(boxstyle="round,pad=0.2", fc=(1, 1, 1, 0.7), ec="none"))
            elif kind == "line":
                for geom in geoms:
                    if geom is None:
                        continue
                    if geom.geom_type in ("LineString", "MultiLineString"):
                        parts = [geom] if geom.geom_type == "LineString" else list(geom.geoms)
                        for ln in parts:
                            x, y = ln.xy
                            ax.plot(x, y, color=line_color, lw=line_width, alpha=line_alpha)
                    elif geom.geom_type in ("Polygon", "MultiPolygon"):
                        parts = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
                        for poly in parts:
                            x, y = poly.exterior.xy
                            ax.plot(x, y, color=line_color, lw=line_width, alpha=line_alpha)
            elif kind == "polygon":
                for geom in geoms:
                    if geom is None:
                        continue
                    parts = [geom] if geom.geom_type == "Polygon" else (list(geom.geoms) if geom.geom_type == "MultiPolygon" else [])
                    for poly in parts:
                        x, y = poly.exterior.xy
                        ax.plot(x, y, color=line_color, lw=line_width, alpha=line_alpha)
                        if fill_color:
                            ax.add_patch(MplPolygon(np.column_stack([x, y]), closed=True,
                                                    facecolor=fill_color, alpha=fill_alpha, edgecolor="none"))
        else:
            # pyshp fallback
            try:
                for item in _pyshp_iter_geoms_lonlat(path):
                    if kind == "point" and item[0] == "point":
                        pts = item[1]
                        ms  = float(spec.get("markersize", 6))
                        lbl = spec.get("label")
                        fs  = float(spec.get("label_fontsize", 10))
                        lc  = spec.get("label_color", line_color)
                        ax.scatter(pts[:, 0], pts[:, 1], s=ms**2, c=line_color, marker="o",
                                   edgecolors="k", linewidths=0.4, zorder=3)
                        if lbl and pts.shape[0] > 0:
                            ax.text(pts[0, 0], pts[0, 1], str(lbl), fontsize=fs, color=lc,
                                    ha="left", va="bottom",
                                    bbox=dict(boxstyle="round,pad=0.2", fc=(1, 1, 1, 0.7), ec="none"))
                    elif kind == "line" and item[0] == "line":
                        seg = item[1]
                        ax.plot(seg[:, 0], seg[:, 1], color=line_color, lw=line_width, alpha=line_alpha)
                    elif kind == "polygon" and item[0] == "polygon":
                        ext, holes = item[1], item[2]
                        ax.plot(ext[:, 0], ext[:, 1], color=line_color, lw=line_width, alpha=line_alpha)
                        if fill_color:
                            ax.add_patch(MplPolygon(ext, closed=True, facecolor=fill_color, alpha=fill_alpha, edgecolor="none"))
            except Exception as e:
                print(f"[shapefile] failed to draw {path}: {e}")

def plot_transect_model_with_distance_bins(
    adcp, model, item_number:int,
    pad:float=0.05, pixel_size_m:float=25.0, k:int=12, p:float=2.0,
    cmap="turbo",
    overlay_color="magenta", overlay_outline_color="white", overlay_outline_width:float=2.0,
    y_agg_mode:str="bin", target=5, bin_width:float=25.0, bin_edges=None,
    shp=None, shapefile_path:str|None=None,
    cbar_bottom_thresh:float=0.01,
    title_left="Simulated SSC Averaged Over Transect Duration",
    title_right: str | None = None,
):
    from matplotlib.ticker import FormatStrFormatter

    # ---- ADCP inputs
    t_dt  = np.asarray(adcp.time.ensemble_datetimes)
    pos   = adcp.position
    x_deg = np.asarray(getattr(pos,"lon",getattr(pos,"longitude",getattr(pos,"x_deg",pos.x))), float).ravel()
    y_deg = np.asarray(getattr(pos,"lat",getattr(pos,"latitude",getattr(pos,"y_deg",pos.y))), float).ravel()
    dist  = np.asarray(pos.distance, float).ravel()
    n = min(x_deg.size, y_deg.size, t_dt.size, dist.size)
    x_deg, y_deg, t_dt, dist = x_deg[:n], y_deg[:n], t_dt[:n], dist[:n]

    # ---- Raster (mg/L)
    Xg, Yg, Zg, extent = model.rasterize_idw_bbox(
        xq=x_deg,
        yq=y_deg,
        t=t_dt.astype("datetime64[ns]"),
        item_number=item_number,
        pad=pad, 
        pixel_size_m=pixel_size_m,
        k=k,
        p=p,
        debug=False, 
        input_crs = adcp.position.epsg,
        output_crs = adcp.position.epsg
    )
    Z_mgL = np.asarray(Zg, float) * 1000.0

    # ---- ADCP SSC mean-of-4 beams
    mode_in  = str(y_agg_mode).lower()
    mode_api = {"depth":"range","range":"range","bin":"bin","hab":"hab"}.get(mode_in, mode_in)

    def _adcp_ssc_mean4():
        if mode_in == "mean":
            ne, nb, _ = adcp.get_beam_data("suspended_solids_concentration", mask=True).shape
            ys=[]
            for b in range(1, nb+1):
                yb,_ = adcp.get_beam_series("suspended_solids_concentration", mode="bin", target=b, beam="mean", agg="mean")
                ys.append(np.asarray(yb,float))
            return np.nanmean(np.vstack(ys), axis=0)
        y,_ = adcp.get_beam_series("suspended_solids_concentration", mode=mode_api, target=target, beam="mean", agg="mean")
        return np.asarray(y,float)

    y_adcp  = _adcp_ssc_mean4()[:n]
    y_model = np.asarray(
        model.extract_transect_idw(xq=x_deg, yq=y_deg, t=t_dt.astype("datetime64[ns]"),
                                   item_number=item_number, input_crs = adcp.position.epsg)[0], float
    )[:n] * 1000.0

    # ---- Distance bins
    if bin_edges is None:
        dmin, dmax = float(np.nanmin(dist)), float(np.nanmax(dist))
        nbins = max(1, int(np.ceil((dmax-dmin)/float(bin_width))))
        edges = np.linspace(dmin, dmax, nbins+1)
    else:
        edges = np.asarray(bin_edges, float)
        if edges.ndim!=1 or edges.size<2:
            raise ValueError("bin_edges must be 1D with ≥2 edges.")
    centers = 0.5*(edges[:-1]+edges[1:])
    idx = np.digitize(dist, edges)-1
    nbins = edges.size-1
    adcp_binned  = np.full(nbins, np.nan)
    model_binned = np.full(nbins, np.nan)
    counts       = np.zeros(nbins, int)
    for b in range(nbins):
        sel=(idx==b)&np.isfinite(y_adcp)&np.isfinite(y_model)
        counts[b]=int(sel.sum())
        if counts[b]>0:
            adcp_binned[b]=float(np.nanmean(y_adcp[sel]))
            model_binned[b]=float(np.nanmean(y_model[sel]))
    keep=counts>0
    centers_plot=centers[keep]; adcp_plot=adcp_binned[keep]; model_plot=model_binned[keep]

    # ---- Colormap with transparent under-threshold
    cm = matplotlib.colormaps.get_cmap(cmap).copy()
    cm.set_under((1,1,1,0)); cm.set_bad((1,1,1,0))

    # =================== LAYOUT: 3 axes, fixed margins. ===================
    fig = plt.figure(figsize=(10, 3))
    gs = fig.add_gridspec(
        nrows=1, ncols=3,
        width_ratios=[1.0, 1.0, 0.5],
        left=0.08, right=0.9, bottom=0.12, top=0.90,
        wspace=0.12, hspace=0.05)

    axL     = fig.add_subplot(gs[0,0])
    axR     = fig.add_subplot(gs[0,1])
    meta_ax = fig.add_subplot(gs[0,2]); meta_ax.axis("off")

    # ----- LHS: image
    vmax_img = np.nanmax(Z_mgL[np.isfinite(Z_mgL)])
    if not np.isfinite(vmax_img):
        vmax_img = cbar_bottom_thresh*2
        
    im = axL.imshow(
        Z_mgL, extent=extent, origin="lower",
        cmap=cm, vmin=cbar_bottom_thresh, vmax=vmax_img,
        interpolation="nearest"
    )

    # shapefiles
    specs = shp if shp is not None else ([{"path": shapefile_path, "type": "line"}] if shapefile_path else None)
    if specs:
        _draw_shapefiles(axL, specs)

    # ADCP transect
    axL.plot(x_deg, y_deg, color=overlay_outline_color, lw=overlay_outline_width, solid_capstyle="round")
    axL.plot(x_deg, y_deg, color=overlay_color, lw=max(0.8, 0.5*overlay_outline_width),
             label="ADCP transect", solid_capstyle="round")
    leg = axL.legend(loc="upper right", fontsize=8, frameon=True)
    leg.get_frame().set_facecolor('white')
    #leg.get_frame().set_edgecolor((0,0,0,0.25))

    # square zoom
    xmin,xmax,ymin,ymax = extent; w=xmax-xmin; h=ymax-ymin
    if w>=h:
        cy=0.5*(ymin+ymax); half=0.5*w; axL.set_xlim(xmin,xmax); axL.set_ylim(cy-half, cy+half)
    else:
        cx=0.5*(xmin+xmax); half=0.5*h; axL.set_xlim(cx-half, cx+half); axL.set_ylim(ymin,ymax)
    axL.set_aspect("equal"); axL.set_autoscale_on(False)

    # labels/ticks; 3-decimal lon/lat
    axL.set_xlabel("Longitude (°)", fontsize=8)
    axL.set_ylabel("Latitude (°)", fontsize=8)
    axL.set_title(title_left, fontsize=8, pad=6)
    axL.tick_params(axis="both", labelsize=6, pad=2)
    axL.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    axL.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

    
    # colorbar appended to LHS axis
    divL = make_axes_locatable(axL)
    cax  = divL.append_axes("right", size="3%", pad=0.03)

    # ----- RHS: bars
    rhs_title = title_right or f"model comparison along ADCP transect {getattr(adcp,'name','Unknown')}"
    axR.set_title(rhs_title, fontsize=8, pad=6)
    if centers_plot.size>1:
        bw=0.25*(centers_plot[1]-centers_plot[0])
    else: 
        bw=3.0
    off=0.5*bw
    axR.bar(centers_plot-off, model_plot, width=bw, color="#1f77b4", alpha=0.95, label="Simulated", edgecolor="none")
    axR.bar(centers_plot+off, adcp_plot,  width=bw, color=overlay_color, alpha=0.95, label="Observed",  edgecolor="none")
    axR.set_xlabel("Distance along transect (m)", fontsize=8, labelpad=2)
    axR.set_ylabel("SSC (mg/L)", fontsize=8, labelpad=2)
    axR.tick_params(axis="both", labelsize=8, pad=2)
    axR.grid(True, axis="y", alpha=0.3)
    axR.legend(loc="upper right", frameon=False, fontsize=8, borderaxespad=0.4)
    if centers_plot.size<=12:
        axR.set_xticks(centers_plot)
        axR.set_xticklabels([f"{c:.0f}" for c in centers_plot], fontsize=8)

    finite_rhs = np.concatenate([model_plot[np.isfinite(model_plot)], adcp_plot[np.isfinite(adcp_plot)]])
    if finite_rhs.size:
        ymin_rhs=float(np.nanmin(finite_rhs))
        ymax_rhs=float(np.nanmax(finite_rhs))
        span=max(1e-9, ymax_rhs-ymin_rhs)
        axR.set_ylim(ymin_rhs-0.05*span, ymax_rhs+0.18*span)

    # update image clim to RHS y-lims
    y0_vis, y1_vis = axR.get_ylim()
    if y1_vis<=cbar_bottom_thresh:
        y1_vis=cbar_bottom_thresh*1.01
    im.set_clim(vmin=cbar_bottom_thresh, vmax=y1_vis)

    # ----- Colorbar
    n_above=256
    colors_above = matplotlib.colormaps.get_cmap(cmap)(np.linspace(0,1,n_above))
    colors_cb = np.vstack([np.array([[1,1,1,1]]), colors_above])
    cmap_cb = ListedColormap(colors_cb)
    eps=max(1e-9,1e-6*cbar_bottom_thresh); v0=min(y0_vis, cbar_bottom_thresh-eps); v1=cbar_bottom_thresh; v2=max(y1_vis, v1+eps)
    bounds = np.concatenate((np.array([v0, v1], float), np.linspace(v1, v2, n_above)))
    norm_cb = BoundaryNorm(bounds, cmap_cb.N)
    sm = plt.cm.ScalarMappable(norm=norm_cb, cmap=cmap_cb)
    cb = plt.colorbar(sm, cax=cax, orientation="vertical")
    yt = axR.get_yticks(); yt = yt[(yt>=v1)&(yt<=v2)]
    white_tick = 0.5*(v0+v1)
    cb.set_ticks(np.concatenate(([white_tick], yt)))
    cb.set_ticklabels([f"< {v1:g}"] + [f"{val:g}" for val in yt])
    cb.ax.tick_params(labelsize=8, pad=2)
    cb.ax.minorticks_off()

    # ----- Metadata axis
    meta_ax.set_clip_on(True)
    meta_ax.set_xlim(0,1); meta_ax.set_ylim(0,1)
    if mode_in in ("depth","range"): mode_desc=f"Depth {target} (m)"
    elif mode_in=="bin":             mode_desc=f"Bin {int(target)}"
    elif mode_in=="hab":             mode_desc=f"{target} m above seabed"
    elif mode_in=="mean":            mode_desc="Depth-averaged"
    else:                            mode_desc = mode_in.capitalize()
    beam_desc="Beam-average"
    t_np=np.asarray(t_dt,dtype="datetime64[ns]").ravel()
    if t_np.size:
        start_txt=np.datetime_as_string(t_np[0], unit='s')
        end_txt  =np.datetime_as_string(t_np[-1], unit='s')
        duration_h=(t_np[-1]-t_np[0]).astype("timedelta64[s]").astype(float)/3600.0
    else:
        start_txt=end_txt="N/A"; duration_h=np.nan
    mean_obs=float(np.nanmean(adcp_plot)) if adcp_plot.size else np.nan
    mean_sim=float(np.nanmean(model_plot)) if model_plot.size else np.nan
    sec1="Observation Aggregation:"; ul1="─"*len(sec1)
    sec2="Survey Timing:";           ul2="─"*len(sec2)
    sec3="Summary Statistics:";      ul3="─"*len(sec3)
    text="\n".join([
        sec1, ul1, f"Mode:  {mode_desc}", f"Beam:  {beam_desc}", "",
        sec2, ul2, f"Start: {start_txt}", f"End:   {end_txt}",
        f"Dur:   {np.nan if not np.isfinite(duration_h) else round(duration_h,2)} h", "",
        sec3, ul3,
        f"Mean observed SSC:  {'N/A' if not np.isfinite(mean_obs) else f'{mean_obs:.3g}'} mg/L",
        f"Mean simulated SSC: {'N/A' if not np.isfinite(mean_sim) else f'{mean_sim:.3g}'} mg/L",
    ])
    box = FancyBboxPatch((0.06,0.06),0.88,0.88, boxstyle="round,pad=0.35",
                         linewidth=0.8, edgecolor="#888", facecolor="white",
                         transform=meta_ax.transAxes)
    meta_ax.add_patch(box)
    meta_ax.text(0.08,0.94,text,ha="left",va="top",fontsize=8,family="monospace",transform=meta_ax.transAxes)

    # keep boxes inside pane
    for ax in (axL, axR, meta_ax):
        try: ax.set_anchor("C")
        except Exception: pass

    outputs={
        "raster":(Xg,Yg,Z_mgL,extent),
        "bins":{"centers":centers_plot,"edges":edges,"adcp":adcp_plot,"model":model_plot,"counts":counts[keep]},
        "cbar_limits":(cbar_bottom_thresh, y1_vis),
        "cbar_bottom_thresh":cbar_bottom_thresh,
    }
    return fig,(axL,axR),outputs



#%%
import numpy as np
import matplotlib.pyplot as plt

# Shapefile layers demonstrating all styling fields supported
shp_layers = [

    {
        "path": r"C:/Users/anba/Downloads/v20250509/v20250509/points_labels.shp",
        "type": "point",
        "color": "#FFD166",     # marker facecolor
        "markersize": 6,        # marker size in points
        "label": "Source Location",
        "label_fontsize": 11,
        "label_color": "pink"
    },
    {
        "path": '/Users/anba/Downloads/v20250509/v20250509/RD7550_CEx_SG_v20250509.shp',
        "type": "polygon",
        "edgecolor": "#222222",   # polygon edge color
        "linewidth": 1.2,         # polygon edge width
        "fill_color": "lightgray",  # polygon fill color (NEW)
        "fill_alpha": 1.0         # polygon fill alpha (default 1.0)
    }
]

# Optional explicit distance-bin edges (demonstrates bin_edges usage)
bin_edges = np.linspace(0, 500, 11)  # 0..500 m in 50 m bins

fig, (axL, axR), out = plot_transect_model_with_distance_bins(
    adcp=adcp,
    model=mt_model,
    item_number=1,
    # ROI + raster controls
    pad=0.01,                 # degrees
    pixel_size_m=5.0,         # meters per pixel
    k=8, p=2.0,
    # Visuals
    cmap="turbo",
    overlay_color=PlottingShell.red1,          # ADCP transect + RHS observed bars
    overlay_outline_color="white",
    overlay_outline_width=2.5,
    # RHS aggregation
    y_agg_mode="bin",         # {'bin','depth','hab','mean'}
    target=5,                 # if 'bin' → bin index; if 'depth'/'hab' → meters
    bin_width=25.0,           # used when bin_edges is None
    bin_edges=bin_edges,      # explicit edges example
    # Shapefiles (layer list) and legacy single-path shown explicitly
    shp=shp_layers,
    shapefile_path=None,      # legacy single path; keep None when using shp list
    # Colorbar threshold (values below shown as white, segment labeled "< thresh")
    cbar_bottom_thresh=0.01,  # mg/L
    # Titles
    title_left="Mean Simulated SSC During Transect",
    title_right=f"Model Comparison along Transect {adcp.name}"
)
plt.show()

#%%
# --- return overlay artists so animator can redraw them every frame -----------
def _draw_shapefiles(ax, shp_specs):
    import os, numpy as np
    from matplotlib.patches import Polygon as MplPolygon
    artists = []
    if not shp_specs:
        return artists
    for spec in shp_specs:
        path = spec.get("path")
        kind = str(spec.get("type", "line")).lower()
        if not path or not os.path.exists(path):
            print(f"[shapefile] not found: {path}")
            continue
        line_color = spec.get("color", spec.get("edgecolor", "#333333"))
        line_width = float(spec.get("width", spec.get("linewidth", 0.8)))
        line_alpha = float(spec.get("alpha", 1.0))
        fill_color = spec.get("fill_color", spec.get("fillcolor", None))
        fill_alpha = float(spec.get("fill_alpha", 1.0))
        z = float(spec.get("zorder", 5.0))  # above raster

        gdf = _gdf_lonlat(path)
        if gdf is not None:
            geoms = gdf.geometry
            if kind == "point":
                ms  = float(spec.get("markersize", 6))
                lbl = spec.get("label"); fs = float(spec.get("label_fontsize", 8))
                lc  = spec.get("label_color", line_color)
                for geom in geoms:
                    if geom is None: continue
                    rp = geom.representative_point()
                    xs = np.atleast_1d(rp.x); ys = np.atleast_1d(rp.y)
                    sc = ax.scatter(xs, ys, s=ms**2, c=line_color, marker="o",
                                    edgecolors="k", linewidths=0.4, zorder=z)
                    artists.append(sc)
                    if lbl:
                        tx = ax.text(xs[0], ys[0], str(lbl), fontsize=fs, color=lc,
                                     ha="left", va="bottom",
                                     bbox=dict(boxstyle="round,pad=0.2", fc=(1,1,1,0.7), ec="none"),
                                     zorder=z+0.1)
                        artists.append(tx)
            elif kind == "line":
                for geom in geoms:
                    if geom is None: continue
                    if geom.geom_type in ("LineString", "MultiLineString"):
                        parts = [geom] if geom.geom_type == "LineString" else list(geom.geoms)
                        for ln in parts:
                            x, y = ln.xy
                            lnobj, = ax.plot(x, y, color=line_color, lw=line_width, alpha=line_alpha, zorder=z)
                            artists.append(lnobj)
                    elif geom.geom_type in ("Polygon", "MultiPolygon"):
                        parts = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
                        for poly in parts:
                            x, y = poly.exterior.xy
                            lnobj, = ax.plot(x, y, color=line_color, lw=line_width, alpha=line_alpha, zorder=z)
                            artists.append(lnobj)
                            if fill_color:
                                pg = MplPolygon(np.column_stack([x, y]), closed=True,
                                                facecolor=fill_color, alpha=fill_alpha, edgecolor="none", zorder=z)
                                ax.add_patch(pg); artists.append(pg)
            elif kind == "polygon":
                for geom in geoms:
                    if geom is None: continue
                    parts = [geom] if geom.geom_type == "Polygon" else (list(geom.geoms) if geom.geom_type == "MultiPolygon" else [])
                    for poly in parts:
                        x, y = poly.exterior.xy
                        lnobj, = ax.plot(x, y, color=line_color, lw=line_width, alpha=line_alpha, zorder=z)
                        artists.append(lnobj)
                        if fill_color:
                            pg = MplPolygon(np.column_stack([x, y]), closed=True,
                                            facecolor=fill_color, alpha=fill_alpha, edgecolor="none", zorder=z)
                            ax.add_patch(pg); artists.append(pg)
        else:
            try:
                for item in _pyshp_iter_geoms_lonlat(path):
                    if kind == "point" and item[0] == "point":
                        pts = item[1]
                        ms  = float(spec.get("markersize", 6))
                        lbl = spec.get("label"); fs = float(spec.get("label_fontsize", 8))
                        lc  = spec.get("label_color", line_color)
                        sc = ax.scatter(pts[:,0], pts[:,1], s=ms**2, c=line_color, marker="o",
                                        edgecolors="k", linewidths=0.4, zorder=z)
                        artists.append(sc)
                        if lbl and pts.shape[0] > 0:
                            tx = ax.text(pts[0,0], pts[0,1], str(lbl), fontsize=fs, color=lc,
                                         ha="left", va="bottom",
                                         bbox=dict(boxstyle="round,pad=0.2", fc=(1,1,1,0.7), ec="none"),
                                         zorder=z+0.1)
                            artists.append(tx)
                    elif kind == "line" and item[0] == "line":
                        seg = item[1]
                        lnobj, = ax.plot(seg[:,0], seg[:,1], color=line_color, lw=line_width, alpha=line_alpha, zorder=z)
                        artists.append(lnobj)
                    elif kind == "polygon" and item[0] == "polygon":
                        ext, holes = item[1], item[2]
                        lnobj, = ax.plot(ext[:,0], ext[:,1], color=line_color, lw=line_width, alpha=line_alpha, zorder=z)
                        artists.append(lnobj)
                        if fill_color:
                            pg = MplPolygon(ext, closed=True, facecolor=fill_color, alpha=fill_alpha, edgecolor="none", zorder=z)
                            ax.add_patch(pg); artists.append(pg)
            except Exception as e:
                print(f"[shapefile] failed to draw {path}: {e}")
    return artists


def animate_bbox_timeseries(
    out: dict,
    *,
    shp=None,
    shapefile_path: str | None=None,
    cmap: str="turbo",
    cbar_bottom_thresh: float=0.01,   # mg/L; log vmin lower bound
    vmax: float | None=None,          # None → 99th percentile of frames
    interval: int=120,                # ms between frames
    figsize: tuple[int,int]=(6, 4),
    dpi: int=150,
    gif_path: str | None=None,        # set path to export GIF
    fps: int=8,
):
    """
    Log-scaled animation for bbox rasters.
    - Colorbar ticks at [0.01, 0.1, 0.5, 1, 5, 10, 50, 100] mg/L (always shown).
    - All fontsizes = 6.
    - Shapefile overlays remain above the raster each frame (works with blitting).
    """
    import numpy as np, matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    from matplotlib.ticker import FormatStrFormatter
    from matplotlib.colors import LogNorm
    from datetime import datetime

    # --- inputs
    frames = np.asarray(out["frames"])  # mg/L, shape (t, ny, nx) or list
    extent = tuple(out["extent"])       # (xmin, xmax, ymin, ymax)
    times  = np.asarray(out["times"])   # numpy datetime64

    # --- desired log tick set (mg/L)
    desired_ticks = np.array([0.01, 0.1,  1.0, 10.0,  100.0], float)

    # --- compute vmin/vmax to COVER the full tick set (so all labels appear)
    tiny = 1e-12
    vmin = max(float(cbar_bottom_thresh), desired_ticks.min(), tiny)
    if vmax is None:
        vmax = float(np.nanpercentile(frames, 99))
    vmax = max(vmax, desired_ticks.max(), vmin * 1.01)

    # --- colormap
    cm = matplotlib.colormaps.get_cmap(cmap).copy()
    cm.set_under((1, 1, 1, 1))  # for any masked/below-data if used
    cm.set_bad((1, 1, 1, 0))

    # --- figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(left=0.1, right=0.90, bottom=0.12, top=0.96)
    # --- image
    norm = LogNorm(vmin=vmin, vmax=vmax, clip=False)
    im = ax.imshow(
        frames[0], extent=extent, origin="lower",
        cmap=cm, norm=norm, interpolation="nearest", zorder=1
    )

    # --- axes style (all fontsizes = 6)
    ax.set_xlabel("Longitude (°)", fontsize=6, labelpad=2)
    ax.set_ylabel("Latitude (°)", fontsize=6, labelpad=2)
    ax.tick_params(axis="both", labelsize=6, pad=1.5)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_aspect("equal")
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])

    # --- shapefile overlays on top; keep artist handles for blitting
    specs = shp if shp is not None else ([{"path": shapefile_path, "type": "line"}] if shapefile_path else None)
    overlay_artists = []
    if specs:
        for s in specs:
            s["zorder"] = max(5.0, float(s.get("zorder", 5.0)))
        # _draw_shapefiles should return a list of artists; fall back to []
        arts = _draw_shapefiles(ax, specs)
        overlay_artists = arts if isinstance(arts, (list, tuple)) else []

    # --- time textbox (UTC) "DD Mon YYYY HH:MM"
    def _fmt_time(ti):
        ts_ns = int(np.asarray(ti, dtype="datetime64[ns]").astype("int"))
        return datetime.utcfromtimestamp(ts_ns / 1e9).strftime("%d %b %Y %H:%M")

    ts_box = ax.text(
        0.02, 0.98, _fmt_time(times[0]),
        transform=ax.transAxes, ha="left", va="top",
        fontsize=6, family="monospace",
        bbox=dict(boxstyle="round,pad=0.2", fc=(1, 1, 1, 0.8), ec="none"),
        zorder=6
    )

    # --- colorbar: narrow width, no minor ticks, ALL desired labels shown
    cb = fig.colorbar(im, ax=ax, fraction=0.018, pad=0.02)
    cb.ax.tick_params(labelsize=6, pad=1.5)
    cb.ax.minorticks_off()
    cb.set_ticks(desired_ticks)
    cb.set_ticklabels([f"{t:g}" for t in desired_ticks])
    cb.set_label('SSC (mg/L)', fontsize=6, labelpad=2)
    ax.set_aspect("equal", adjustable="box")
    ax.set_anchor("W")          # shove content to the left
    ax.margins(0.1)               # no extra data margins
        # --- animator
    def _update(i):
        im.set_data(frames[i])
        ts_box.set_text(_fmt_time(times[i]))
        # return overlay artists so they redraw above the raster when blitting
        return (im, ts_box, *overlay_artists)

    ani = FuncAnimation(fig, _update, frames=frames.shape[0], interval=interval, blit=True)

    # --- optional GIF export
    if gif_path:
        ani.save(gif_path, writer=matplotlib.animation.PillowWriter(fps=fps), dpi=dpi)

    return fig, ani




#%%
#dsa
#bbox = (103.95, 104.09, 1.30, 1.42)
bbox = (cx.min(), cx.max(),cy.min(),cy.max())
out = mt_model.rasterize_bbox_timeseries(
    item_number=1,
    bbox=bbox,
    pixel_size_m=100.0,
    k=8, 
    p=2.0,
    times=mt_model.model_times,
    pad=0.0,
    as_stack=True,
    output_crs = adcp.position.epsg
)

out['frames'] = out['frames']*1000

#%%
# Optional shapefile layers (reuse your existing style spec)
shp_layers = [
    {"path": r'/Users/anba/Downloads/v20250509/v20250509/RD7550_CEx_SG_v20250509.shp',
     "type": "polygon",
     "edgecolor": "#222",
     "linewidth": 1.0,
     "fill_color": "lightgray", "fill_alpha": 1.0}
]

fig, ani = animate_bbox_timeseries(
    out,
    shp=shp_layers,           # or shapefile_path="/path/to/your.shp"
    cmap="turbo",
    cbar_bottom_thresh=0.001,     # None → 99th pct across frames
    interval=5,
    figsize=(4,4),
    dpi=100,
    gif_path=r'C:\Users\anba\OneDrive - DHI\Desktop\Documents\GitHub\PlumeTrack\backend\model_gif_test2.gif', 
    fps = 8,            # e.g., "model_anim.gif" to export
)

plt.show()
