
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


#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2025_CESS_survey_data\5. Jul\20250725_CESS_CETUS'


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
 
 
i = 0
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
    'water_properties': water_properties,
    'sediment_properties':sediment_properties,
    'abs_params': abs_params,
    'ssc_params': ssc_params,
    }
 
adcp = DatasetADCP(cfg, name = name)
adcps.append(adcp)
 


#%% 
adcp.plot.platform_orientation()




adcp.plot.four_beam_flood_plot(field_name= "percent_good",
                                y_axis_mode= "bin",          
                                cmap='jet',                            
                                vmin= None,
                                vmax= None,
                                n_time_ticks= 6,
                                title= None, 
                                mask = False)




adcp.plot.transect_velocities(bin_sel='mean',                 # int or "mean"
                                every_n=1,                   # subsample step
                                scale=0.005,                  # quiver scale (visual only)
                                title=None,
                                shared_cmap='jet',       # single cmap for line & quiver
                                shared_vmin=None,            # shared colormap min
                                shared_vmax=None,            # shared colormap max
                                line_width=2.5,              # centerline width
                                line_alpha=0.9,              # centerline transparency
                                hist_bins=20,                # bins for inset histogram
                                figsize=(5, 5)               # figure size
                            )

  
adcp.plot.single_beam_flood_plot(beam='mean', #
                                field_name= "suspended_solids_concentration",
                                y_axis_mode = "bin",          # "depth", "bin", or "z"
                                cmap='jet',                            # str or Colormap; defaults to cmocean.thermal else "turbo"
                                vmin=None,
                                vmax=10,
                                n_time_ticks= 6,
                                title= None, 
                                mask = True)




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
