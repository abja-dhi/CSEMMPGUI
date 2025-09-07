# -*- coding: utf-8 -*-
"""
DFS2 -> DFSU with absolute E/N nodes, topmost PyQt5 progress dialog, Cancel support,
and progress bar suffix showing input/output filenames.
On cancel: closes files and removes partially written DFSU.
"""

from mikecore.DfsFileFactory import DfsFileFactory
from mikecore.DfsuBuilder import DfsuBuilder, DfsuFileType
from mikecore.DfsFactory import DfsFactory
from mikecore.eum import eumQuantity, eumItem, eumUnit
import numpy as np
from datetime import datetime
import os
from pyproj import CRS, Transformer


# -----------------------------
# CRS helpers
# -----------------------------
def _crs_from_mike_projection(P) -> CRS:
    """Map MIKE projection tokens to pyproj CRS."""
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


# -----------------------------
# Node generation
# -----------------------------
def en_nodes_from_dfs2(dfs2, prefer_geo_anchor=True):
    """
    Build absolute Easting/Northing nodes from DFS2 header.
    Uses axis Orientation and optional geographic anchor.
    """
    ax = dfs2.SpatialAxis
    nx, ny = int(ax.XCount), int(ax.YCount)
    dx, dy = float(ax.Dx), float(ax.Dy)
    x0, y0 = float(ax.X0), float(ax.Y0)
    theta = float(getattr(dfs2.FileInfo.Projection, "Orientation", 0.0))
    ct, st = np.cos(np.deg2rad(theta)), np.sin(np.deg2rad(theta))

    ii = np.arange(nx + 1, dtype=float)
    jj = np.arange(ny + 1, dtype=float)
    X = x0 + ii[None, :] * dx
    Y = y0 + jj[:, None] * dy
    dX, dY = X - x0, Y - y0

    E0, N0 = x0, y0  # default local anchor

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


# -----------------------------
# Progress dialog with Cancel and suffix
# -----------------------------
class _QtProgress:
    """Topmost non-modal dialog with percent bar, details, Cancel, and suffix text."""
    def __init__(self, title="DFS2 → DFSU"):
        from PyQt5 import QtWidgets, QtCore
        self.QtWidgets, self.QtCore = QtWidgets, QtCore
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.cancelled = False
        self.suffix = ""

        self.dlg = QtWidgets.QDialog()
        self.dlg.setWindowTitle(title)
        self.dlg.setModal(False)
        self.dlg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        self.dlg.setFixedWidth(540)

        lay = QtWidgets.QVBoxLayout(self.dlg)
        self.label = QtWidgets.QLabel("Starting…")
        self.detail = QtWidgets.QLabel("")
        self.detail.setStyleSheet("color:#555;")
        self.bar = QtWidgets.QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setFormat("%p%")

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        self.btn_cancel = QtWidgets.QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self._on_cancel)
        btn_row.addWidget(self.btn_cancel)

        lay.addWidget(self.label)
        lay.addWidget(self.detail)
        lay.addWidget(self.bar)
        lay.addLayout(btn_row)

        self.dlg.show()
        self.dlg.raise_()
        self.dlg.activateWindow()
        self.app.processEvents(self.QtCore.QEventLoop.AllEvents)

    def set_suffix(self, text: str):
        self.suffix = f" {text}" if text else ""

    def _on_cancel(self):
        self.cancelled = True

    def update(self, pct: float, msg: str = "", detail: str = ""):
        p = max(0, min(100, int(round(float(pct)))))
        self.bar.setValue(p)

        fmt = "%p%"
        if msg:
            self.label.setText(str(msg))
            fmt = f"%p% — {msg}"
        if self.suffix:
            fmt = f"{fmt}{self.suffix}"
        self.bar.setFormat(fmt)

        if detail:
            self.detail.setText(str(detail))

        self.dlg.raise_()
        self.dlg.activateWindow()
        self.app.processEvents(self.QtCore.QEventLoop.AllEvents)

    def close(self):
        self.dlg.close()
        self.app.processEvents()


# -----------------------------
# Converter
# -----------------------------
def Dfs2_to_Dfsu(in_path, out_path, *, show_qt_progress: bool = True):
    """
    Convert DFS2 to 2D DFSU. Supports Cancel mid-write.
    On cancel, closes files and deletes partial output.
    Returns True on success, "Cancelled by user" if cancelled, or error string.
    """
    ui = _QtProgress() if show_qt_progress else None
    if ui:
        from os.path import basename
        ui.set_suffix(f"[{basename(in_path)} → {basename(out_path)}]")
    report = (ui.update if ui else (lambda *a, **k: None))

    def _maybe_cancel():
        if ui and ui.cancelled:
            raise KeyboardInterrupt("User cancelled")

    dfs2 = None
    dfsu = None
    created_out = False

    try:
        # Output prep
        if os.path.exists(out_path):
            try:
                os.remove(out_path)
            except OSError:
                if ui:
                    ui.close()
                return f"Cannot remove existing file: {out_path}"

        # Open DFS2
        report(0, "Opening DFS2", os.path.basename(in_path))
        _maybe_cancel()
        dfs2 = DfsFileFactory.Dfs2FileOpen(str(in_path))

        # Axis
        ax = dfs2.SpatialAxis
        nx = int(ax.XCount)
        ny = int(ax.YCount)
        dx = float(ax.Dx)
        dy = float(ax.Dy)
        x0 = float(ax.X0)
        y0 = float(ax.Y0)

        # Items
        n_items = len(dfs2.ItemInfo)

        # Time axis → seconds array
        ta = dfs2.FileInfo.TimeAxis

        def _times_seconds(ta_obj):
            dt_attr = getattr(ta_obj, "TimeStep", None)
            n_attr = getattr(ta_obj, "NumberOfTimeSteps", None) or getattr(ta_obj, "Count", None)
            if (dt_attr is not None) and (n_attr is not None):
                n = int(n_attr)
                dt_s = float(dt_attr)
                return np.arange(n, dtype=float) * dt_s
            times = getattr(ta_obj, "Times", None)
            return np.asarray(list(times), dtype=float) if times is not None else np.array([0.0], float)

        start_time = getattr(ta, "StartDateTime", None)
        if not isinstance(start_time, datetime):
            start_time = datetime(2000, 1, 1)

        tsec = _times_seconds(ta).astype(float)
        n_steps = int(tsec.size) if tsec.size else 1
        if tsec.size == 0:
            tsec = np.array([0.0], dtype=float)
        dt_header = float(tsec[1] - tsec[0]) if n_steps > 1 else 1.0

        # Nodes
        report(5, "Building nodes", f"nx={nx}, ny={ny}, dx={dx}, dy={dy}")
        _maybe_cancel()
        Xn, Yn = en_nodes_from_dfs2(dfs2, prefer_geo_anchor=True)
        n_node = (ny + 1) * (nx + 1)
        Zn = np.full(n_node, 0.0, dtype=np.float32)
        codes = np.ones(n_node, dtype=np.int32)

        # Mask: optional NaN-based masking (off by default)
        mask_with_nan = False
        item_for_mask = 1
        if mask_with_nan:
            report(8, "Reading mask")
            _maybe_cancel()
            arr0 = np.asarray(dfs2.ReadItemTimeStep(item_for_mask, 0).Data, float)
            cell_valid = np.isfinite(arr0.reshape(ny, nx))
        else:
            cell_valid = np.ones((ny, nx), dtype=bool)

        # Elements
        report(12, "Building elements", f"valid cells≈{int(cell_valid.sum())}")
        _maybe_cancel()
        node_id = (np.arange(n_node).reshape(ny + 1, nx + 1) + 1).astype(np.int32)
        elements = []
        for j in range(ny):
            if ny and (j % max(1, ny // 50) == 0):
                report(12 + 8 * (j / max(1, ny - 1)), f"Elements row {j+1}/{ny}")
                _maybe_cancel()
            row_valid = cell_valid[j, :]
            if not row_valid.any():
                continue
            for i in range(nx):
                if not row_valid[i]:
                    continue
                n00 = node_id[j, i]
                n10 = node_id[j, i + 1]
                n11 = node_id[j + 1, i + 1]
                n01 = node_id[j + 1, i]
                elements.append(np.asarray([n00, n10, n11, n01], dtype=np.int32))

        if not elements:
            if ui:
                ui.close()
            if dfs2:
                dfs2.Close()
            return "No valid cells to convert."

        # Projection
        P = dfs2.FileInfo.Projection
        proj = DfsFactory().CreateProjection(P.WKTString)

        # DFSU 2D type
        two_d = None
        for m in DfsuFileType:
            if "2D" in m.name.upper() or "MESH2" in m.name.upper():
                two_d = m
                break
        if two_d is None:
            if ui:
                ui.close()
            if dfs2:
                dfs2.Close()
            return "No 2D DfsuFileType found."

        # Build DFSU
        report(22, "Creating DFSU", f"items={n_items}, start={start_time.isoformat()}")
        _maybe_cancel()
        builder = DfsuBuilder.Create(two_d)
        builder.SetNodes(Xn, Yn, Zn, codes)
        builder.SetElements(elements)
        builder.SetProjection(proj)
        builder.SetTimeInfo(start_time, float(dt_header))

        for k in range(n_items):
            info = dfs2.ItemInfo[k]
            qty = getattr(info, "Quantity", None) or eumQuantity.Create(
                eumItem.eumIGeneral, eumUnit.eumUunitUndefined
            )
            builder.AddDynamicItem(info.Name, qty)

        dfsu = builder.CreateFile(str(out_path))
        created_out = True

        # Stream writes with frequent cancel checks
        report(30, "Writing data", f"steps={n_steps}, items={n_items}")
        total_frames = max(1, n_steps * n_items)
        wrote = 0
        tick = 1  # update every frame

        for it in range(n_steps):
            t_sec = float(tsec[it])
            _maybe_cancel()
            for k in range(1, n_items + 1):
                _maybe_cancel()
                vals = dfs2.ReadItemTimeStep(k, it).Data
                mask = vals == dfs2.FileInfo.DeleteValueFloat
                vals[mask] = dfsu.DeleteValueFloat
                elem_vals = vals.reshape(ny, nx).ravel(order="C").astype(np.float32, copy=False)
                dfsu.WriteItemTimeStepNext(t_sec, elem_vals)
                wrote += 1
                if (wrote % tick) == 0:
                    pct = 30 + 68 * (wrote / total_frames)
                    report(pct, f"Writing {wrote}/{total_frames}", f"t={t_sec:.3f}s, item={k}/{n_items}")

        report(98, "Finalizing", "closing files")

    except KeyboardInterrupt:
        # User cancel: close and remove partial file
        try:
            if dfsu is not None:
                try:
                    dfsu.Close()
                except Exception:
                    pass
            if dfs2 is not None:
                try:
                    dfs2.Close()
                except Exception:
                    pass
        finally:
            if created_out and os.path.exists(out_path):
                try:
                    os.remove(out_path)
                except OSError:
                    pass
            if ui:
                ui.close()
        return "Cancelled by user"

    except Exception as exc:
        # Any other error: close and clean partial
        try:
            if dfsu is not None:
                try:
                    dfsu.Close()
                except Exception:
                    pass
            if dfs2 is not None:
                try:
                    dfs2.Close()
                except Exception:
                    pass
        finally:
            if created_out and os.path.exists(out_path):
                try:
                    os.remove(out_path)
                except OSError:
                    pass
            if ui:
                ui.close()
        return f"Error: {exc}"

    else:
        # Success
        try:
            if dfsu is not None:
                dfsu.Close()
        finally:
            if dfs2 is not None:
                dfs2.Close()
            if ui:
                ui.update(100, "Done", "")
                ui.close()
        return True


if __name__ == '__main__':
    # in_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'
    # out_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/test5.dfsu'
    
    
    in_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'
    out_path = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\Models\F3\2024\10. October/test2.dfsu'
    
    Dfs2_to_Dfsu(in_path, out_path, show_qt_progress=True)
