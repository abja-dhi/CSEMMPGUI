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
import sys
import os


# Add the project root (one level up from /tests/) to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend
from backend.pd0 import Pd0Decoder
from backend.adcp import ADCP as ADCPDataset
from backend.pd0 import Pd0Decoder as Pd0

from backend._adcp_position import ADCPPosition
from backend.utils import Utils, CSVParser
from backend.plotting import PlottingShell

from logging import root
import xml.etree.ElementTree as ET
from adcp import ADCP as ADCPDataset
from typing import List
from obs import OBS as OBSDataset
from watersample import WaterSample as WaterSampleDataset
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

from utils_xml import XMLUtils
from utils_dfsu2D import DfsuUtils2D
from utils_dfsu import DfsuUtils






#%% Load the model
model_fpath = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Model Files/MT20241002.dfsu'
model = DfsuUtils2D(model_fpath)


# #%% load ADCP transects
# xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
# project = XMLUtils(xml_path)
# survey_name = 'Survey 1'

# adcp_cfgs = project.get_survey_adcp_cfgs(survey_name)

# # load ADCP data
# adcps = []
# for cfg in adcp_cfgs:
#     adcp = ADCPDataset(cfg, name = cfg['name'])
#     adcps.append(adcp)
#     break


#%% load in CESS specific surveys 
#%% get a bunch of examaple data 


#root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2024_survey_data\10. Oct\20241024_F3(E)'
root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2025_CESS_survey_data\5. Jul\20250725_CESS_CETUS'
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

i = 3 # indicator variable for dataset selection

adcp_ssc = []
model_ssc = []
times = []
for i in range(len(pd0_fpaths)):
        
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
    
    ssc_params = {'A': 3, 'B':.049}
    
    
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
    
        
    #% extract transect
    #transect_raw = model.extract_transect(xq = adcp.position.x,yq = adcp.position.y, t = adcp.time.ensemble_datetimes, item_number = 1)
    transect = model.extract_transect_idw(xq = adcp.position.x,yq = adcp.position.y, t = adcp.time.ensemble_datetimes, item_number = 1)
    ssc_model = transect[0]*1000
    
    ssc_adcp= adcp.get_beam_data(field_name = 'suspended_solids_concentration', mask = True)
    ssc_adcp = np.nanmean(np.nanmean(ssc_adcp,axis = 1),axis = 1) # avearge adcp ssc for all bins and beams

    ssc_adcp = adcp.get_beam_series(field_name = 'suspended_solids_concentration',                       
                            mode = 'hab',
                            target = 5,
                            beam='mean',
                            agg='mean')
                                    
                                    

    times.append(adcp.time.ensemble_datetimes)
    model_ssc.append(ssc_model)
    adcp_ssc.append(ssc_adcp)
    print(i)
    adcp.plot.four_beam_flood_plot(y_axis_mode = 'depth')
    break
    
#%

fig,ax = PlottingShell.subplots(figheight = 5, figwidth = 7)


for i in range(len(pd0_fpaths)):
    
    label_model =None
    label_adcp = None
    if i == 0:
        label_model ='model'
        label_adcp = 'Depth-beam averaged ADCP'
    
    ax.plot(times[i],model_ssc[i], c = 'black', label = label_model)
    ax.plot(times[i],adcp_ssc[i], c = 'red', label = label_adcp)
    ax.legend()
    ax.set_ylabel('SSC (mg/L)')
    break
    
#%%
fig,ax = PlottingShell.subplots(figheight = 5, figwidth = 7)

ax.imshow(adcp.geometry.HAB_beam_midpoint_distances[:,:,0].T)
ax.set_aspect('auto')



