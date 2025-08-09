
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
    if i==3:
        break

adcp.plot.platform_orientation()
adcp.plot.transect_animation(cmap = 'turbo',
                             save_gif = False,
                             show_beam_trail = False,
                             show_pos_trail = True, 
                             pos_trail_len = 200,)


adcp.plot.beam_geometry_animation()

#%% four beam flood plot 
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

# --- config ---
field = "echo_intensity"  # any attribute in adcp.beam_data
y_axis = "bin"            # "bin" or "z"
cmap = "turbo"            # default colormap
n_xticks = 6               # evenly spaced ticks from start to end

plt.rcParams.update({
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7
})

# --- data ---
t = np.asarray(adcp.time.ensemble_datetimes)
T = mdates.date2num(t).astype(float)
T0, T1 = float(T[0]), float(T[-1])

Aall = ma.masked_invalid(adcp.get_beam_data(field_name=field, mask=True))  # (time,bins,beams)
bins = np.asarray(adcp.geometry.bin_midpoint_distances, dtype=float)      # (bins,)
zrel = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, dtype=float)  # (time,bins,beams)

# Bottom track range to seabed (beams, time) -> (time, beams)
range_bt = np.asarray(adcp.bottom_track.range_to_seabed, dtype=float).T

# If plotting depth, make seabed negative
def convert_seabed_range(r):
    return -np.abs(r) if field.lower() == "depth" else r
range_bt = convert_seabed_range(range_bt)

invert_y = str(adcp.geometry.beam_facing).lower() == "down"

finite_vals = Aall.compressed()
if finite_vals.size == 0:
    raise ValueError("No finite data in selected field.")
vmin = float(np.nanmin(finite_vals))
vmax = float(np.nanmax(finite_vals))

_units = {
    "echo_intensity": "Counts",
    "correlation_magnitude": "Counts",
    "percent_good": "%",
    "absolute_backscatter": "dB",
    "absolute backscatter": "dB",
    "alpha_s": "dB/km",
    "alpha_w": "dB/km",
    "signal_to_noise_ratio": "",
    "suspended_solids_concentration": "",
    "depth": "m"
}

def pretty(name: str) -> str:
    return name.replace("_", " ").strip().capitalize()

ylabel = "Bin distance (m)" if y_axis == "bin" else "Mean z (m)"

# --- figure layout with colorbar column ---
fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(
    nrows=adcp.geometry.n_beams,
    ncols=2,
    width_ratios=[20, 1],
    wspace=0.05
)

axs = [fig.add_subplot(gs[i, 0]) for i in range(adcp.geometry.n_beams)]
cax = fig.add_subplot(gs[:, 1])  # colorbar axis spanning all rows

fig.supylabel(ylabel, fontsize=11)

# evenly spaced time ticks
xticks = np.linspace(T0, T1, n_xticks)

last_im = None
for b, axb in enumerate(axs):
    A = ma.masked_invalid(Aall[:, :, b])  # (time,bins)

    if y_axis == "bin":
        y0, y1 = float(bins[0]), float(bins[-1])
    else:
        z_mean = np.nanmean(zrel[:, :, b], axis=0)
        if not np.isfinite(z_mean).any():
            z_mean = bins
        y0, y1 = float(z_mean[0]), float(z_mean[-1])

    last_im = axb.matshow(
        A.T, origin="lower", aspect="auto",
        extent=[T0, T1, y0, y1],
        vmin=vmin, vmax=vmax, cmap=cmap
    )

    if invert_y:
        axb.invert_yaxis()

    # overlay bottom track range as line
    axb.plot(T, range_bt[:, b], color='k', linewidth=0.5)

    # move x-axis to bottom for all subplots
    axb.xaxis.set_ticks_position('bottom')
    axb.xaxis.set_label_position('bottom')
    axb.set_xticks(xticks)

    # hide tick labels except for bottom subplot
    if b != adcp.geometry.n_beams - 1:
        axb.tick_params(labelbottom=False)

# format tick labels on bottom subplot (first/last full date, middle mm:ss)
date_labels = []
for i, val in enumerate(xticks):
    dt = mdates.num2date(val)
    if i == 0 or i == len(xticks) - 1:
        date_labels.append(dt.strftime("%Y-%m-%d\n%H:%M:%S"))
    else:
        date_labels.append(dt.strftime("%M:%S"))
axs[-1].set_xticklabels(date_labels)
axs[-1].set_xlabel("Time", fontsize=9)

# --- single colorbar ---
units = _units.get(field, "")
cblabel = f"{pretty(field)}" + (f" ({units})" if units else "")
cb = fig.colorbar(last_im, cax=cax, orientation="vertical")
cb.set_label(cblabel, fontsize=9)
cb.ax.tick_params(labelsize=7)

# --- beam labels exactly on top edge of each subplot ---
fig.canvas.draw()  # ensure positions computed
for b, axb in enumerate(axs):
    bbox = axb.get_position()
    fig.text(
        bbox.x0,
        bbox.y1,
        f"Beam {b+1}",
        ha="left", va="bottom",
        fontsize=8
    )

plt.tight_layout()


#%%
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# # 3D animation of RELATIVE beam geometry across all ensembles

# # --- Data ---
# t = np.asarray(adcp.time.ensemble_datetimes)
# ens = np.asarray(adcp.time.ensemble_numbers)

# bx = np.asarray(adcp.geometry.relative_beam_midpoint_positions.x, dtype=float)  # (time, bins, beams)
# by = np.asarray(adcp.geometry.relative_beam_midpoint_positions.y, dtype=float)
# bz = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, dtype=float)

# if bx.ndim != 3 or by.ndim != 3 or bz.ndim != 3:
#     raise ValueError("relative_beam_midpoint_positions must be (time, bins, beams)")

# n_t, n_bins, n_beams = bx.shape

# # --- Figure/Axes ---
# fig, ax = PlottingShell.subplots3d(figheight=6, figwidth=7)
# ax.set_title(f"{adcp.name} — Relative Beam Geometry (3D)")
# ax.set_xlabel('Δx (m)')
# ax.set_ylabel('Δy (m)')
# ax.set_zlabel('Δz (m)')
# ax.set_box_aspect((1, 1, 1))

# # --- Global limits (symmetric around 0) ---
# finite = np.isfinite(bx) & np.isfinite(by) & np.isfinite(bz)
# if not np.any(finite):
#     raise ValueError("No finite beam midpoint coordinates to animate.")
# maxabs = max(np.nanmax(np.abs(bx[finite])), np.nanmax(np.abs(by[finite])), np.nanmax(np.abs(bz[finite])), 1e-9)
# L = 1.1 * maxabs
# ax.set_xlim(-L, L)
# ax.set_ylim(-L, L)
# ax.set_zlim(-L, L)

# # --- Artists ---
# colors = plt.rcParams['axes.prop_cycle'].by_key().get('color', ['C0','C1','C2','C3','C4','C5'])
# beam_lines = []
# head_markers = []  # first valid bin per beam (transducer end)
# for b in range(n_beams):
#     (ln,) = ax.plot([], [], [], '-', lw=2, color=colors[b % len(colors)], label=f'Beam {b+1}')
#     (mk,) = ax.plot([], [], [], 'o', ms=4, color=colors[b % len(colors)])
#     beam_lines.append(ln)
#     head_markers.append(mk)

# label = ax.text2D(0.02, 0.98, '', transform=ax.transAxes, ha='left', va='top', fontsize=9)
# ax.legend(loc='upper right', fontsize=8)

# # --- Helpers ---
# def _format_ts(ts):
#     try:
#         return ts.strftime('%Y-%m-%d %H:%M:%S')
#     except Exception:
#         import matplotlib.dates as mdates
#         return mdates.num2date(mdates.date2num(ts)).strftime('%Y-%m-%d %H:%M:%S')

# # --- Animation callbacks ---
# def init():
#     for ln, mk in zip(beam_lines, head_markers):
#         ln.set_data_3d([], [], [])
#         mk.set_data_3d([], [], [])
#     label.set_text('')
#     return (*beam_lines, *head_markers, label)


# def update(i):
#     for b, (ln, mk) in enumerate(zip(beam_lines, head_markers)):
#         xb = bx[i, :, b]
#         yb = by[i, :, b]
#         zb = bz[i, :, b]
#         m = np.isfinite(xb) & np.isfinite(yb) & np.isfinite(zb)
#         if np.any(m):
#             ln.set_data_3d(xb[m], yb[m], zb[m])
#             # first valid bin index
#             first_idx = np.argmax(m)
#             mk.set_data_3d([xb[first_idx]], [yb[first_idx]], [zb[first_idx]])
#         else:
#             ln.set_data_3d([], [], [])
#             mk.set_data_3d([], [], [])

#     label.set_text(f"{_format_ts(t[i])}  (#{int(ens[i])})")
#     return (*beam_lines, *head_markers, label)

# # --- Build & run ---
# ani = FuncAnimation(fig, update, frames=n_t, init_func=init, interval=50, blit=False)
# plt.show()

#%%
