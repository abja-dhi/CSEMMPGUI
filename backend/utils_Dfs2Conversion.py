

from datetime import datetime
import os
import numpy as np

from mikecore.DfsFileFactory import DfsFileFactory
from mikecore.DfsuBuilder import DfsuBuilder, DfsuFileType
from mikecore.DfsFactory import DfsFactory
from mikecore.eum import eumQuantity, eumItem, eumUnit


# -----------------------------
# Progress dialog (topmost, cancel)
# -----------------------------
class _QtProgress:
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
            fmt = f"{fmt} {self.suffix}"
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
# Helpers
# -----------------------------
def _times_seconds(ta_obj):
    dt_attr = getattr(ta_obj, "TimeStep", None)
    n_attr = getattr(ta_obj, "NumberOfTimeSteps", None) or getattr(ta_obj, "Count", None)
    if (dt_attr is not None) and (n_attr is not None):
        n = int(n_attr)
        dt_s = float(dt_attr)
        return np.arange(n, dtype=float) * dt_s
    times = getattr(ta_obj, "Times", None)
    return np.asarray(list(times), dtype=float) if times is not None else np.array([0.0], float)


def _build_projection_from_dfs2(dfs2):
    """
    Recreate a projection including geo-origin and orientation.
    Uses DfsFactory.CreateProjectionGeoOrigin(WKT, lon, lat, orientation) when available;
    falls back to CreateProjection(WKT) if geo-origin fields are missing.
    """
    P = dfs2.FileInfo.Projection
    wkt = str(P.WKTString)
    has_lon = hasattr(P, "Longitude")
    has_lat = hasattr(P, "Latitude")
    has_ori = hasattr(P, "Orientation")
    if has_lon and has_lat and has_ori:
        lon = float(P.Longitude)
        lat = float(P.Latitude)
        ori = float(P.Orientation)
        return DfsFactory().CreateProjectionGeoOrigin(wkt, lon, lat, ori)
    else:
        return DfsFactory().CreateProjection(wkt)


def _grid_nodes_from_dfs2(dfs2):
    ax = dfs2.SpatialAxis
    nx, ny = int(ax.XCount), int(ax.YCount)
    dx, dy = float(ax.Dx), float(ax.Dy)
    x0, y0 = float(ax.X0), float(ax.Y0)

    # index grids (ny+1, nx+1)
    ii = np.arange(nx + 1, dtype=float)
    jj = np.arange(ny + 1, dtype=float)
    I, J = np.meshgrid(ii, jj, indexing="xy")  # I: x-index, J: y-index

    # absolute node coords
    X = x0 + I * dx
    Y = y0 + J * dy

    # flatten to per-node vectors of identical length (ny+1)*(nx+1)
    Xn = X.ravel(order="C").astype(np.float64)
    Yn = Y.ravel(order="C").astype(np.float64)
    return Xn, Yn, nx, ny



# -----------------------------
# Converter
# -----------------------------
def Dfs2_to_Dfsu(in_path, out_path, *, show_qt_progress: bool = True):
    """
    Convert a DFS2 to a 2D DFSU with:
      - raw grid nodes (no manual rotation/translation),
      - projection recreated with DFS2 geo-origin + orientation,
      - DeleteValueFloat mapping.
    """
    ui = _QtProgress() if show_qt_progress else None
    if ui:
        from os.path import basename
        ui.set_suffix(f"[{basename(in_path)} → {basename(out_path)}]")
    report = (ui.update if ui else (lambda *a, **k: None))

    if os.path.exists(out_path):
        os.remove(out_path)

    report(2, "Opening DFS2")
    dfs2 = DfsFileFactory.Dfs2FileOpen(str(in_path))

    # Axis / time
    ax = dfs2.SpatialAxis
    nx = int(ax.XCount)
    ny = int(ax.YCount)
    ta = dfs2.FileInfo.TimeAxis

    start_time = getattr(ta, "StartDateTime", None)
    if not isinstance(start_time, datetime):
        start_time = datetime(2000, 1, 1)

    tsec = _times_seconds(ta).astype(float)
    n_steps = int(tsec.size) if tsec.size else 1
    if tsec.size == 0:
        tsec = np.array([0.0], dtype=float)
    dt_header = float(tsec[1] - tsec[0]) if n_steps > 1 else 1.0

    # Nodes (raw grid)
    report(8, "Building nodes", f"nx={nx}, ny={ny}")
    Xn, Yn, nx_chk, ny_chk = _grid_nodes_from_dfs2(dfs2)
    assert nx_chk == nx and ny_chk == ny
    n_node = (ny + 1) * (nx + 1)
    Zn = np.zeros(n_node, dtype=np.float32)
    codes = np.ones(n_node, dtype=np.int32)

    # Elements (quads)
    report(12, "Building elements")
    node_id = (np.arange(n_node).reshape(ny + 1, nx + 1) + 1).astype(np.int32)
    elements = []
    for j in range(ny):
        for i in range(nx):
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

    # Projection (with geo-origin + orientation)
    report(16, "Creating projection")
    proj = _build_projection_from_dfs2(dfs2)

    # DFSU type
    two_d = None
    for m in DfsuFileType:
        if "2D" in m.name.upper() or "MESH2" in m.name.upper():
            two_d = m
            break
    if two_d is None:
        if ui:
            ui.close()
        dfs2.Close()
        return "No 2D DfsuFileType found."

    # Build DFSU
    n_items = len(dfs2.ItemInfo)
    report(20, "Creating DFSU file", f"items={n_items}, start={start_time.isoformat()}")
    builder = DfsuBuilder.Create(two_d)
    builder.SetNodes(Xn, Yn, Zn, codes)
    builder.SetElements(elements)
    builder.SetProjection(proj)               # <-- set BEFORE CreateFile
    builder.SetTimeInfo(start_time, float(dt_header))

    for k in range(n_items):
        info = dfs2.ItemInfo[k]
        qty = getattr(info, "Quantity", None) or eumQuantity.Create(
            eumItem.eumIGeneral, eumUnit.eumUunitUndefined
        )
        builder.AddDynamicItem(info.Name, qty)

    dfsu = builder.CreateFile(str(out_path))

    # Stream data
    report(30, "Writing data", f"steps={n_steps}, items={n_items}")
    total_frames = max(1, n_steps * n_items)
    wrote = 0

    for it in range(n_steps):
        if it>2: break
        t_sec = float(tsec[it])
        for k in range(1, n_items + 1):
            vals = dfs2.ReadItemTimeStep(k, it).Data
            # map delete value to dfsu delete
            dv_in = dfs2.FileInfo.DeleteValueFloat
            dv_out = dfsu.DeleteValueFloat
            mask = vals == dv_in
            vals[mask] = dv_out

            elem_vals = vals.reshape(ny, nx).ravel(order="C").astype(np.float32, copy=False)
            dfsu.WriteItemTimeStepNext(t_sec, elem_vals)

            wrote += 1
            pct = 30 + 68 * (wrote / total_frames)
            report(pct, f"Writing {wrote}/{total_frames}", f"t={t_sec:.3f}s, item={k}/{n_items}")

        if ui and ui.cancelled:
            dfsu.Close()
            dfs2.Close()
            if os.path.exists(out_path):
                os.remove(out_path)
            ui.close()
            return "Cancelled by user"

    report(98, "Finalizing")
    dfsu.Close()
    dfs2.Close()
    if ui:
        ui.update(100, "Done")
        ui.close()
    return True



if __name__ == '__main__':
    # in_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'
    # out_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/test5.dfsu'
    
    
    in_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'
    out_path = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\Models\F3\2024\10. October/MT\test2.dfsu'
    
    status = Dfs2_to_Dfsu(in_path, out_path, show_qt_progress=True)
