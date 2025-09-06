# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 12:17:25 2025

@author: anba
"""
# import pathlib
# root = pathlib.Path(r".")  
# total = 0
# for path in root.rglob('*.py'):
#     total += sum(1 for _ in open(path, 'r', encoding='utf-8'))


#%%
import sys,os
# Class with params on the PLOT method, not on __init__.
# Simple continuous lines. No helpers called across methods.

import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from utils_dfsu2D_test import DfsuUtils2D
from utils_xml import XMLUtils
from adcp import ADCP as ADCPDataset
from utils_crs import CRSHelper
from plotting import PlottingShell
# # %% load from project file

# xml_path = r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj"
# survey_name = "Survey 1"
# project = XMLUtils(xml_path)
# adcp_cfgs = project.get_survey_adcp_cfgs(survey_name)

# # Provide SSC calibration defaults if your ADCP class expects them.
# ssc_params = {"A": 3, "B": 0.049}
# for cfg in adcp_cfgs:
#     cfg["ssc_params"] = ssc_params
#     cfg['velocity_average_window_len'] = 3
# adcps = [ADCPDataset(cfg, name=cfg.get("name")) for cfg in adcp_cfgs]

#%%

crs_helper = CRSHelper(project_crs = 4326)

#model_fpath = r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Model Files/MT20241002.dfsu"
model_fpath = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/test2.dfsu'
mt_model = DfsuUtils2D(model_fpath, crs_helper = crs_helper)  # provides extract_transect_idw(...)






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
 
    
adcp = adcps[0]
#%% extract an adcp transect 
xq = adcp.position.x
yq = adcp.position.y
t = adcp.time.ensemble_datetimes
item_number = 1
ssc = mt_model.extract_transect(xq, yq, t, item_number)


#%%
xc,yc = mt_model.get_centroids()
bbox = [xc.min(),
        xc.max(),
        yc.min(),
        yc.max()]


out = mt_model.rasterize_idw_bbox(item_number = 1,
                                        bbox = bbox, 
                                        t = adcp.time.ensemble_datetimes,
                                        pixel_size_m = 25)
data = out[0]
data[data<mt_model.dfsu.DeleteValueFloat] = np.nan


#%%
fig,ax = PlottingShell.subplots()

ax.scatter(xc,yc)
ax.set_aspect('equal')

#%%

fig,ax = PlottingShell.subplots()

xc,yc = mt_model.get_centroids()

# ax.scatter(xc,yc)
# ax.plot(xq,yq, c = 'red')

im = ax.imshow(data, extent = out[1], origin = 'lower')

for adcp in adcps:
    
    ax.plot(adcp.position.x,
            adcp.position.y)
fig.colorbar(im)