
import sys
import os


# Add the project root (one level up from /tests/) to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend
from backend.pd0 import Pd0Decoder
from backend.adcp import ADCP as DatasetADCP
from backend._adcp_position import ADCPPosition
from backend.utils import Utils, CSVParser
from backend.plotting import PlottingShell

import matplotlib.pyplot as plt

root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2024_survey_data\10. Oct\20241024_F3(E)'

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
            




#%%

pd0 = Pd0Decoder(pd0_fpaths[0], cfg = {})

#vl = pd0._get_variable_leader()[0].to_dict()




#%% init position datasets
pos_cfgs = []
position_datasets = []
for i,fpath in enumerate(pos_fpaths):
    print(i)
    cfg = {'filename':fpath,
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
    pos_cfgs.append(cfg)
    #position_datasets.append(ADCPPosition(cfg))

#%%

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
cfgs = []
position_datasets = []
adcps = []
for i,fpath in enumerate(pd0_fpaths):
    print(i)
    name = fpath.split(os.sep)[-1].split('.000')[0]
    cfg = {'filename':fpath,
           'name':name,
           'pos_cfg':pos_cfgs[i],
           'pg_min' : 50,
           'vel_min' : -2.0,
           'vel_max' : 2.0,
           'echo_min' : 0,
           'echo_max' : 255,
           'cormag_min' : 0,
           'cormag_max' : 255,
           'abs_min' : -100,
           'abs_max': 0,
           'err_vel_max' : 0.5,
           'start_datetime' : None,
           'end_datetime' : None,
           'first_good_ensemble' : None,
           'last_good_ensemble' : None,
           'magnetic_declination' : 0,
           'utc_offset' : None,
           'beam_dr': 0.1,
           'crp_rotation_angle' : 0,
           'crp_offset_x' : 0,
           'crp_offset_y' : -3,
           'crp_offset_z' : 0,
           'transect_shift_x': 0.0,
           'transect_shift_y': 0.0,
           'transect_shift_z': 0.0,
           'transect_shift_t': 0.0,
           'water_properties': water_properties,
           'sediment_properties':sediment_properties,
           'abs_params': abs_params,
           'ssc_params': ssc_params
           }
    
    adcp = DatasetADCP(cfg, name = name)
    adcps.append(adcp)
    
    break
    if i==1:
        break
adcp.plot.single_beam_flood_plot(beam=4,
                                field_name= "echo_intensity",
                                y_axis_mode = "bin",          # "depth", "bin", or "z"
                                cmap='jet',                            # str or Colormap; defaults to cmocean.thermal else "turbo"
                                vmin=None,
                                vmax=None,
                                n_time_ticks= 6,
                                title= None)
    
#%%
adcp.plot.platform_orientation()
adcp.plot.beam_geometry_animation()
adcp.plot.transect_animation(cmap = 'turbo',
                             save_gif = False,
                             show_beam_trail = False,
                             show_pos_trail = True, 
                             pos_trail_len = 200,)


adcp.plot.four_beam_flood_plot(field_name= "echo_intensity",
                                y_axis_mode= "bin",          
                                cmap='jet',                            
                                vmin= None,
                                vmax= None,
                                n_time_ticks= 6,
                                title= 'test')

adcp.plot.single_beam_flood_plot(beam=4,
                                field_name= "echo_intensity",
                                y_axis_mode = "depth",          # "depth", "bin", or "z"
                                cmap='jet',                            # str or Colormap; defaults to cmocean.thermal else "turbo"
                                vmin=None,
                                vmax=None,
                                n_time_ticks= 6,
                                title= 'test')
#%%
# Single-beam flood plot — standalone script (not a function)
# Requires an `adcp` object in scope and a target `beam` index (1..n_beams).
# Single-beam flood plot — standalone script (not a function)
# Requires an `adcp` object in scope and a target `beam` index (1..n_beams).

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

# -----------------
# CONFIG
# -----------------
beam = 1                              # 1..n_beams
field_name = "echo_intensity"         # beam_data field (time,bins,beams)
y_axis_mode = "bin"                  # "depth", "bin", or "z"
cmap = None                           # None → cmocean.thermal if available else "turbo"
vmin = None
vmax = None
n_time_ticks = 6
title = None                          # None → adcp.name

# Colormap default
if cmap is None:
    cmap = "turbo"

if not (1 <= int(beam) <= int(adcp.geometry.n_beams)):
    raise ValueError(f"beam must be in [1, {adcp.geometry.n_beams}]")
ib = int(beam) - 1

# Small fonts
plt.rcParams.update({
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

# ---------- Data ----------
t_dt = np.asarray(adcp.time.ensemble_datetimes)
t_num = mdates.date2num(t_dt).astype(float)
t0, t1 = float(t_num[0]), float(t_num[-1])

beam_data = ma.masked_invalid(adcp.get_beam_data(field_name=field_name, mask=True))  # (time,bins,beams)
data_tb = ma.masked_invalid(beam_data[:, :, ib])  # (time,bins)

bin_dist_m = np.asarray(adcp.geometry.bin_midpoint_distances, dtype=float)
z_rel = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, dtype=float)    # (time,bins,beams)
bt_range = np.asarray(adcp.bottom_track.range_to_seabed, dtype=float).T              # (time,beams)
invert_y = str(adcp.geometry.beam_facing).lower() == "down"

# Color limits from this beam only
if vmin is None or vmax is None:
    finite_vals = data_tb.compressed()
    if finite_vals.size == 0:
        raise ValueError("No finite data in selected field for this beam.")
    if vmin is None:
        vmin = float(np.nanmin(finite_vals))
    if vmax is None:
        vmax = float(np.nanmax(finite_vals))

units_map = {
    "echo_intensity": "Counts",
    "correlation_magnitude": "Counts",
    "percent_good": "%",
    "absolute_backscatter": "dB",
    "absolute backscatter": "dB",
    "alpha_s": "dB/km",
    "alpha_w": "dB/km",
    "signal_to_noise_ratio": "",
    "suspended_solids_concentration": "mg/L",
}

def pretty(s: str) -> str:
    return s.replace("_", " ").strip().capitalize()

# ---------- Y axis config ----------
ymode = (y_axis_mode or "depth").lower()
if ymode == "bin":
    # Bin 0 at TOP: normal extent then invert axis
    y_label = "Bin distance (m)"
    y0, y1 = float(bin_dist_m[0]), float(bin_dist_m[-1])
    do_invert = True
    bt_single = np.asarray(np.abs(bt_range[:, ib]), float)
elif ymode == "depth":

    # Depth positive downward; invert only for down-looking heads
    y_label = "Depth (m)"
    y0, y1 = float(bin_dist_m[0]), float(bin_dist_m[-1])
    do_invert = bool(invert_y)
    bt_single = np.asarray(np.abs(bt_range[:, ib]), float)
else:  # "z"
    y_label = "Mean z (m)"
    z_mean = np.nanmean(z_rel[:, :, ib], axis=0)
    if not np.isfinite(z_mean).any():
        z_mean = bin_dist_m
    y0, y1 = float(np.nanmin(z_mean)), float(np.nanmax(z_mean))
    do_invert = bool(invert_y)
    # Project range to z for each time
    bt_abs = np.asarray(np.abs(bt_range[:, ib]), float)
    bt_single = np.full(bt_abs.shape, np.nan, float)
    for it in range(len(t_num)):
        zi = z_rel[it, :, ib]
        if np.all(~np.isfinite(zi)):
            continue
        bt_single[it] = np.interp(bt_abs[it], bin_dist_m, zi)

# ---------- Layout ----------
fig = plt.figure(figsize=(8, 4.5))
gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[20, 0.6], wspace=0.05)
ax = fig.add_subplot(gs[0, 0])
ax_cbar = fig.add_subplot(gs[0, 1])

fig.suptitle(str(title) if title is not None else str(adcp.name), fontsize=9, fontweight="bold")

# Time ticks
xticks = np.linspace(t0, t1, n_time_ticks)

# Image
im = ax.matshow(
    data_tb.T,
    origin="lower",
    aspect="auto",
    extent=[t0, t1, y0, y1],
    vmin=vmin,
    vmax=vmax,
    cmap=cmap,
)

# Invert only when requested
if do_invert:
    ax.invert_yaxis()

# Bottom track line clipped to axis y-range
if np.isfinite(bt_single).any():
    bt_clipped = np.clip(bt_single, min(y0, y1), max(y0, y1))
    ax.plot(t_num, bt_clipped, color="k", linewidth=1)

# X axis formatting
ax.xaxis.set_ticks_position("bottom")
ax.xaxis.set_label_position("bottom")
ax.set_xticks(xticks)

lbls = []
for i, x in enumerate(xticks):
    dt = mdates.num2date(x)
    lbls.append(dt.strftime("%Y-%m-%d\n%H:%M:%S") if i in (0, len(xticks) - 1) else dt.strftime("%H:%M:%S"))
ax.set_xticklabels(lbls)
ax.set_xlabel("Time", fontsize=8)

# Y label and beam tag
ax.set_ylabel(y_label, fontsize=8)
ax.text(
    0.01,
    0.02,
    f"Beam {ib + 1}",
    transform=ax.transAxes,
    ha="left",
    va="bottom",
    fontsize=7,
    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9),
)

# Top distance axis aligned to time ticks
dist = np.asarray(adcp.position.distance, dtype=float)
idx = np.abs(t_num[:, None] - xticks[None, :]).argmin(axis=0)
dist_ticks = dist[idx]
ax_top = ax.twiny()
ax_top.set_xlim(t0, t1)
ax_top.set_xticks(xticks)
ax_top.set_xticklabels([f"{d:.0f}" for d in dist_ticks])
ax_top.set_xlabel("Distance along transect (m)", fontsize=8)
ax_top.tick_params(axis="x", labelsize=8)

# Colorbar
cblabel = f"{pretty(field_name)}" + (f" ({units_map.get(field_name, '')})" if units_map.get(field_name, "") else "")
cbar = fig.colorbar(im, cax=ax_cbar, orientation="vertical")
cbar.set_label(cblabel, fontsize=8)
cbar.ax.tick_params(labelsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()
