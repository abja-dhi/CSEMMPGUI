
import sys
import os


# Add the project root (one level up from /tests/) to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend
from backend.pd0 import Pd0Decoder
from backend.adcp import ADCP as ADCPDataset
from backend._adcp_position import ADCPPosition
from backend.utils import Utils, CSVParser
from backend.plotting import PlottingShell

import matplotlib.pyplot as plt




#%% get a bunch of examaple data 


root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2024_survey_data\10. Oct\20241024_F3(E)'
#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2025_CESS_survey_data\5. Jul\20250725_CESS_CETUS'
#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2024_survey_data\10. Oct\20241003_F3(F)'

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
            

#%% Load a dataset

i = 4 # indicator variable for dataset selection

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
 
adcp = ADCPDataset(cfg, name = cfg['name'])
#adcps.append(adcp)
 


#%% example plots

report = adcp._pd0.instrument_summary()

# adcp.plot.platform_orientation()




# adcp.plot.four_beam_flood_plot(field_name= "suspended_solids_concentration",
#                                 y_axis_mode= "bin",          # 'bin' or 'depth'
#                                 cmap='viridis',                            
#                                 vmin= None,
#                                 vmax= None,
#                                 n_time_ticks= 6,
#                                 title= "Test", 
#                                 mask = True)



# adcp.plot.transect_velocities(bin_sel='mean',                 # int or "mean"
#                                 every_n=1,                   # subsample step
#                                 scale=0.005,                  # quiver scale (visual only), smaller = longer quiver lines
#                                 title=None,
#                                 cmap='jet',       
#                                 vmin=None,            # colormap min
#                                 vmax=None,            # colormap max
#                                 line_width=2.5,              # centerline width
#                                 line_alpha=0.9,              # centerline transparency
#                                 hist_bins=20)                # bins for inset histogram
# plt.show()
# quit()
  
# adcp.plot.single_beam_flood_plot(beam='mean', # int or 'mean'
#                                 field_name= "suspended_solids_concentration",
#                                 y_axis_mode = "bin",          # "depth", "bin"
#                                 cmap='jet',                  # str or Colormap; defaults to cmocean.thermal else "turbo"
#                                 vmin=None,
#                                 vmax=10,
#                                 n_time_ticks= 6, # number of time axis ticks and labels 
#                                 title= None, 
#                                 mask = True)




# adcp.plot.beam_geometry_animation()


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
plt.show()