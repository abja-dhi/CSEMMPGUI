# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 14:47:05 2025

@author: anba
"""
from mikecore.DfsFileFactory import DfsFileFactory
from mikecore.DfsuBuilder import DfsuBuilder, DfsuFileType
from mikecore.DfsFactory import DfsFactory
from mikecore.eum import eumQuantity, eumItem, eumUnit
import numpy as np
from pathlib import Path
from datetime import datetime
import time
import os



def Dfs2_to_Dfsu(in_path, out_path):
    
    ' converts dfs2 to dfsu using mikecore'
    
    # -------------------
    # config
    # -------------------
    #in_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'

    out_dfsu = out_path #Path(in_path).with_suffix(".dfsu")
    
    # # check if out file already exists and give warning if true
    if os.path.exists(out_dfsu): 
        os.remove(out_dfsu)


    
    z_level = 0.0                 # node Z
    mask_with_nan = False         # drop cells where chosen item at t=0 is NaN
    item_for_mask = 1             # 1-based item index for mask
    
    
    # -------------------
    # open DFS2
    # -------------------
    
    dfs2 = DfsFileFactory.Dfs2FileOpen(str(in_path))
    
    # spatial axis
    ax = dfs2.SpatialAxis
    nx = int(ax.XCount); ny = int(ax.YCount)
    dx = float(ax.Dx);   dy = float(ax.Dy)
    x0 = float(ax.X0);   y0 = float(ax.Y0)
    theta_deg = float(getattr(ax, "Orientation", 0.0))
    ct = np.cos(np.deg2rad(theta_deg)); st = np.sin(np.deg2rad(theta_deg))
    
    # items
    n_items = len(dfs2.ItemInfo)
    
    # -------------------
    # time axis (FileInfo.TimeAxis)
    # -------------------
    ta = dfs2.FileInfo.TimeAxis  # .NET temporal axis
    
    def _times_seconds(ta_obj):
        dt_attr = getattr(ta_obj, "TimeStep", None)
        n_attr = getattr(ta_obj, "NumberOfTimeSteps", None) or getattr(ta_obj, "Count", None)
        if (dt_attr is not None) and (n_attr is not None):
            n = int(n_attr)
            dt_s = float(dt_attr)
            return np.arange(n, dtype=float) * dt_s
        times = getattr(ta_obj, "Times", None)  # seconds since start if present
        if times is not None:
            return np.asarray(list(times), dtype=float)
        # fallback: probe by reads
        t = []
        it = 0
        while True:
            try:
                dfs2.ReadItemTimeStep(1, it)
                t.append(float(it))
                it += 1
            except: break
        return np.asarray(t, dtype=float)
    
    start_time = getattr(ta, "StartDateTime", None)
    if not isinstance(start_time, datetime):
        start_time = datetime(2000, 1, 1)
    
    tsec = _times_seconds(ta).astype(float)
    n_steps = int(tsec.size) if tsec.size else 1
    if tsec.size == 0:
        tsec = np.array([0.0], dtype=float)
    dt_header = float(tsec[1] - tsec[0]) if n_steps > 1 else 1.0
    
    # -------------------
    # nodes (corner grid) with rotation about (x0,y0)
    # -------------------
    
    ii = np.arange(nx + 1, dtype=float)
    jj = np.arange(ny + 1, dtype=float)
    X = x0 + ii[None, :] * dx
    Y = y0 + jj[:, None] * dy
    Xr = x0 + ct * (X - x0) - st * (Y - y0)
    Yr = y0 + st * (X - x0) + ct * (Y - y0)
    
    node_id = (np.arange((ny + 1) * (nx + 1)).reshape(ny + 1, nx + 1) + 1).astype(np.int32)
    
    # -------------------
    # optional mask from data t=0
    # -------------------
    if mask_with_nan:
        log("read frame for mask t=0")
        arr0 = np.asarray(dfs2.ReadItemTimeStep(item_for_mask, 0).Data, float)
        cell_valid = np.isfinite(arr0.reshape(ny, nx))
    else:
        cell_valid = np.ones((ny, nx), dtype=bool)
    
    flat_valid = cell_valid.ravel(order="C")
    idx_valid = np.flatnonzero(flat_valid)
    
    # -------------------
    # elements as quads [n1,n2,n3,n4] CCW, 1-based indices
    # -------------------
    
    elements = []
    rows_report = max(1, ny // 20)
    for j in range(ny):

        for i in range(nx):
            if not cell_valid[j, i]:
                continue
            n00 = node_id[j,     i    ]
            n10 = node_id[j,     i + 1]
            n11 = node_id[j + 1, i + 1]
            n01 = node_id[j + 1, i    ]
            elements.append(np.asarray([n00, n10, n11, n01], dtype=np.int32))
    
    n_elem = len(elements)
    n_node = (ny + 1) * (nx + 1)
    if n_elem == 0:
        return "No valid cells to convert."
    
    # -------------------
    # flatten nodes
    # -------------------
    Xn = Xr.ravel(order="C").astype(np.float64)
    Yn = Yr.ravel(order="C").astype(np.float64)
    Zn = np.full(n_node, z_level, dtype=np.float32)
    codes = np.ones(n_node, dtype=np.int32)  # 1 = water
    
    # -------------------
    # projection
    # -------------------
    proj_str = dfs2.FileInfo.Projection.WKTString
    proj = DfsFactory().CreateProjection(proj_str)
    
    # pick 2D dfsu enum member
    two_d = None
    for m in DfsuFileType:
        if "2D" in m.name.upper() or "MESH2" in m.name.upper():
            two_d = m; break
    if two_d is None:
        for name in ("Dfsu2D", "Mesh2D", "Type2D", "TwoD"):
            try:
                two_d = getattr(DfsuFileType, name); break
            except: 
                return 'Not a Dfs2 file'
    if two_d is None:
        return "No 2D DfsuFileType found."
    
    # -------------------
    # build DFSU (clone item schema)
    # -------------------
    builder = DfsuBuilder.Create(two_d)
    builder.SetNodes(Xn, Yn, Zn, codes)
    builder.SetElements(elements)
    builder.SetProjection(proj)
    builder.SetTimeInfo(start_time, float(dt_header))
    #builder.DeleteValueFloat = -1e30

    # find all items in the dfs2
    for k in range(n_items):
        info = dfs2.ItemInfo[k]
        name = getattr(info, "Name", f"item{k+1}")
        qty = getattr(info, "Quantity", None)
        if qty is None:
            qty = eumQuantity.Create(eumItem.eumIGeneral, eumUnit.eumUunitUndefined)
        builder.AddDynamicItem(name, qty)
        
    dfsu = builder.CreateFile(str(out_dfsu))
    # -------------------
    # stream data
    # ------------------
    for it in range(n_steps):
        t_sec = float(tsec[it])
        for k in range(1, n_items + 1):  # 1-based
            vals = dfs2.ReadItemTimeStep(k, it).Data  # len nx*ny
            mask = vals == dfs2.FileInfo.DeleteValueFloat
            vals[mask] = dfsu.DeleteValueFloat
            elem_vals = vals.reshape(ny, nx).ravel(order="C").astype(np.float32, copy=False)
            dfsu.WriteItemTimeStepNext(t_sec, elem_vals)
    dfsu.Close()
    dfs2.Close()
    
    return True

if __name__ == '__main__':
    in_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'
    out_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/test2.dfsu'
    
    Dfs2_to_Dfsu(in_path,out_path)