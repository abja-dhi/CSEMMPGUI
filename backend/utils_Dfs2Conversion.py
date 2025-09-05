# -*- coding: utf-8 -*-
"""
DFS2 -> DFSU with absolute E/N nodes and a minimal PyQt5 progress dialog.
"""

from mikecore.DfsFileFactory import DfsFileFactory
from mikecore.DfsuBuilder import DfsuBuilder, DfsuFileType
from mikecore.DfsFactory import DfsFactory
from mikecore.eum import eumQuantity, eumItem, eumUnit
import numpy as np
from datetime import datetime
import os

from pyproj import CRS, Transformer


# ---- CRS token mapper (handles WKT tokens like 'UTM-48') ----
def _crs_from_mike_projection(P) -> CRS:
    s = str(P.WKTString).strip().upper()
    if s.startswith("EPSG:"):
        return CRS.from_user_input(s)
    if s in ("LONG/LAT", "LAT/LONG", "GEOGRAPHIC", "WGS84"):
        return CRS.from_epsg(4326)
    if s.startswith("UTM-"):
        zone = int(s.split("-")[1])
        lat0 = float(getattr(P, "Latitude", np.nan))
        north = np.isnan(lat0) or (lat0 >= 0.0)
        return CRS.from_epsg((32600 if north else 32700) + zone)
    return CRS.from_wkt(P.WKTString)


# ---- Build absolute E/N nodes from DFS2 header (uses Orientation + optional geo anchor) ----
def en_nodes_from_dfs2(dfs2, prefer_geo_anchor=True):
    ax = dfs2.SpatialAxis
    nx, ny = int(ax.XCount), int(ax.YCount)
    dx, dy = float(ax.Dx), float(ax.Dy)
    x0, y0 = float(ax.X0), float(ax.Y0)
    theta = float(getattr(ax, "Orientation", 0.0))
    ct, st = np.cos(np.deg2rad(theta)), np.sin(np.deg2rad(theta))

    ii = np.arange(nx + 1, dtype=float)
    jj = np.arange(ny + 1, dtype=float)
    X = x0 + ii[None, :] * dx
    Y = y0 + jj[:, None] * dy
    dX, dY = X - x0, Y - y0

    E0, N0 = x0, y0  # default: local anchor

    P = dfs2.FileInfo.Projection
    if hasattr(P, "Longitude") and hasattr(P, "Latitude"):
        lon0, lat0 = float(P.Longitude), float(P.Latitude)
        crs = _crs_from_mike_projection(P)
        tr = Transformer.from_crs(CRS.from_epsg(4326), crs, always_xy=True)
        Eg, Ng = tr.transform(lon0, lat0)
        if prefer_geo_anchor or (abs(x0) < 1e-6 and abs(y0) < 1e-6):
            E0, N0 = Eg, Ng

    E = E0 + ct * dX - st * dY
    N = N0 + st * dX + ct * dY

    Xn = E.ravel(order="C").astype(np.float64)
    Yn = N.ravel(order="C").astype(np.float64)
    return Xn, Yn


# ---- Minimal PyQt5 progress dialog (no stdout, no threads) ----
class _QtProgress:
    def __init__(self, title="DFS2 → DFSU"):
        from PyQt5 import QtWidgets
        self.QtWidgets = QtWidgets
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.dlg = QtWidgets.QDialog()
        self.dlg.setWindowTitle(title)
        self.dlg.setModal(False)
        self.dlg.setFixedWidth(420)
        lay = QtWidgets.QVBoxLayout(self.dlg)
        self.label = QtWidgets.QLabel("Starting…")
        self.bar = QtWidgets.QProgressBar()
        self.bar.setRange(0, 100)
        self.btn = QtWidgets.QPushButton("Cancel")
        self.btn.setEnabled(False)  # wire later if you add cancellation
        lay.addWidget(self.label); lay.addWidget(self.bar); lay.addWidget(self.btn)
        self.dlg.show()
        self.app.processEvents()

    def update(self, pct: float, msg: str = ""):
        p = max(0, min(100, int(round(float(pct)))))
        self.bar.setValue(p)
        if msg:
            self.label.setText(str(msg))
        self.app.processEvents()

    def close(self):
        self.dlg.close()
        self.app.processEvents()


def Dfs2_to_Dfsu(in_path, out_path, *, show_qt_progress: bool = False):
    """Converts dfs2 to dfsu using mikecore. Optional PyQt progress dialog."""
    ui = _QtProgress() if show_qt_progress else None
    report = (ui.update if ui else (lambda *a, **k: None))

    # output prep
    if os.path.exists(out_path):
        os.remove(out_path)

    z_level = 0.0
    mask_with_nan = False
    item_for_mask = 1

    # open
    report(0, "Opening DFS2")
    dfs2 = DfsFileFactory.Dfs2FileOpen(str(in_path))

    # axis
    ax = dfs2.SpatialAxis
    nx = int(ax.XCount); ny = int(ax.YCount)
    dx = float(ax.Dx);   dy = float(ax.Dy)
    x0 = float(ax.X0);   y0 = float(ax.Y0)

    # items
    n_items = len(dfs2.ItemInfo)

    # time axis
    ta = dfs2.FileInfo.TimeAxis
    def _times_seconds(ta_obj):
        dt_attr = getattr(ta_obj, "TimeStep", None)
        n_attr = getattr(ta_obj, "NumberOfTimeSteps", None) or getattr(ta_obj, "Count", None)
        if (dt_attr is not None) and (n_attr is not None):
            n = int(n_attr); dt_s = float(dt_attr)
            return np.arange(n, dtype=float) * dt_s
        times = getattr(ta_obj, "Times", None)
        return np.asarray(list(times), dtype=float) if times is not None else np.array([0.0], float)

    start_time = getattr(ta, "StartDateTime", None)
    if not isinstance(start_time, datetime):
        start_time = datetime(2000, 1, 1)

    tsec = _times_seconds(ta).astype(float)
    n_steps = int(tsec.size) if tsec.size else 1
    if tsec.size == 0: tsec = np.array([0.0], dtype=float)
    dt_header = float(tsec[1] - tsec[0]) if n_steps > 1 else 1.0

    # nodes (absolute E/N)
    report(5, "Building nodes")
    Xn, Yn = en_nodes_from_dfs2(dfs2, prefer_geo_anchor=True)
    n_node = (ny + 1) * (nx + 1)
    Zn = np.full(n_node, z_level, dtype=np.float32)
    codes = np.ones(n_node, dtype=np.int32)

    # mask
    if mask_with_nan:
        report(8, "Reading mask")
        arr0 = np.asarray(dfs2.ReadItemTimeStep(item_for_mask, 0).Data, float)
        cell_valid = np.isfinite(arr0.reshape(ny, nx))
    else:
        cell_valid = np.ones((ny, nx), dtype=bool)

    # elements
    report(12, "Building elements")
    node_id = (np.arange(n_node).reshape(ny + 1, nx + 1) + 1).astype(np.int32)
    elements = []
    for j in range(ny):
        if ny and (j % max(1, ny // 50) == 0):
            report(12 + 8 * (j / max(1, ny-1)), f"Elements row {j+1}/{ny}")
        for i in range(nx):
            if not cell_valid[j, i]:
                continue
            n00 = node_id[j,     i    ]
            n10 = node_id[j,     i + 1]
            n11 = node_id[j + 1, i + 1]
            n01 = node_id[j + 1, i    ]
            elements.append(np.asarray([n00, n10, n11, n01], dtype=np.int32))
    if not elements:
        if ui: ui.close()
        return "No valid cells to convert."

    # projection
    P = dfs2.FileInfo.Projection
    proj = DfsFactory().CreateProjection(P.WKTString)

    # dfsu type
    two_d = None
    for m in DfsuFileType:
        if "2D" in m.name.upper() or "MESH2" in m.name.upper():
            two_d = m; break
    if two_d is None:
        if ui: ui.close()
        return "No 2D DfsuFileType found."

    # build file
    report(22, "Creating DFSU")
    builder = DfsuBuilder.Create(two_d)
    builder.SetNodes(Xn, Yn, Zn, codes)
    builder.SetElements(elements)
    builder.SetProjection(proj)
    builder.SetTimeInfo(start_time, float(dt_header))

    for k in range(n_items):
        info = dfs2.ItemInfo[k]
        qty = getattr(info, "Quantity", None) or eumQuantity.Create(eumItem.eumIGeneral, eumUnit.eumUunitUndefined)
        builder.AddDynamicItem(info.Name, qty)

    dfsu = builder.CreateFile(str(out_path))

    # stream data
    report(30, "Writing data")
    total_frames = max(1, n_steps * n_items)
    wrote = 0
    tick = max(1, total_frames // 65)  # map 30→98 %
    for it in range(n_steps):
        t_sec = float(tsec[it])
        for k in range(1, n_items + 1):
            vals = dfs2.ReadItemTimeStep(k, it).Data
            mask = vals == dfs2.FileInfo.DeleteValueFloat
            vals[mask] = dfsu.DeleteValueFloat
            elem_vals = vals.reshape(ny, nx).ravel(order="C").astype(np.float32, copy=False)
            dfsu.WriteItemTimeStepNext(t_sec, elem_vals)
            wrote += 1
            if (wrote % tick) == 0:
                pct = 30 + 68 * (wrote / total_frames)
                report(pct, f"Writing {wrote}/{total_frames}")

    report(98, "Finalizing")
    dfsu.Close()
    dfs2.Close()
    report(100, "Done")
    if ui: ui.close()
    return True



if __name__ == '__main__':
    in_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'
    out_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/test4.dfsu'

    Dfs2_to_Dfsu(in_path, out_path)
