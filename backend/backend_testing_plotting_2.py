# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 13:33:18 2025

@author: anba
"""

import pathlib

root = pathlib.Path(r".")  # change this path
total = 0
for path in root.rglob('*.py'):
    total += sum(1 for _ in open(path, 'r', encoding='utf-8'))
print(total)

#%%
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

#%% read in a project XML file 

xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
project = XMLUtils(xml_path)

adcp_cfgs = project.get_adcp_cfgs()
obs_cfgs = project.get_obs_cfgs()
ws_cfgs = project.get_ws_cfgs()



#%%

adcp_st = []
adcp_et = []
adcps = []
for cfg in adcp_cfgs:
    adcp = ADCPDataset(cfg, name = cfg['name'])
    adcp_st.append(adcp.time.ensemble_datetimes[0])
    adcp_et.append(adcp.time.ensemble_datetimes[-1])
    adcps.append(adcp)
    

#%%
from datetime import timedelta
tol = timedelta(seconds=0)  # adjust if you want slack at edges

# loop OBS and tag matching ADCP index
for cfg in obs_cfgs:
    cfg['ssc_params'] = {'A': 0, 'B': 1.2}
    obs = OBSDataset(cfg)
    # normalize OBS endpoints
    obs_st = pd.to_datetime(np.nanmin(obs.data.datetime), errors="coerce")
    obs_et = pd.to_datetime(np.nanmax(obs.data.datetime), errors="coerce")

    adcp_index = None
    for i, (s, e) in enumerate(zip(adcp_st, adcp_et)):
        if pd.isna(s) or pd.isna(e):
            continue
        if (obs_st >= s - tol) and (obs_et <= e + tol):
            adcp_index = i
            break
        
        
    cfg['adcp_index'] = adcp_index
    obs.plot.depth_profile(plot_field="ntu", use_spline=True, k=1)
    
    
    
    
    
    
    
    






