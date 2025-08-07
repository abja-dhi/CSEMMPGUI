
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
           'crp_rotation_angle' : 0,
           'crp_offset_x' : 0.0,
           'crp_offset_y' : 0.0,
           'crp_offset_z' : 0.0,
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


#%%
import numpy as np 
fig, ax = PlottingShell.subplots(figheight = 3, figwidth = 6)
a = adcp.get_beam_data('absolute_backscatter', mask = True)
ax.imshow(a[:,:,0].T)
ax.set_aspect('auto', adjustable = 'box')

fig, ax = PlottingShell.subplots(figheight = 3, figwidth = 6)
m = adcp.masking.beam_data_mask
ax.imshow(m[:,:,0].T)
ax.set_aspect('auto', adjustable = 'box')

## To-Do
## SSC
## plotting
## beam plots, 
## beam geometry verification 
## correction for ADCP instrument pitch roll if beam 3 not forward. 
## bottom track velocity correction 



#%% generic testing for ADCP functions
import numpy as np

nc = adcp.geometry.n_bins
ne = adcp.time.n_ensembles


# define constant parameters
E_r = adcp.abs_params.E_r
WB = adcp.abs_params.WB
C = adcp.abs_params.C
k_c = adcp.abs_params.rssi
alpha_w = adcp.abs_params.alpha_w # water attenuation coefficient 
P_dbw = adcp.abs_params.P_dbw


bin_distances = adcp.geometry.bin_midpoint_distances
pulse_lengths = adcp.abs_params.tx_pulse_length
bin_depths = abs(adcp.geometry.geographic_beam_midpoint_positions.z)
instrument_freq = adcp.abs_params.frequency*1000 # in hz

temperature = adcp.water_properties.temperature
pressure = adcp.aux_sensor_data.pressure
salinity = adcp.water_properties.salinity
water_density = adcp.water_properties.density

particle_density = adcp.sediment_properties.particle_density
particle_diameter = adcp.sediment_properties.particle_diameter

pressure = np.outer(pressure, np.ones(nc))
salinity = salinity * np.ones((ne, nc))
water_density = water_density * np.ones((ne, nc))

pulse_lengths = np.outer(pulse_lengths, np.ones(nc))
bin_distances = np.outer(bin_distances, np.ones(ne)).T

print(f"temp shape: {temperature.shape}")
print(f"pressure shape: {pressure.shape}")
print(f"salinity shape: {salinity.shape}")
print(f"water_density shape: {water_density.shape}")
print(f"pulse_lengths shape: {pulse_lengths.shape}")
print(f"bin_distances shape: {bin_distances.shape}")


print(f"""\
Means:
------
E_r: {E_r}
WB: {WB}
C: {C}
k_c (mean over beams): {np.mean(list(k_c.values())):.4f}
alpha_w (mean): {np.mean(alpha_w):.6f}
P_dbw: {P_dbw}
instrument_freq: {instrument_freq} Hz
pulse_lengths (mean): {np.mean(pulse_lengths):.4f} m
bin_distances (mean): {np.mean(bin_distances):.4f} m
bin_depths (mean): {np.mean(bin_depths):.4f} m
temperature (mean): {np.mean(temperature):.4f} °C
pressure (mean): {np.mean(pressure):.4f} dbar
salinity (mean): {np.mean(salinity):.4f} PSU
water_density (mean): {np.mean(water_density):.4f} kg/m³
particle_density: {particle_density} kg/m³
particle_diameter: {particle_diameter} m
""")

echo = adcp.beam_data.echo_intensity
# ABS = np.zeros_like(Echo, dtype=float)
# SSC = np.zeros_like(Echo, dtype=float)
# alpha_s = np.zeros_like(Echo, dtype=float)

#%%
alpha_s = np.zeros(echo.shape, dtype=float)

for bm in range(adcp.geometry.n_beams):
    
    echo_beam = adcp.get_beam_data(field_name='echo_intensity', mask=False)[:, :, bm]
    abs_beam = adcp.get_beam_data(field_name='absolute_backscatter', mask=False)[:, :, bm]

    ssc_beam = adcp._backscatter_to_ssc(abs_beam)

    # --------- Iteratively update bin 0 ---------
    n_iter = 0
    max_iter = 100
    stop = False
    bn = 0
    while not stop and n_iter < max_iter:

        alpha_s_bm_bn = adcp._sediment_absorption_coeff(
            ps=particle_density,
            pw=water_density[:, bn],
            z=pressure[:, bn],
            d=particle_diameter,
            SSC=ssc_beam[:, bn],             # ✅ vector
            T=temperature[:, bn],
            S=salinity[:, bn],
            f=instrument_freq
        )

        sv, _ = adcp._counts_to_absolute_backscatter(
            E=echo_beam[:, bn],
            E_r=E_r,
            k_c=k_c[bm + 1],
            alpha=alpha_w[:, bn] + alpha_s_bm_bn,
            C=C,
            R=bin_distances[:, bn],
            Tx_T=temperature[:, bn],
            Tx_PL=pulse_lengths[:, bn],
            P_dbw=P_dbw
        )

        stop = np.allclose(abs_beam[:, bn], sv, rtol=1e-5, atol=1e-8)
        abs_beam[:, bn] = sv
        ssc_beam[:, bn] = adcp._backscatter_to_ssc(sv)
        n_iter += 1

    alpha_s[:, bn, bm] = alpha_s_bm_bn

    # --------- Propagate to deeper bins ---------
    for bn in range(1, adcp.geometry.n_bins - 1):

        # ✅ Vector of ensemble-wise mean SSC from above bins
        ssc_beam_column = np.nanmean(ssc_beam[:, :bn], axis=1)

        print(f'beam = {bm} | bin = {bn} | ssc mean = {np.nanmean(ssc_beam_column):.3f} mg/L')

        alpha_s_bm_bn = adcp._sediment_absorption_coeff(
            ps=particle_density,
            pw=water_density[:, bn],
            z=pressure[:, bn],
            d=particle_diameter,
            SSC=ssc_beam_column,              # ✅ vector
            T=temperature[:, bn],
            S=salinity[:, bn],
            f=instrument_freq
        )

        sv, _ = adcp._counts_to_absolute_backscatter(
            E=echo_beam[:, bn],
            E_r=E_r,
            k_c=k_c[bm + 1],
            alpha=alpha_w[:, bn] + alpha_s_bm_bn,
            C=C,
            R=bin_distances[:, bn],
            Tx_T=temperature[:, bn],
            Tx_PL=pulse_lengths[:, bn],
            P_dbw=P_dbw
        )

        abs_beam[:, bn] = sv
        ssc_beam[:, bn] = adcp._backscatter_to_ssc(sv)
        alpha_s[:, bn, bm] = alpha_s_bm_bn



fig, ax = PlottingShell.subplots(figheight = 3, figwidth = 6)
a = ssc_beam
ax.imshow(a.T, vmax = 10)
ax.set_aspect('auto', adjustable = 'box')   

fig, ax = PlottingShell.subplots(figheight = 3, figwidth = 6)
a = ssc_beam_init
ax.imshow(a.T, vmax = 10)
ax.set_aspect('auto', adjustable = 'box')  

fig, ax = PlottingShell.subplots(figheight = 3, figwidth = 6)
a = alpha_s[:,:,-1]
ax.imshow(a.T)
ax.set_aspect('auto', adjustable = 'box') 


# #%% Calculate an initial guess at SSC

# alpha_s = np.zeros(echo.shape,dtype = float)
# for bm in range(adcp.geometry.n_beams):
    
#     echo_beam = adcp.get_beam_data(field_name = 'echo_intensity', mask = False)[:,:,bm]
#     abs_beam = adcp.get_beam_data(field_name = 'absolute_backscatter', mask = False)[:,:,bm]
    
#     #abs_beam = adcp.get_beam_data(field_name = 'absolute_backscatter', mask = False)[:,:,bm] #.absolute_backscatter[:,:,beam]
#     ssc_beam = adcp._backscatter_to_ssc(abs_beam)
#     ssc_beam_init = ssc_beam.copy()
#     # iterate on soluton for alpha_s first bin
#     n_iter = 0
#     max_iter = 100
#     stop = False
#     while (not stop):
#         bn = 0
#         alpha_s_bm_bn = adcp._sediment_absorption_coeff(ps = particle_density,
#                                                 pw = water_density[:,bn],
#                                                 z = pressure[:,bn],
#                                                 d = particle_diameter,
#                                                 SSC = ssc_beam[:,bn],
#                                                 T = temperature[:,bn],
#                                                 S = salinity[:,bn],
#                                                 f = instrument_freq)
        
        
#         sv,_ = adcp._counts_to_absolute_backscatter(E = echo_beam[:,bn],
#                                                 E_r = E_r,
#                                                 k_c= k_c[bm+1],
#                                                 alpha = alpha_w[:,bn] + alpha_s_bm_bn,
#                                                 C = C,
#                                                 R = bin_distances[:,bn],
#                                                 Tx_T = temperature[:,bn],
#                                                 Tx_PL = pulse_lengths[:,bn],
#                                                 P_dbw = P_dbw)
  
#         # diff = abs(np.sum(abs_beam[:,bn]- sv))
#         # print(f'diff  = {diff} | iter = {n_iter} | beam = {bm}')
#         stop = np.allclose(abs_beam[:,bn], sv, rtol=1e-5, atol=1e-8)
#         abs_beam[:,bn] = sv
#         ssc_beam[:,bn] = adcp._backscatter_to_ssc(sv)
#         n_iter +=1
#     alpha_s[:,bn,bm] = alpha_s_bm_bn    
    

#     # for each bin, calculate alpha_s using SSC from bin above
#     for bn in range(1,adcp.geometry.n_bins-1):
#         if bn<2:
#             ssc_beam_column = ssc_beam[bn-1,bm]
#         else:
#             ssc_beam_column = np.nanmean(ssc_beam[:bn,bm])
            
            
#         print(f'beam = [{bm} | bin = {bn} | ssc mean = {ssc_beam_column}')
#         alpha_s_bm_bn = adcp._sediment_absorption_coeff(ps = particle_density,
#                                                 pw = water_density[:,bn],
#                                                 z = pressure[:,bn],
#                                                 d = particle_diameter,
#                                                 SSC = ssc_beam_column,
#                                                 T = temperature[:,bn],
#                                                 S = salinity[:,bn],
#                                                 f = instrument_freq)
        
#         sv,_ = adcp._counts_to_absolute_backscatter(E = echo_beam[:,bn],
#                                                 E_r = E_r,
#                                                 k_c= k_c[bm+1],
#                                                 alpha = alpha_w[:,bn] + alpha_s_bm_bn,
#                                                 C = C,
#                                                 R = bin_distances[:,bn],
#                                                 Tx_T = temperature[:,bn],
#                                                 Tx_PL = pulse_lengths[:,bn],
#                                                 P_dbw = P_dbw)
        
        
#         abs_beam[:,bn] = sv
#         ssc_beam[:,bn] = adcp._backscatter_to_ssc(sv)
#         alpha_s[:,bn,bm] = alpha_s_bm_bn 
        
   
    
 
    # abs_beam, stn_beam = adcp._counts_to_absolute_backscatter(E = echo_beam,
    #                                                           E_r = E_r,
    #                                                           k_c = k_c[beam],
    #                                                           alpha = ,
    #                                                           C,
    #                                                           R,
    #                                                           Tx_T,
    #                                                           Tx_PL,
    #                                                           P_dbw)
        
        
    #     E,
    #                                                           E_r,
    #                                                           float(k_c[i+1]),
    #                                                           alpha,
    #                                                           C,
    #                                                           bin_distances,
    #                                                           temperature,
    #                                                           transmit_pulse_length,
    #                                                           P_dbw)
    #     )
    # # calcualte absolute backscatter with alpha_s = 0
    
    
    





# #%
# for bm in range(adcp.geometry.n_beams):
#     for bn in range(adcp.geometry.n_bins):
#         if bn == 0:
#             ssc_beam_bin = adcp._backscatter_to_SSC(ABS)[:,bm,bn] #SSC for current beam and bin
            
#             for _ in range(100):
#                 print(i)
#                 print(ssc_beam_bin.max())
#                 alpha_s = adcp._sediment_absorption_coeff(
#                     ps=adcp.sediment_properties.particle_density,
#                     pw=water_density[bn],
#                     z=pressure[bn],
#                     d=adcp.sediment_properties.particle_diameter,
#                     SSC=ssc_beam_bin,#[bm, bn, :],
#                     T=temp[bn],
#                     S=salinity[bn],
#                     f=instrument_freq
#                 )
#                 sv, _ = adcp._counts_to_absolute_backscatter(
#                     E=E[bm, bn],
#                     E_r=E_r,
#                     k_c=k_c[bm + 1],
#                     alpha=alpha_w[bn] + alpha_s,
#                     C=C,
#                     R=bin_distances[bn],
#                     Tx_T=temp[bn],
#                     Tx_PL=pulse_lengths[bn],
#                     P_dbw=P_dbw
#                 )
#                 ssc_new = adcp._backscatter_to_SSC(sv)
#                 if np.allclose(ssc_new, ssc_beam_bin, rtol=0, atol=1e-6, equal_nan=True):
#                     print('broken')
#                     break
#                 ssc_beam_bin = ssc_new
                
#             ABS[:,bm, bn] = sv
#             print(ssc_beam_bin.shape)
#             SSC[:,bm, bn] = ssc_beam_bin
#             Alpha_s[:,bm, bn] = alpha_s
            
            
#         else:
#             ssc_beam_bin = np.nanmean(SSC[:,bm, :bn], axis=0)
#             alpha_s = adcp._sediment_absorption_coeff(
#                 ps=adcp.sediment_properties.particle_density,
#                 pw=water_density[bn],
#                 z=pressure[bn],
#                 d=adcp.sediment_properties.particle_diameter,
#                 SSC=ssc_beam_bin,
#                 T=temp[bn],
#                 S=salinity[bn],
#                 f=instrument_freq
#             )
#             sv, _ = adcp._counts_to_absolute_backscatter(
#                 E=E[bm, bn],
#                 E_r=E_r,
#                 k_c=k_c[bm + 1],
#                 alpha=alpha_w[bn] + alpha_s,
#                 C=C,
#                 R=bin_distances[bn],
#                 Tx_T=temp[bn],
#                 Tx_PL=pulse_lengths[bn],
#                 P_dbw=P_dbw
#             )
#             ABS[:,bm, bn] = sv
#             SSC[:,bm, bn] = adcp._backscatter_to_SSC(sv)
#             Alpha_s[:,bm, bn] = alpha_s









#%%
#def ADCP_instrument_summary():

#     pd0_fpath = r'\\SGSIN1-STOR\Projects\61801596\Working Documents\Data and Calculations\10_Field Survey\Sediment Flux\2022\10. Oct\20221003-TF(F)-Exp2\RawDataRT\20221003-TF(F)-001r.000'
    
#     pd0_fpath = r'Dive05_T3A_sn24156.000'
    
#     cfg = {
#     "progress_bar": "True",
#     "instrument_depth": 12.5,          # meters
#     "instrument_HAB": 2.0,             # height above bed, meters
#     "name": "ADCP_20221003_TF(F)",
#     "noise_floor": 39,
#     "absolute_backscatter_C": -149.14,
#     "absolute_backscatter_alpha": 0.178,
#     "absolute_backscatter_P_dbw": 9,
#     "rssi_beam_1": 0.3931,
#     "rssi_beam_2": 0.4145,
#     "rssi_beam_3": 0.4160,
#     "rssi_beam_4": 0.4129,
#     }
    
#     import numpy as np
#     pd0 = Pd0Decoder(pd0_fpath, cfg = cfg)

#     #fixed_leader = pd0._get_fixed_leader()[0]#.to_dict()
#     fixed_leader = pd0._fixed

#     datetimes = pd0._get_datetimes()
#     dt_diffs = np.diff(datetimes)
#     duration = datetimes[-1] - datetimes[0]
#     total_seconds = int(duration.total_seconds())
#     days, rem = divmod(total_seconds, 86400)
#     hours, rem = divmod(rem, 3600)
#     minutes, seconds = divmod(rem, 60)
    
#     out = {
#         "Ensemble Timing and General Metadata": {
#             'Number of Ensembles': pd0._n_ensembles,
#             'First Ensemble DateTime (UTC)': datetimes[0],
#             'Last Ensemble DateTime (UTC)': datetimes[-1],
#             'Duration (d:h:m:s)': f"{days}:{hours:02}:{minutes:02}:{seconds:02}",
#             'Mean Ensemble Duration (s)': round(np.nanmean(dt_diffs).total_seconds(), 3),
#             'Median Ensemble Duration (s)': round(np.nanmedian(dt_diffs).total_seconds(), 3),
#             'Minimum Ensemble Duration (s)': round(np.nanmin(dt_diffs).total_seconds(), 3),
#             'Maximum Ensemble Duration (s)': round(np.nanmax(dt_diffs).total_seconds(), 3),
#         },
    
    
#         "Beam Configuration and System Geometry": {
#             'Beam Facing': fixed_leader.system_configuration.beam_facing,
#             'Beam Pattern': fixed_leader.system_configuration.beam_pattern,
#             'Beam Angle (°)': fixed_leader.system_configuration.beam_angle,
#             'Beam Angle (Redundant °)': fixed_leader.beam_angle,
#             'Janus Config': fixed_leader.system_configuration.janus_config,
#             'Frequency': fixed_leader.system_configuration.frequency,
#         },
    
#         "Measurement Configuration and Resolution": {
#             'Number of Beams': fixed_leader.number_of_beams,
#             'Number of Cells': fixed_leader.number_of_cells_wn,
#             'Pings per Ensemble': fixed_leader.pings_per_ensemble_wp,
#             'Cell Size (cm)': fixed_leader.depth_cell_length_ws,
#             'Blank After Transmit (cm)': fixed_leader.blank_after_transmit_wf,
#             'Bin 1 Distance (cm)': fixed_leader.bin_1_distance,
#             'Lag Length': fixed_leader.lag_length,
#             'Transmit Lag Distance (cm)': fixed_leader.transmit_lag_distance,
#             'Transmit Pulse Length Based on Water Track': fixed_leader.xmit_pulse_length_based_on_wt,
#             'Ref Layer Start/End Cell': fixed_leader.starting_cell_wp_ref_layer_average_wl_ending_cell,
#         },
    
#         "Timing Parameters": {
#             'TPP Minutes': fixed_leader.tpp_minutes,
#             'TPP Seconds': fixed_leader.tpp_seconds,
#             'TPP Hundredths': fixed_leader.tpp_hundredths_tp,
#         },
    
#         "Quality Control and Filtering Thresholds": {
#             'Low Correlation Threshold': fixed_leader.low_corr_thresh_wc,
#             'Number of Code Repetitions': fixed_leader.no_code_reps,
#             'Minimum Good Data (%)': fixed_leader.gd_minimum_wg,
#             'Max Error Velocity Threshold (mm/s)': fixed_leader.error_velocity_maximum_we,
#             'False Target Threshold (dB)': fixed_leader.false_target_thresh_wa,
#         },
    
#         "Coordinate Transforms and Orientation": {
#             'Coordinate Transform Flags': fixed_leader.coordinate_transform_ex,
#             'Heading Alignment (°)': fixed_leader.heading_alignment_ea,
#             'Heading Bias (°)': fixed_leader.heading_bias_eb,
#         },
    
#         "Sensor and Source Configuration": {
#             'Sensor Source Flags': fixed_leader.sensor_source_ez,
#             'Sensors Available Flags': fixed_leader.sensors_available,
#         },
    
#         "Firmware and Hardware Metadata": {
#             'CPU Firmware Version': fixed_leader.cpu_fw_ver,
#             'CPU Firmware Revision': fixed_leader.cpu_fw_rev,
#             'CPU Board Serial Number': fixed_leader.cpu_board_serial_number,
#             'Instrument Serial Number': fixed_leader.instrument_serial_number,
#             'System Bandwidth (kHz)': fixed_leader.system_bandwidth_wb,
#             'System Power (W)': fixed_leader.system_power_cq,
#         },
    
#         "Flags and Placeholders": {
#             'Realsim Flag': fixed_leader.realsim_flag,
#             'Spare1': fixed_leader.spare1,
#             'Spare2': fixed_leader.spare2,
#         }
#     }

#     lines = []
#     for section, items in out.items():
#         lines.append(section.upper())
#         lines.append("=" * len(section))
    
#         max_key_len = max(len(key) for key in items)
#         for key, value in items.items():
#             padding = " " * 2
#             key_str = key.ljust(max_key_len + 4)
#             lines.append(f"{padding}{key_str}: {value}")
    
#         lines.append("")  # Blank line between sections
    
#     report = "\n".join(lines)
 
#     with open("adcp_summary.txt", "w", encoding="utf-8") as f:
#         f.write(report)
    
