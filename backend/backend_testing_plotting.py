
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
    
 
    if i==1:
        break
    
# adcp._get_transformed_velocity(target_frame = 'ship')    
# fasd
    
##%% TO-DO 

#Handle velocity coordinate conversions for earth and ship, deal with units appropriately !!!!
#%%   
adcp.plot.single_beam_flood_plot(beam=4,
                                field_name= "echo_intensity",
                                y_axis_mode = "bin",          # "depth", "bin", or "z"
                                cmap='jet',                            # str or Colormap; defaults to cmocean.thermal else "turbo"
                                vmin=None,
                                vmax=None,
                                n_time_ticks= 6,
                                title= None)
    




adcp.plot.platform_orientation()


adcp.plot.beam_geometry_animation()



adcp.plot.transect_animation(cmap= 'jet',
                                    vmin= None,
                                    vmax= None,
                                    show_pos_trail = True,
                                    show_beam_trail = False,
                                    pos_trail_len= 200,
                                    beam_trail_len = 50,
                                    interval_ms= 10,
                                    save_gif = True,
                                    gif_name= None)


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

u,v,z,ev = adcp._get_velocity(target_frame = 'earth')

ubt,vbt,zbt,evbt = adcp._get_bt_velocity(target_frame = 'earth')

#%%
# #b1,b2,b3,b4 = 

# # fl = adcp._pd0.fixed_leaders
# # fl0 = fl[0]

# import numpy as np


# def beam_to_inst_coords(B):
    
#     beam_pattern = adcp._pd0.fixed_leaders[0].system_configuration.beam_pattern
#     beam_angle = int(adcp._pd0.fixed_leaders[0].system_configuration.beam_angle[:2])
    
#     c_ref = {'CONVEX':1,'CONCAVE':-1}
#     c = c_ref[beam_pattern]
    
#     a = 1/(2*np.sin(beam_angle*np.pi/180)) 
#     b = 1/(4*np.cos(beam_angle*np.pi/180)) 
#     d = a/ np.sqrt(2) 
    
#     M = np.array([
#         [  c*a, -c*a,  0.0,  0.0],   # X
#         [  0.0,  0.0, -c*a,  c*a],   # Y
#         [    b,    b,    b,    b],   # Z
#         [    d,    d,   -d,   -d],   # error velocity
#     ], dtype=float)
#     I = B @ M.T
#     return I


# def inst_to_earth(I, heading_deg, pitch_deg, roll_deg,
#                   declination_deg=0.0, heading_bias_deg=0.0, use_tilts=True):
#     """
#     Rotate instrument-frame velocities to Earth (ENU).

#     Parameters
#     ----------
#     I : ndarray, shape (T, K, 3)
#         Instrument velocities [X,Y,Z] in m/s for T ensembles and K bins.
#     heading_deg, pitch_deg, roll_deg : ndarray, shape (T,)
#         Timeseries of heading, pitch, roll in degrees.
#     declination_deg : float, optional
#         Magnetic declination added to heading.
#     heading_bias_deg : float, optional
#         Additional heading bias.
#     use_tilts : bool, optional
#         If False, set pitch=roll=0.

#     Returns
#     -------
#     E : ndarray, shape (T, K, 3)
#         Earth velocities [E,N,U] in m/s.
#     """
#     T = I.shape[0]
#     K = I.shape[1]
#     E = np.empty_like(I)

#     H = np.deg2rad(heading_deg + declination_deg + heading_bias_deg)
#     P = np.deg2rad(pitch_deg if use_tilts else 0.0)
#     R = np.deg2rad(roll_deg if use_tilts else 0.0)

#     CH, SH = np.cos(H), np.sin(H)
#     CP, SP = np.cos(P), np.sin(P)
#     CR, SR = np.cos(R), np.sin(R)

#     for t in range(T):
#         # Rotation matrix M_t (instrument XYZ → earth ENU), Eq. 18 (TRDI)
#         M_t = np.array([
#             [CH[t]*CR[t] + SH[t]*SP[t]*SR[t],  SH[t]*CP[t],  CH[t]*SR[t] - SH[t]*SP[t]*CR[t]],
#             [-SH[t]*CR[t] + CH[t]*SP[t]*SR[t], CH[t]*CP[t], -SH[t]*SR[t] - CH[t]*SP[t]*CR[t]],
#             [          -CP[t]*SR[t],                 SP[t],              CP[t]*CR[t]],
#         ], dtype=float)

#         # (K,3) @ (3,3) → (K,3)
#         E[t] = I[t] @ M_t.T

#     return E

# def inst_to_ship(I, pitch_deg, roll_deg, use_tilts=True):
#     """
#     Rotate instrument-frame velocities to Ship (SFU).

#     Parameters
#     ----------
#     I : ndarray, shape (T, K, 3)
#         Instrument velocities [X, Y, Z] in m/s.
#     pitch_deg, roll_deg : ndarray, shape (T,)
#         Pitch and roll time series in degrees.
#     use_tilts : bool, default True
#         If False, set pitch=roll=0.

#     Returns
#     -------
#     S : ndarray, shape (T, K, 3)
#         Ship velocities [Starboard, Forward, Up] in m/s.
#     """

#     T = I.shape[0]
#     K = I.shape[1]
#     S = np.empty_like(I)

#     P = np.deg2rad(pitch_deg if use_tilts else 0.0)
#     R = np.deg2rad(roll_deg if use_tilts else 0.0)
#     CP, SP = np.cos(P), np.sin(P)
#     CR, SR = np.cos(R), np.sin(R)

#     for t in range(T):
#         # H=0 ⇒ CH=1, SH=0. TRDI Eq. 18 reduced to ship frame.
#         M = np.array([
#             [CR[t],          0.0,        SR[t]],       # → Starboard
#             [SP[t]*SR[t],    CP[t],     -SP[t]*CR[t]], # → Forward
#             [-CP[t]*SR[t],   SP[t],      CP[t]*CR[t]], # → Up
#         ], dtype=float)

#         # (K,3) @ (3,3) → (K,3)
#         S[t] = I[t] @ M.T

#     return S




#%%
# B = adcp._get_bt_velocity()

# I = beam_to_inst_coords(B)


# ev = I[:,-1]
# I = I[:,:3]
# E = inst_to_earth(


# S = inst_to_ship(I,  pitch_deg, roll_deg, use_tilts=True)


#%%



#%%

# Feather plot using local-meter x_m, y_m with robust length alignment.

import numpy as np
import matplotlib.pyplot as plt

# -----------------
# CONFIG
# -----------------
bin_number = 15  # 1-based
every_n    = 1
scale      = 1
color      = None
title      = None

# -----------------
# DATA
# -----------------
ub,vb,zb,evb = adcp.velocity.from_


u = adcp.adcp.velocity.from_earth.u
v = adcp.adcp.velocity.from_earth.u
z = adcp.adcp.velocity.from_earth.u

#u, v, w, ev = adcp.adcp.velocity.from_earth.    # (time, bins)

x = np.asarray(adcp.position.x_local_m).ravel()   # (time,)
y = np.asarray(adcp.position.y_local_m).ravel()

u = u-ub[:,None]
v = v-vb[:,None]

bin_idx = int(bin_number) - 1
if bin_idx < 0 or bin_idx >= u.shape[1]:
    raise IndexError(f"bin_number {bin_number} out of range 1..{u.shape[1]}")

u_b = np.asarray(u[:, bin_idx]).ravel()
v_b = np.asarray(v[:, bin_idx]).ravel()

# align lengths
n = min(x.size, y.size, u_b.size, v_b.size)
x, y, u_b, v_b = x[:n], y[:n], u_b[:n], v_b[:n]

# global valid mask, then subsample with a shared index
valid = np.isfinite(x) & np.isfinite(y) & np.isfinite(u_b) & np.isfinite(v_b)
idx = np.nonzero(valid)[0][::max(1, int(every_n))]
if idx.size == 0:
    raise ValueError("No valid samples to plot after masking/subsampling.")

X, Y = x[idx], y[idx]
U, V = (u_b[idx] * scale), (v_b[idx] * scale)

# -----------------
# PLOT
# -----------------
fig, ax = PlottingShell.subplots(figheight=5, figwidth=5)
q = ax.quiver(X, Y, U, V, angles="xy", scale_units="xy", scale=.04,
              color=color, width=0.002, headwidth=3, headlength=4, pivot="tail")

spd = np.hypot(U, V)
ref = np.nanpercentile(spd, 75)
if np.isfinite(ref) and ref > 0:
    ax.quiverkey(q, 0.05, 0.95, ref, f"{ref:.2f} m/s", labelpos="E")

ax.set_aspect("equal", adjustable="datalim")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title(title or f"{getattr(adcp,'name','ADCP')} — Feather plot, bin {bin_number}")
ax.grid(True, alpha=0.3)

plt.show()

