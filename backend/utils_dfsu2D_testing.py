# -*- coding: utf-8 -*-
# Full, clean script. Uses mikecore only for DFSU I/O.
# Compares three locators over a bbox ROI: TriFinder, SciPy Delaunay, Walking.

from mikecore.DfsuFile import DfsuFile
import numpy as np
from matplotlib.tri import Triangulation
from scipy.spatial import Delaunay
import time
import sys, os
from pathlib import Path
import pandas as pd  # only if you later want to dump results

# ---- project modules (adjust root if needed)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from utils_xml import XMLUtils
from adcp import ADCP as ADCPDataset

# ---------------- I/O helpers ----------------
def open_dfsu_2d(path):
    """Open a 2D triangular DFSU. Return (dfsu, x_nodes, y_nodes, et)."""
    dfsu = DfsuFile.Open(path)
    n_layers = int(getattr(dfsu, "NumberOfLayers", 0) or 0)
    if n_layers != 0:
        raise ValueError("Requires 2D DFSU (NumberOfLayers == 0).")
    x_nodes = np.asarray(dfsu.X, float)
    y_nodes = np.asarray(dfsu.Y, float)
    et = (np.stack(dfsu.ElementTable, axis=1).T - 1).astype(int)  # (n_elem, 3)
    if et.shape[1] != 3:
        raise ValueError("Mesh must be triangular (3 nodes per element).")
    return dfsu, x_nodes, y_nodes, et

def select_elements_in_bbox(x_nodes, y_nodes, et, xmin, xmax, ymin, ymax, mode="centroid"):
    """Return zero-based element indices inside bbox."""
    X = x_nodes[et]  # (n_elem, 3)
    Y = y_nodes[et]
    if mode == "centroid":
        cx = X.mean(axis=1); cy = Y.mean(axis=1)
        keep = (cx >= xmin) & (cx <= xmax) & (cy >= ymin) & (cy <= ymax)
    elif mode == "anynode":
        keep = ((X >= xmin) & (X <= xmax) & (Y >= ymin) & (Y <= ymax)).any(axis=1)
    else:
        raise ValueError("mode must be 'centroid' or 'anynode'.")
    idx = np.nonzero(keep)[0]
    if idx.size == 0:
        raise ValueError("No elements in bbox.")
    return idx

# ---------------- TriFinder over ROI ----------------
def build_locator_over_roi(x_nodes, y_nodes, et, elem_idx):
    """Triangulation+TriFinder over ROI only."""
    elem_idx = np.asarray(elem_idx, int)
    tri_keep = et[elem_idx]                  # (n_roi, 3) old node ids
    node_keep = np.unique(tri_keep.ravel())  # sorted old node ids

    old_to_new = -np.ones(x_nodes.size, int)
    old_to_new[node_keep] = np.arange(node_keep.size)

    et_roi = old_to_new[tri_keep]            # new contiguous node ids
    x_roi = x_nodes[node_keep]
    y_roi = y_nodes[node_keep]

    tri = Triangulation(x_roi, y_roi, et_roi)
    trifinder = tri.get_trifinder()
    return {"tri": tri, "trifinder": trifinder, "elem_map": elem_idx}

def locate_points_trifinder(locator, xq, yq):
    """Map query points to original element ids using TriFinder."""
    xq = np.asarray(xq, float).ravel()
    yq = np.asarray(yq, float).ravel()
    roi_elem = locator["trifinder"](xq, yq)    # ROI triangle ids or -1
    return np.where(roi_elem < 0, -1, locator["elem_map"][roi_elem])

# ---------------- Delaunay over ROI ----------------
def build_delaunay_locator_roi(x_nodes, y_nodes, et, elem_idx):
    """Delaunay on ROI nodes; map simplices -> original element ids."""
    elem_idx = np.asarray(elem_idx, int)
    tri_keep = et[elem_idx]
    node_keep = np.unique(tri_keep.ravel())
    old2new = -np.ones(x_nodes.size, int)
    old2new[node_keep] = np.arange(node_keep.size)

    et_roi = old2new[tri_keep]
    x_roi = x_nodes[node_keep]
    y_roi = y_nodes[node_keep]

    delau = Delaunay(np.column_stack([x_roi, y_roi]))

    key2eid = {tuple(sorted(t.tolist())): int(e) for t, e in zip(et_roi, elem_idx)}
    simp2eid = np.full(delau.simplices.shape[0], -1, int)
    for si, tri_nodes in enumerate(delau.simplices):
        simp2eid[si] = key2eid.get(tuple(sorted(tri_nodes.tolist())), -1)
    return delau, simp2eid

def locate_delaunay_roi(delau, simp2eid, xq, yq):
    """Map query points to original element ids using Delaunay.find_simplex."""
    P = np.column_stack([np.asarray(xq, float).ravel(), np.asarray(yq, float).ravel()])
    s = delau.find_simplex(P)  # -1 if outside hull
    return np.where(s >= 0, simp2eid[s], -1)

# ---------------- Walking locator over ROI ----------------
def build_adjacency_roi(et, elem_idx):
    """Adjacency among ROI elements only. Returns (nbr, tri_roi)."""
    from collections import defaultdict
    elem_idx = np.asarray(elem_idx, int)
    tri = et[elem_idx]  # ROI triangles in original node ids
    edge2tri = defaultdict(list)
    for rid, (a, b, c) in enumerate(tri):
        for u, v in ((a, b), (b, c), (c, a)):
            edge2tri[tuple(sorted((u, v)))].append(rid)
    nbr = -np.ones((tri.shape[0], 3), int)
    for rid, (a, b, c) in enumerate(tri):
        for k, (u, v) in enumerate(((a, b), (b, c), (c, a))):
            nb = edge2tri[tuple(sorted((u, v)))]
            if len(nb) == 2:
                nbr[rid, k] = nb[0] if nb[1] == rid else nb[1]
    return nbr, tri

def _inside_tri(px, py, ax, ay, bx, by, cx, cy):
    den = (cx - ax) * (by - ay) - (bx - ax) * (cy - ay)
    if den == 0.0:
        return False
    u = ((px - ax) * (by - ay) - (bx - ax) * (py - ay)) / den
    v = ((cx - ax) * (py - ay) - (px - ax) * (cy - ay)) / den
    return (u >= 0.0) and (v >= 0.0) and (u + v <= 1.0)

def locate_polyline_walk_roi(x_nodes, y_nodes, et, elem_idx, nbr, tri_roi, xq, yq, start_elem_roi):
    """Walk along ordered points; returns original element ids or -1."""
    X = x_nodes[tri_roi]  # (n_roi,3)
    Y = y_nodes[tri_roi]
    out = np.full(len(xq), -1, int)
    rid = int(start_elem_roi)
    for i, (px, py) in enumerate(zip(map(float, xq), map(float, yq))):
        for _ in range(64):
            ax, ay = X[rid, 0], Y[rid, 0]
            bx, by = X[rid, 1], Y[rid, 1]
            cx, cy = X[rid, 2], Y[rid, 2]
            if _inside_tri(px, py, ax, ay, bx, by, cx, cy):
                out[i] = int(elem_idx[rid])  # ROI id -> original element id
                break
            sAB = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
            sBC = (cx - bx) * (py - by) - (cy - by) * (px - bx)
            sCA = (ax - cx) * (py - cy) - (ay - cy) * (px - cx)
            k = int(np.argmin([sAB, sBC, sCA]))
            nxt = nbr[rid, k]
            if nxt < 0:
                break
            rid = int(nxt)
    return out

# ---------------- Load DFSU and ADCP path ----------------
# Edit these paths if needed
model_fpath = str(ROOT / "tests" / "Model Files" / "MT20241002.dfsu")
xml_path = str(ROOT / "tests" / "Real Project.mtproj")
survey_name = "Survey 1"

project = XMLUtils(xml_path)
adcp_cfgs = project.get_survey_adcp_cfgs(survey_name)

adcps = []
for cfg in adcp_cfgs[12:]:
    adcps.append(ADCPDataset(cfg, name=cfg["name"]))
    break
adcp = adcps[0]

# Query points (ordered transect)
xq = np.asarray(adcp.position.x, float).ravel()
yq = np.asarray(adcp.position.y, float).ravel()

#%% ---------------- Build ROI from ADCP bbox ----------------
import time

# ---- time file open and ROI build ----
t_open0 = time.perf_counter()
dfsu, x_nodes, y_nodes, et = open_dfsu_2d(model_fpath)
t_open = time.perf_counter() - t_open0

pad = 0.01
xq = np.asarray(adcp.position.x, float).ravel()
yq = np.asarray(adcp.position.y, float).ravel()
xmin = float(np.nanmin(xq)) - pad; xmax = float(np.nanmax(xq)) + pad
ymin = float(np.nanmin(yq)) - pad; ymax = float(np.nanmax(yq)) + pad

t_bbox0 = time.perf_counter()
elems = select_elements_in_bbox(x_nodes, y_nodes, et, xmin, xmax, ymin, ymax, mode="centroid")
t_bbox = time.perf_counter() - t_bbox0

# ---- TriFinder: BUILD vs LOCATE ----
t_tb0 = time.perf_counter()
loc = build_locator_over_roi(x_nodes, y_nodes, et, elems)     # Triangulation + get_trifinder
t_tri_build = time.perf_counter() - t_tb0

t_tl0 = time.perf_counter()
elem_tri = locate_points_trifinder(loc, xq, yq)
t_tri_loc = time.perf_counter() - t_tl0

# ---- Delaunay: BUILD vs LOCATE ----
t_db0 = time.perf_counter()
delau, simp2eid = build_delaunay_locator_roi(x_nodes, y_nodes, et, elems)
t_del_build = time.perf_counter() - t_db0

t_dl0 = time.perf_counter()
elem_del = locate_delaunay_roi(delau, simp2eid, xq, yq)
t_del_loc = time.perf_counter() - t_dl0

# ---- Walking: BUILD vs LOCATE ----
# seed start from TriFinder if available else Delaunay else first ROI element
if np.any(elem_tri >= 0):
    eid0 = int(elem_tri[np.flatnonzero(elem_tri >= 0)[0]])
elif np.any(elem_del >= 0):
    eid0 = int(elem_del[np.flatnonzero(elem_del >= 0)[0]])
else:
    eid0 = int(elems[0])
eid_to_rid = {int(e): i for i, e in enumerate(elems)}
start_rid = int(eid_to_rid.get(eid0, 0))

t_wb0 = time.perf_counter()
nbr, tri_roi = build_adjacency_roi(et, elems)
t_walk_build = time.perf_counter() - t_wb0

t_wl0 = time.perf_counter()
elem_walk = locate_polyline_walk_roi(x_nodes, y_nodes, et, elems, nbr, tri_roi, xq, yq, start_elem_roi=start_rid)
t_walk_loc = time.perf_counter() - t_wl0

# ---- report ----
n_pts = xq.size
print(f"OPEN dfsu: {t_open:.3f}s | BBOX select: {t_bbox:.3f}s")
print(f"TriFinder  BUILD: {t_tri_build:.3f}s | LOCATE {n_pts}: {t_tri_loc:.3f}s")
print(f"Delaunay   BUILD: {t_del_build:.3f}s | LOCATE {n_pts}: {t_del_loc:.3f}s")
print(f"Walking    BUILD: {t_walk_build:.3f}s | LOCATE {n_pts}: {t_walk_loc:.3f}s")

agree_td = np.sum((elem_tri >= 0) & (elem_del >= 0) & (elem_tri == elem_del))
agree_tw = np.sum((elem_tri >= 0) & (elem_walk >= 0) & (elem_tri == elem_walk))
agree_dw = np.sum((elem_del >= 0) & (elem_walk >= 0) & (elem_del == elem_walk))
print(f"Agree T vs D: {agree_td} | T vs W: {agree_tw} | D vs W: {agree_dw}")
print(f"Outside counts -> T:{(elem_tri<0).sum()} D:{(elem_del<0).sum()} W:{(elem_walk<0).sum()}")


#%%
import matplotlib.pyplot as plt

# precompute triangle vertices and centroids once on FULL mesh
Xtri = x_nodes[et]                # (n_elem, 3)
Ytri = y_nodes[et]
Cx   = Xtri.mean(axis=1)          # centroid x per element
Cy   = Ytri.mean(axis=1)

# per-method centroid at each query point
def centroids_for(elem_ids):
    inside = elem_ids >= 0
    cx = np.full(elem_ids.size, np.nan, float)
    cy = np.full(elem_ids.size, np.nan, float)
    cx[inside] = Cx[elem_ids[inside]]
    cy[inside] = Cy[elem_ids[inside]]
    return cx, cy, inside

cx_T, cy_T, in_T = centroids_for(elem_tri)
cx_D, cy_D, in_D = centroids_for(elem_del)
cx_W, cy_W, in_W = centroids_for(elem_walk)

agree_all = (elem_tri == elem_del) & (elem_tri == elem_walk) & (elem_tri >= 0)

plt.figure(figsize=(7,7))
# ADCP path
plt.plot(xq, yq, lw=1, alpha=0.5, label="ADCP path", color="0.7")

# centroids per method
plt.scatter(cx_T[in_T], cy_T[in_T], s=8, marker="o", label="TriFinder", alpha=0.8)
plt.scatter(cx_D[in_D], cy_D[in_D], s=8, marker="^", label="Delaunay", alpha=0.8)
plt.scatter(cx_W[in_W], cy_W[in_W], s=8, marker="s", label="Walking", alpha=0.8)

# highlight mismatches
mis = (~agree_all) & in_T & in_D & in_W
if np.any(mis):
    plt.scatter(cx_T[mis], cy_T[mis], s=30, facecolors="none", edgecolors="k", linewidths=1.0, label="Disagree")

plt.gca().set_aspect("equal", adjustable="box")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Locator centroid comparison")
plt.legend()
plt.tight_layout()
plt.show()
