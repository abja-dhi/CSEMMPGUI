
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


root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2025_CESS_survey_data\5. Jul\20250725_CESS_CETUS'


#Utils.extern_to_csv_batch(r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2025_CESS_survey_data\5. Jul')
#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2024_survey_data\10. Oct\20241003_F3(F)'
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

   
fpath = r'//usden1-stor.dhi.dk/Projects/41806287/41806287 NORI-D Data/Data/Fixed Stations/02_Fixed_Bottom_Current_Turbidity/02_FBCT2/01_ADCP_600kHz-24144/Raw/Full Duration/FBCT2000b.000'

pd0 = Pd0Decoder(fpath, cfg = {})

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



# for i,fpath in enumerate(pd0_fpaths):
# print(i)
 
 
i = 6
fpath = pd0_fpaths[i]
name = fpath.split(os.sep)[-1].split('.000')[0]
#fpath = r'//usden1-stor.dhi.dk/Projects/41806287/41806287 NORI-D Data/Data/Fixed Stations/02_Fixed_Bottom_Current_Turbidity/02_FBCT2/01_ADCP_600kHz-24144/Raw/Full Duration/FBCT2000b.000'

cfg = {'filename':fpath,
    'name':name,
    'pos_cfg':pos_cfgs[i],
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
    'water_properties': water_properties,
    'sediment_properties':sediment_properties,
    'abs_params': abs_params,
    'ssc_params': ssc_params
    }
 
adcp = DatasetADCP(cfg, name = name)
adcps.append(adcp)
 
print(f'max roll :{adcp.aux_sensor_data.roll.max()}')
print(f'max roll :{adcp.aux_sensor_data.pitch.max()}')
 
adcp.plot.velocity_flood_plot(field_name = 'speed', mask = True, cmap = 'jet')

#%%   
adcp.plot.single_beam_flood_plot(beam=4,
                                field_name= "suspended_solids_concentration",
                                y_axis_mode = "bin",          # "depth", "bin", or "z"
                                cmap='jet',                            # str or Colormap; defaults to cmocean.thermal else "turbo"
                                vmin=None,
                                vmax=10,
                                n_time_ticks= 6,
                                title= None)


adcp.plot.platform_orientation()


adcp.plot.beam_geometry_animation()



adcp.plot.transect_animation(cmap= 'jet',
                                    vmin= None,
                                    vmax= None,
                                    show_pos_trail = True,
                                    show_beam_trail = True,
                                    pos_trail_len= 200,
                                    beam_trail_len = 200,
                                    interval_ms= 10,
                                    save_gif = False,
                                    gif_name= None)


adcp.plot.four_beam_flood_plot(field_name= "percent_good",
                                y_axis_mode= "bin",          
                                cmap='jet',                            
                                vmin= None,
                                vmax= None,
                                n_time_ticks= 6,
                                title= None, 
                                mask = False)

adcp.plot.single_beam_flood_plot(beam=2,
                                field_name= "echo_intensity",
                                y_axis_mode = "bin",          # "depth", "bin", or "z"
                                cmap='turbo',                            # str or Colormap; defaults to cmocean.thermal else "turbo"
                                vmin=None,
                                vmax=None,
                                n_time_ticks= 6,
                                title= None, 
                                mask = True)





#%%

# u,v,z,ev = adcp._get_velocity(target_frame = 'earth')

# ubt,vbt,zbt,evbt = adcp._get_bt_velocity(target_frame = 'earth')





#%%
u = adcp.velocity.from_earth.u
v = adcp.velocity.from_earth.v
se = np.hypot(u,v)


u = adcp.velocity.from_ship.S
v = adcp.velocity.from_ship.F
ss = np.hypot(u,v)


u = adcp.velocity.from_instrument.x
v = adcp.velocity.from_instrument.y
si = np.hypot(u,v)

# u = adcp.velocity.from_beam.u
# v = adcp.velocity.from_beam.v
# sb = np.hypot(u,v)

#%%
# Feather plot + centerline colored by aggregated beam data.
# Updates: shared colormap (default 'jet'), bottom-left map-style scale bar of constant size using axis coordinates,
# quivers colored by beam data, bin aggregation applied consistently to velocity and beam data,
# `scale` passed to quiver.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib import patches as mpatches

# -----------------
# CONFIG
# -----------------
bin_sel    = 'mean'
every_n    = 1
scale      = 0.01
title      = None

field_name = "absolute_backscatter"
beam_sel   = "mean"
mask_data  = True
cmap       = plt.cm.get_cmap("jet")
vmin       = None
vmax       = None
line_width = 2.5
line_alpha = 0.9
add_cbar   = True

# -----------------
# DATA
# -----------------
u,v,z,ev,s,d = adcp.get_velocity_data(coord_sys = 'earth',mask = True)
# u = adcp.velocity.from_earth.u
# v = adcp.velocity.from_earth.v
x = np.asarray(adcp.position.x_local_m).ravel()
y = np.asarray(adcp.position.y_local_m).ravel()

if isinstance(bin_sel, (int, np.integer)):
    bni = int(bin_sel) - 1
    if bni < 0 or bni >= u.shape[1]:
        raise IndexError(f"bin_sel {bin_sel} out of range 1..{u.shape[1]}")
    u_b = np.asarray(u[:, bni]).ravel()
    v_b = np.asarray(v[:, bni]).ravel()
elif str(bin_sel).lower() in {"mean", "avg"}:
    u_b = np.nanmean(u, axis=1).ravel()
    v_b = np.nanmean(v, axis=1).ravel()
else:
    raise ValueError("bin_sel must be 'mean' or 1..n_bins")

n = min(x.size, y.size, u_b.size, v_b.size)
x, y, u_b, v_b = x[:n], y[:n], u_b[:n], v_b[:n]

S = None
if field_name is not None:
    D = adcp.get_beam_data(field_name=field_name, mask=mask_data)[:n, :, :]
    if isinstance(bin_sel, (int, np.integer)):
        D = D[:, bni, :]
    else:
        D = np.nanmean(D, axis=1)
    if isinstance(beam_sel, (int, np.integer)):
        bmi = int(beam_sel) - 1
        if bmi < 0 or bmi >= D.shape[1]:
            raise IndexError(f"beam_sel {beam_sel} out of range 1..{D.shape[1]}")
        S = D[:, bmi]
    elif str(beam_sel).lower() in {"mean", "avg"}:
        S = np.nanmean(D, axis=1)
    else:
        raise ValueError("beam_sel must be 'mean' or 1..n_beams")

valid = np.isfinite(x) & np.isfinite(y) & np.isfinite(u_b) & np.isfinite(v_b)
if S is not None: valid &= np.isfinite(S)
idx = np.nonzero(valid)[0][::max(1, int(every_n))]
if idx.size < 2: raise ValueError("Need ≥2 valid samples.")

X, Y = x[idx], y[idx]
U, V = u_b[idx], v_b[idx]
C = None if S is None else S[idx]

# -----------------
# PLOT
# -----------------
fig, ax = PlottingShell.subplots(figheight=5, figwidth=5)

if C is not None:
    norm = Normalize(vmin if vmin is not None else np.nanmin(C), vmax if vmax is not None else np.nanmax(C))
    pts  = np.column_stack([X, Y])
    segs = np.stack([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(segs, cmap=cmap, norm=norm, linewidths=line_width, alpha=line_alpha)
    lc.set_array(C[:-1])
    ax.add_collection(lc)

q = ax.quiver(X, Y, U, V, None if C is None else C,
              cmap=None if C is None else cmap,
              norm=None if C is None else norm,
              angles="xy", scale_units="xy", scale=scale,
              width=0.002, headwidth=3, headlength=4, pivot="tail")

if C is not None and add_cbar:
    cb = fig.colorbar(lc, ax=ax, shrink=0.85, pad=0.02)
    cb.set_label(field_name.replace("_", " "))

# -----------------
# CONSTANT-SIZE SPEED SCALEBAR (anchored in axes coords, bottom-left, labels above)
# -----------------
# Draw the bar in AXES coordinates so it stays in the lower-left regardless of data limits.
# The label values reflect the speed corresponding to the bar length via the quiver scale.

# fixed visual size as fraction of axes width/height
bar_width_axes = 0.25   # 25% of axes width
bar_height_axes = 0.025 # thin bar height
pad_x = 0.05            # left padding in axes coords
pad_y = 0.05            # bottom padding in axes coords

# compute equivalent data-length for labeling speeds
x0_data, x1_data = ax.get_xlim()
L_data = bar_width_axes * (x1_data - x0_data)
ref_speed = L_data * float(scale)

# bar geometry in axes coordinates
x0_ax = pad_x
y0_ax = pad_y

# two-tone rectangles
rect1 = mpatches.Rectangle((x0_ax, y0_ax), bar_width_axes/2, bar_height_axes,
                           transform=ax.transAxes, facecolor="k", edgecolor="k", clip_on=False)
rect2 = mpatches.Rectangle((x0_ax + bar_width_axes/2, y0_ax), bar_width_axes/2, bar_height_axes,
                           transform=ax.transAxes, facecolor="w", edgecolor="k", clip_on=False)
ax.add_patch(rect1)
ax.add_patch(rect2)

# tick marks at 0, mid, end
for dx in (0.0, bar_width_axes/2, bar_width_axes):
    ax.plot([x0_ax + dx, x0_ax + dx], [y0_ax, y0_ax + bar_height_axes],
            transform=ax.transAxes, color="k", lw=0.8, clip_on=False)

# labels above bar, small font
font_small = 6
ax.text(x0_ax, y0_ax + bar_height_axes*1.6, "0", transform=ax.transAxes,
        va="bottom", ha="center", fontsize=font_small, clip_on=False)
ax.text(x0_ax + bar_width_axes/2, y0_ax + bar_height_axes*1.6, f"{ref_speed/2:.2f}",
        transform=ax.transAxes, va="bottom", ha="center", fontsize=font_small, clip_on=False)
ax.text(x0_ax + bar_width_axes, y0_ax + bar_height_axes*1.6, f"{ref_speed:.2f}",
        transform=ax.transAxes, va="bottom", ha="center", fontsize=font_small, clip_on=False)
ax.text(x0_ax + bar_width_axes/2, y0_ax + bar_height_axes*3.2, "speed (m/s)",
        transform=ax.transAxes, va="bottom", ha="center", fontsize=font_small, clip_on=False)

ax.set_aspect("equal", adjustable="datalim")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title(title or f"{getattr(adcp,'name','ADCP')} — Feather plot, bin {bin_sel}")
ax.grid(True, alpha=0.3)

plt.show()

