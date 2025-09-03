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

#%% read in a project XML file 

xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
project = XMLUtils(xml_path)
survey_name = 'Survey 1'


adcp_cfgs = project.get_survey_adcp_cfgs(survey_name)
obs_cfgs = project.get_survey_obs_cfgs(survey_name)
ws_elems  = project.get_survey_ws_elems("Survey 2")


# load ADCP data
adcps = []
for cfg in adcp_cfgs:
    adcp = ADCPDataset(cfg, name = cfg['name'])
    adcps.append(adcp)
    
    
    
#%%
# 3D curtain plots from existing ADCP objects in `adcps`
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ---- CONFIG ----
field_name   = "absolute_backscatter"   # any beam-data field
beam_sel     = "mean"                   # "mean" or 1..n_beams
z_mode       = "depth"                  # "depth" or "hab"
cmap_name    = "viridis"
alpha        = 0.9
linewidth    = 0.0
antialiased  = False
shared_scale = True
vmin, vmax   = None, None

def adcp_to_curtain(adcp, field_name, beam_sel="mean", z_mode="depth", mask=True):
    """Return x,y,z_bins, V(time,bin) for one ADCP."""
    # along-track coordinates (time,)
    x = np.asarray(adcp.position.x_local_m).ravel()
    y = np.asarray(adcp.position.y_local_m).ravel()

    # vertical coordinates: prefer velocity z (time,bin) or (bin,)
    z_raw = getattr(adcp.velocity.from_earth, "z", None)
    if z_raw is None:
        raise ValueError(f"{getattr(adcp,'name','ADCP')}: missing velocity z.")
    z_raw = np.asarray(z_raw)
    z_bins = np.nanmedian(z_raw, axis=0) if z_raw.ndim == 2 else z_raw.ravel()

    # data (time,bin,beam) -> (time,bin)
    D = adcp.get_beam_data(field_name=field_name, mask=mask)  # (t,b,beam)
    if D.ndim != 3:
        raise ValueError(f"{adcp.name}: expected (time,bin,beam), got {D.shape}.")
    if isinstance(beam_sel, (int, np.integer)):
        bi = int(beam_sel) - 1
        if bi < 0 or bi >= D.shape[2]:
            raise IndexError(f"{adcp.name}: beam_sel out of range 1..{D.shape[2]}")
        V = D[:, :, bi]
    elif str(beam_sel).lower() in {"mean", "avg"}:
        V = np.nanmean(D, axis=2)
    else:
        raise ValueError("beam_sel must be 'mean' or 1..n_beams")

    # align lengths
    n = min(x.size, y.size, V.shape[0])
    x, y, V = x[:n], y[:n], V[:n, :]
    z_bins = z_bins[:V.shape[1]]

    # z orientation
    if z_mode == "depth":
        Zsign = -1.0  # plot downward
        z_plot = z_bins * Zsign
        z_label = "Depth (m)"
    elif z_mode == "hab":
        z_plot = (np.nanmax(z_bins) - z_bins)  # 0 at bed, +up
        Zsign = +1.0
        z_label = "HAB (m)"
    else:
        raise ValueError("z_mode must be 'depth' or 'hab'")

    return x, y, z_plot, V, z_label

# ---- COLLECT CURTAINS ----
curtains = []
for adcp in adcps:
    x, y, z_plot, V, z_label = adcp_to_curtain(adcp, field_name, beam_sel, z_mode, mask=True)
    curtains.append({"name": getattr(adcp, "name", "ADCP"),
                     "x": x, "y": y, "z": z_plot, "V": V})

# ---- COLOR SCALING ----
cmap = cm.get_cmap(cmap_name)
if shared_scale:
    arr = np.concatenate([c["V"].ravel() for c in curtains])
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        raise ValueError("No finite values to color.")
    vmin_eff = np.nanmin(arr) if vmin is None else vmin
    vmax_eff = np.nanmax(arr) if vmax is None else vmax
else:
    vmin_eff, vmax_eff = vmin, vmax
norm = colors.Normalize(vmin=vmin_eff, vmax=vmax_eff)

# ---- PLOT ----
fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(111, projection="3d")

for c in curtains:
    x, y, z1d, V = c["x"], c["y"], c["z"], c["V"]
    # grids (M bins, N samples)
    X = np.tile(x, (z1d.size, 1))
    Y = np.tile(y, (z1d.size, 1))
    Z = np.tile(z1d[:, None], (1, x.size))
    C = V.T  # (M,N)

    # masks and colors
    Zm = np.ma.masked_invalid(Z)
    Cm = np.ma.masked_invalid(C)
    facecolors = cmap(norm(Cm))

    ax.plot_surface(X, Y, Zm,
                    facecolors=facecolors,
                    rstride=1, cstride=1,
                    linewidth=linewidth,
                    antialiased=antialiased,
                    shade=False,
                    alpha=alpha)

mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])
cb = fig.colorbar(mappable, ax=ax, shrink=0.85, pad=0.02)
cb.set_label(field_name.replace("_", " "))

ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel(z_label)
ax.view_init(elev=22, azim=-60)
plt.tight_layout()
plt.show()
