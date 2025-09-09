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

# xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
# project = XMLUtils(xml_path)
# survey_name = 'Survey 1'


# adcp_cfgs = project.get_survey_adcp_cfgs(survey_name)
# obs_cfgs = project.get_survey_obs_cfgs(survey_name)
# ws_elems  = project.get_survey_ws_elems("Survey 2")


# # load ADCP data
# adcps = []
# for cfg in adcp_cfgs:
#     adcp = ADCPDataset(cfg, name = cfg['name'])
#     adcps.append(adcp)
    
# # load OBS data 
# obss = []
# for cfg in obs_cfgs:
#     obs = OBSDataset(cfg)
#     obss.append(obs)
    
    
# # load water sample data 
# water_samps = []
# for el in ws_elems:
#     ws = WaterSampleDataset(el)
#     water_samps.append(ws)

  
#attribute position to each obs profile
#%%
# for obs in obss:
#     obs_st = pd.to_datetime(np.nanmin(obs.data.datetime)).to_pydatetime()
#     obs_et = pd.to_datetime(np.nanmax(obs.data.datetime)).to_pydatetime()
#     for adcp in adcps:
#         adcp_st = pd.to_datetime(np.nanmin(adcp.time.ensemble_datetimes)).to_pydatetime()
#         adcp_et = pd.to_datetime(np.nanmax(adcp.time.ensemble_datetimes)).to_pydatetime()

#         overlap = (obs_st <= adcp_et) and (obs_et >= adcp_st)
#         if overlap:
#             obs.position = adcp.position
#             obs.position._resample_to(obs.data.datetime)
            
 
# for ws in water_samps:
#     ws_time = pd.to_datetime(ws.data.datetime).to_pydatetime()
#     ws_x = []
#     ws_y = []
#     for t in ws_time:
        
#         for adcp in adcps:
#             adcp_st = pd.to_datetime(np.nanmin(adcp.time.ensemble_datetimes)).to_pydatetime()
#             adcp_et = pd.to_datetime(np.nanmax(adcp.time.ensemble_datetimes)).to_pydatetime()

#             overlap = (t <= adcp_et) and (t >= adcp_st)
            
#             if overlap:
#                 print(overlap)
            # if overlap:
                
            #     ws.position._resample_to(ws.data.datetime)



# # not implement\ed
# obs_profiles = []
# water_samples = []




# #%%To DO 

# on hover, show transect start date alongside name 

# 

#%%
# -*- coding: utf-8 -*-
"""
ADCP transect map with OBS overlay, selection, and context menus.
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QAction, QMenuBar, QMenu, QFileDialog, QTabWidget,
    QInputDialog, QColorDialog, QDialog, QPlainTextEdit,
    QProgressDialog
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib import colors as mcolors
from pyproj import Transformer

# project imports (adjust sys.path one level up)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils_xml import XMLUtils
from adcp import ADCP as ADCPDataset
from obs import OBS as OBSDataset


# -----------------------------
# Canvas: ADCP transects + OBS
# -----------------------------
class ADCPMapCanvas(FigureCanvas):
    def __init__(self, adcps, obss=None):
        self.current_label = 'absolute_backscatter'
        self.current_label_display = 'Absolute Backscatter'
        self.current_cmap = 'turbo_r'
        self.norm = None

        self.adcps = list(adcps)
        self.obss = list(obss or [])

        self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        self.collections = []            # LineCollection per ADCP
        self.backscatter_cache = []      # color arrays per ADCP

        self.hover_index = None          # ADCP hover
        self.selected_index = None       # ADCP selected
        self.tolerance = 15              # data-units heuristic for lines

        self.obs_pts_xy = None           # (N,2) projected
        self.obs_scatter = None          # PathCollection
        self.hover_obs_index = None      # OBS hover
        self.selected_obs_index = None   # OBS selected
        self.obs_tol = 25                # px

        self.hover_callback = None
        self.vector_layers = []

        self.fig = Figure()
        super().__init__(self.fig)
        import matplotlib.gridspec as gridspec
        gs = self.fig.add_gridspec(2, 3, height_ratios=[20, 1], hspace=0.2)
        self.ax = self.fig.add_subplot(gs[0, :])
        self.cax = self.fig.add_subplot(gs[1, 2])
        self.ax.set_aspect('equal', adjustable='datalim')
        self.setAcceptDrops(True)

        self.plot_transects()
        self.mpl_connect("motion_notify_event", self.on_hover)
        self.mpl_connect("button_press_event", self.on_click)
        self.mpl_connect("button_release_event", self.on_release)
        self.mpl_connect("scroll_event", self.on_scroll)

    # ----- DnD shapefiles -----
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for u in event.mimeData().urls():
                if str(u.toLocalFile()).lower().endswith('.shp'):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        paths = [str(u.toLocalFile()) for u in event.mimeData().urls()]
        for p in paths:
            if p.lower().endswith('.shp'):
                self.add_vector_layer(p)
        self.plot_transects()

    def add_vector_layer(self, path, edgecolor="#444444", linewidth=1.0):
        try:
            import geopandas as gpd, os as _os
        except ImportError as e:
            raise RuntimeError("geopandas is required to load shapefiles") from e
        gdf = gpd.read_file(path)
        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        if gdf.crs.to_string().upper() != "EPSG:3857":
            gdf = gdf.to_crs("EPSG:3857")
        name = _os.path.basename(path)
        self.vector_layers.append({
            "name": name,
            "gdf": gdf,
            "edgecolor": edgecolor,
            "linewidth": linewidth,
            "linealpha": 1.0,
            "fillcolor": "#cccccc",
            "fillalpha": 0.2,
            "visible": True,
        })

    # ----- Plot -----
    def plot_transects(self):
        self.ax.clear()

        if not self.adcps:
            self.draw(); return

        # gather color range from all ADCPs
        all_values = []
        for adcp in self.adcps:
            try:
                v = adcp.get_beam_data('absolute_backscatter', mask=True)
                # v: (time, bins, beams) -> max over beams then bins
                vmax_t = np.nanmax(np.nanmax(v, axis=2), axis=1)[:-1]
                all_values.append(vmax_t)
            except Exception:
                pass
        if not all_values:
            self.draw(); return
        all_values = np.concatenate(all_values)

        vmin = float(np.nanmin(all_values))
        vmax = float(np.nanmax(all_values))
        if self.norm is not None:
            if self.norm.vmin is not None: vmin = self.norm.vmin
            if self.norm.vmax is not None: vmax = self.norm.vmax
        self.norm = Normalize(vmin=vmin, vmax=vmax)

        self.collections.clear()
        self.backscatter_cache.clear()

        all_x, all_y = [], []
        for adcp in self.adcps:
            lon = np.asarray(adcp.position.x)
            lat = np.asarray(adcp.position.y)
            X, Y = self.transformer.transform(lon, lat)
            all_x.extend(X); all_y.extend(Y)

            pts = np.column_stack([X, Y]).reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            color = np.nanmax(np.nanmax(adcp.get_beam_data('absolute_backscatter', mask=True), axis=2), axis=1)[:-1]
            self.backscatter_cache.append(color)

            lc = LineCollection(segs, array=color, cmap=self.current_cmap, linewidth=2, norm=self.norm)
            self.ax.add_collection(lc)
            self.collections.append(lc)

        if all_x and all_y:
            try:
                self.ax.set_xlim(np.nanmin(all_x), np.nanmax(all_x))
                self.ax.set_ylim(np.nanmin(all_y), np.nanmax(all_y))
            except Exception:
                pass

        # shapefile layers
        for layer in self.vector_layers:
            if not layer.get("visible", True):
                continue
            g = layer["gdf"]
            ec = mcolors.to_rgba(layer.get("edgecolor", "#444444"), layer.get("linealpha", 1.0))
            fc = mcolors.to_rgba(layer.get("fillcolor", "#cccccc"), layer.get("fillalpha", 0.2))
            try:
                g.plot(ax=self.ax, facecolor=fc, edgecolor=ec, linewidth=layer.get("linewidth", 1.0), zorder=0)
            except Exception:
                g.boundary.plot(ax=self.ax, edgecolor=ec, linewidth=layer.get("linewidth", 1.0), zorder=0)

        # colorbar
        import matplotlib.cm as cm
        cmap_obj = self._resolve_cmap(self.current_cmap)
        sm = cm.ScalarMappable(cmap=cmap_obj, norm=self.norm)
        sm.set_array([])
        self.cax.cla()
        self.fig.colorbar(sm, cax=self.cax, orientation='horizontal', label=self.current_label_display)

        # OBS mean points
        self._build_obs_points()

        self.draw()

    def _resolve_cmap(self, name):
        if isinstance(name, str) and name.startswith("cmo."):
            import cmocean
            return getattr(cmocean.cm, name[4:])
        return name

    def _build_obs_points(self):
        pts = []
        for obs in self.obss:
            try:
                lon = np.asarray(getattr(obs.position, 'x', []), float)
                lat = np.asarray(getattr(obs.position, 'y', []), float)
                if lon.size == 0 or lat.size == 0:
                    continue
                X, Y = self.transformer.transform(lon, lat)
                xm, ym = np.nanmean(X), np.nanmean(Y)
                if np.isfinite(xm) and np.isfinite(ym):
                    pts.append([xm, ym])
            except Exception:
                pass
        self.obs_pts_xy = np.array(pts) if pts else None
        if self.obs_pts_xy is not None and self.obs_pts_xy.size:
            if self.obs_scatter is None:
                self.obs_scatter = self.ax.scatter(
                    self.obs_pts_xy[:, 0], self.obs_pts_xy[:, 1],
                    s=52, marker='o', facecolors='white', edgecolors='k',
                    linewidths=1.2, zorder=4
                )
            else:
                self.obs_scatter.set_offsets(self.obs_pts_xy)

    # ----- Events -----
    def on_hover(self, event):
        if getattr(self, "_is_panning", False):
            if event.inaxes == self.ax and event.xdata is not None and self._pan_start is not None:
                dx = event.xdata - self._pan_start[0]
                dy = event.ydata - self._pan_start[1]
                x0, x1 = self._pan_xlim
                y0, y1 = self._pan_ylim
                self.ax.set_xlim(x0 - dx, x1 - dx)
                self.ax.set_ylim(y0 - dy, y1 - dy)
                self.draw_idle()
            return
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        # OBS priority
        j = self.find_closest_obs(event.xdata, event.ydata, self.obs_tol)
        changed = False
        if j != self.hover_obs_index:
            self.hover_obs_index = j
            changed = True
        if j is None:
            i = self.find_closest_transect(event.xdata, event.ydata, self.tolerance)
            if i != self.hover_index:
                self.hover_index = i
                if self.hover_callback:
                    self.hover_callback(i if i is not None else "None")
                changed = True
        if changed:
            self.update_colors()

    def on_click(self, event):
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        # OBS first
        j = self.find_closest_obs(event.xdata, event.ydata, self.obs_tol)
        if j is not None:
            if event.button == 1:
                self.selected_obs_index = j
                self.update_colors()
                obs = self.obss[j]
                title = f"OBS: {getattr(obs, 'name', j)}"
                try:
                    t0 = pd.to_datetime(np.nanmin(obs.data.datetime))
                    t1 = pd.to_datetime(np.nanmax(obs.data.datetime))
                    txt = f"Start: {t0}\nEnd: {t1}\nN: {len(obs.data)}"
                except Exception:
                    txt = "(no summary)"
                self.show_text_popup(title, txt)
            elif event.button == 3:
                qme = getattr(event, 'guiEvent', None)
                self.show_obs_menu(j, qme.globalPos() if qme is not None else None)
            return
        # ADCP fallback
        i = self.find_closest_transect(event.xdata, event.ydata, self.tolerance)
        if i is None:
            return
        if event.button == 1:
            self.selected_index = i
            self.update_colors()
            adcp = self.adcps[i]
            import io, contextlib
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    ret = adcp._pd0.instrument_summary()
                out = buf.getvalue().strip()
                summary_text = out if out else (ret if isinstance(ret, str) else str(ret) if ret is not None else "")
            except Exception as e:
                summary_text = f"Error generating summary: {e}"
            self.show_text_popup(f"Instrument Summary: {getattr(adcp, 'name', i)}", summary_text)
        elif event.button == 3:
            qme = getattr(event, 'guiEvent', None)
            self.show_transect_menu(i, qme.globalPos() if qme is not None else None)

    def on_release(self, event):
        if event.button == 1 and getattr(self, "_is_panning", False):
            self._is_panning = False
            self._pan_start = None
            self._pan_xlim = None
            self._pan_ylim = None

    def on_scroll(self, event):
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        base_scale = 1.2
        scale = 1.0 / base_scale if event.button == 'up' else base_scale if event.button == 'down' else None
        if scale is None:
            return
        x_left, x_right = self.ax.get_xlim()
        y_bottom, y_top = self.ax.get_ylim()
        new_left   = event.xdata - (event.xdata - x_left) * scale
        new_right  = event.xdata + (x_right - event.xdata) * scale
        new_bottom = event.ydata - (event.ydata - y_bottom) * scale
        new_top    = event.ydata + (y_top - event.ydata) * scale
        self.ax.set_xlim(new_left, new_right)
        self.ax.set_ylim(new_bottom, new_top)
        self.draw_idle()

    # ----- Menus -----
    def show_transect_menu(self, idx, global_pos=None):
        menu = QMenu()
        a_beam_geom = menu.addAction("beam_geometry_animation")
        a_four_beam = menu.addAction("four_beam_flood_plot")
        a_platform  = menu.addAction("platform_orientation")
        a_tr_anim   = menu.addAction("transect_animation")
        a_tr_vel    = menu.addAction("transect_velocities")
        a_vel_flood = menu.addAction("velocity_flood_plot")
        chosen = menu.exec_(global_pos) if global_pos is not None else menu.exec_()
        if not chosen:
            return
        adcp = self.adcps[idx]
        if chosen == a_beam_geom:
            fig, ani = adcp.plot.beam_geometry_animation(); self._beam_ani = ani; fig.show()
        elif chosen == a_four_beam:
            adcp.plot.four_beam_flood_plot(field_name=self.current_label, cmap=self.current_cmap,
                                           vmin=self.norm.vmin, vmax=self.norm.vmax)
        elif chosen == a_platform:
            adcp.plot.platform_orientation()
        elif chosen == a_tr_anim:
            fig, ani = adcp.plot.transect_animation(cmap=self.current_cmap, vmin=self.norm.vmin, vmax=self.norm.vmax)
            self._transect_ani = ani; fig.show()
        elif chosen == a_tr_vel:
            adcp.plot.transect_velocities()
        elif chosen == a_vel_flood:
            adcp.plot.velocity_flood_plot(field_name=self.current_label, cmap=self.current_cmap)

    def show_obs_menu(self, j, global_pos=None):
        menu = QMenu()
        a_profile = menu.addAction("Depth Profile")

        chosen = menu.exec_(global_pos) if global_pos is not None else menu.exec_()
        if not chosen:
            return
        obs = self.obss[j]
        if chosen == a_profile and hasattr(getattr(obs, 'plot', None), 'depth_profile'):
            obs.plot.depth_profile()
     

    # ----- Helpers -----
    def find_closest_transect(self, x, y, tol):
        min_dist = float("inf")
        closest_index = None
        q = np.array([x, y])
        for i, lc in enumerate(self.collections):
            for seg in lc.get_segments():
                d = np.min(np.linalg.norm(seg - q, axis=1))
                if d < tol and d < min_dist:
                    min_dist = d
                    closest_index = i
        return closest_index

    def find_closest_obs(self, x, y, tol_px):
        if self.obs_pts_xy is None or self.obs_pts_xy.size == 0:
            return None
        pts_disp = self.ax.transData.transform(self.obs_pts_xy)
        qx, qy = self.ax.transData.transform([[x, y]])[0]
        d = np.hypot(pts_disp[:, 0] - qx, pts_disp[:, 1] - qy)
        j = int(np.argmin(d))
        return j if d[j] <= tol_px else None

    def update_colors(self):
        # ADCP
        for i, lc in enumerate(self.collections):
            if i == self.selected_index:
                lc.set_color('red'); lc.set_array(None)
            elif i == self.hover_index and i != self.selected_index:
                lc.set_color('yellow'); lc.set_array(None)
            else:
                lc.set_array(self.backscatter_cache[i])
                lc.set_color(None)
                lc.set_cmap(self._resolve_cmap(self.current_cmap))
                lc.set_norm(self.norm)
        # OBS
        if self.obs_scatter is not None and self.obs_pts_xy is not None:
            n = self.obs_pts_xy.shape[0]
            ec = np.tile([[0, 0, 0, 1.0]], (n, 1))
            fc = np.tile([[1, 1, 1, 1.0]], (n, 1))
            if self.hover_obs_index is not None:
                ec[self.hover_obs_index] = [1, 0.8, 0, 1.0]
            if self.selected_obs_index is not None:
                ec[self.selected_obs_index] = [1, 0, 0, 1.0]
                fc[self.selected_obs_index] = [1, 1, 1, 1.0]
            self.obs_scatter.set_edgecolors(ec)
            self.obs_scatter.set_facecolors(fc)
        self.draw_idle()

    def show_text_popup(self, title: str, text: str):
        dlg = QDialog(self.window()); dlg.setWindowTitle(title)
        edit = QPlainTextEdit(dlg); edit.setPlainText(text or "(no output)")
        edit.setReadOnly(True); edit.setMinimumSize(640, 480)
        layout = QVBoxLayout(dlg); layout.addWidget(edit); dlg.setLayout(layout)
        dlg.exec_()


# -----------------------------
# Main Window
# -----------------------------
class ADCPMainWindow(QMainWindow):
    def __init__(self, xml_path, survey_name):
        super().__init__()

        project = XMLUtils(xml_path)
        adcp_cfgs = project.get_survey_adcp_cfgs(survey_name)
        obs_cfgs  = project.get_survey_obs_cfgs(survey_name)

        progress = QProgressDialog("Loading ADCP transects...", "Cancel", 0, len(adcp_cfgs), self)
        progress.setWindowTitle("Loading"); progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.show()
        QApplication.processEvents()

        adcps = []
        for i, cfg in enumerate(adcp_cfgs):
            QApplication.processEvents()
            if progress.wasCanceled():
                break
            adcp = ADCPDataset(cfg, name=cfg.get('name', f'ADCP {i}'))
            adcps.append(adcp)
            progress.setValue(i + 1)
        progress.close()

        obss = []
        for cfg in obs_cfgs:
            try:
                obss.append(OBSDataset(cfg))
            except Exception:
                pass

        # attach positions to OBS where time ranges overlap an ADCP
        for obs in obss:
            try:
                obs_st = pd.to_datetime(np.nanmin(obs.data.datetime)).to_pydatetime()
                obs_et = pd.to_datetime(np.nanmax(obs.data.datetime)).to_pydatetime()
            except Exception:
                continue
            for adcp in adcps:
                try:
                    adcp_st = pd.to_datetime(np.nanmin(adcp.time.ensemble_datetimes)).to_pydatetime()
                    adcp_et = pd.to_datetime(np.nanmax(adcp.time.ensemble_datetimes)).to_pydatetime()
                except Exception:
                    continue
                if (obs_st <= adcp_et) and (obs_et >= adcp_st):
                    obs.position = adcp.position
                    try:
                        obs.position._resample_to(obs.data.datetime)
                    except Exception:
                        pass
                    break

        self.setWindowTitle("ADCP Transect Viewer")
        self.canvas = ADCPMapCanvas(adcps, obss)
        self.hover_label = QLabel("Hover index: None")
        self.canvas.hover_callback = self.update_hover_label

        tabs = QTabWidget(); map_tab = QWidget(); layout = QVBoxLayout(map_tab)
        layout.addWidget(self.canvas, stretch=1); layout.addWidget(self.hover_label, stretch=0)
        tabs.addTab(map_tab, "Map"); self.setCentralWidget(tabs)

        navtb = NavigationToolbar(self.canvas, self)
        self.addToolBar(Qt.TopToolBarArea, navtb)

        menubar = QMenuBar(self); options_menu = menubar.addMenu("Options")

        transect_menu = QMenu("Transect", self); options_menu.addMenu(transect_menu)
        act_colormap = QAction("Colormap...", self); act_colormap.triggered.connect(self.choose_colormap)
        act_vmin     = QAction("Set vmin...", self);  act_vmin.triggered.connect(self.set_vmin)
        act_vmax     = QAction("Set vmax...", self);  act_vmax.triggered.connect(self.set_vmax)
        transect_menu.addActions([act_colormap, act_vmin, act_vmax])

        self.shapefile_menu = QMenu("Shapefiles", self); options_menu.addMenu(self.shapefile_menu)
        self.setMenuBar(menubar); self.refresh_shapefile_menu()

    # ---- dynamic shapefile menu ----
    def refresh_shapefile_menu(self):
        self.shapefile_menu.clear()
        load_action = QAction("Load shapefile...", self)
        load_action.triggered.connect(self.load_shapefile_dialog)
        self.shapefile_menu.addAction(load_action)
        self.shapefile_menu.addSeparator()
        for idx, layer in enumerate(self.canvas.vector_layers):
            sub = QMenu(layer["name"], self)
            vis_act = QAction("Visible", self, checkable=True)
            vis_act.setChecked(layer.get("visible", True))
            vis_act.triggered.connect(lambda checked, i=idx: self.toggle_layer_visibility(i, checked))
            sub.addAction(vis_act)
            lw_act = QAction("Line width...", self)
            lw_act.triggered.connect(lambda _=False, i=idx: self.set_layer_linewidth(i))
            sub.addAction(lw_act)
            lc_act = QAction("Line color...", self)
            lc_act.triggered.connect(lambda _=False, i=idx: self.set_layer_linecolor(i))
            sub.addAction(lc_act)
            la_act = QAction("Line alpha...", self)
            la_act.triggered.connect(lambda _=False, i=idx: self.set_layer_linealpha(i))
            sub.addAction(la_act)
            fc_act = QAction("Fill color...", self)
            fc_act.triggered.connect(lambda _=False, i=idx: self.set_layer_fillcolor(i))
            sub.addAction(fc_act)
            fa_act = QAction("Fill alpha...", self)
            fa_act.triggered.connect(lambda _=False, i=idx: self.set_layer_fillalpha(i))
            sub.addAction(fa_act)
            rem_act = QAction("Remove", self)
            rem_act.triggered.connect(lambda _=False, i=idx: self.remove_layer(i))
            sub.addAction(rem_act)
            self.shapefile_menu.addMenu(sub)

    def load_shapefile_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open shapefile", "", "Shapefiles (*.shp)")
        if path:
            self.canvas.add_vector_layer(path)
            self.refresh_shapefile_menu()
            self.canvas.plot_transects()

    def toggle_layer_visibility(self, idx, vis):
        if 0 <= idx < len(self.canvas.vector_layers):
            self.canvas.vector_layers[idx]["visible"] = bool(vis)
            self.canvas.plot_transects()

    def remove_layer(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            self.canvas.vector_layers.pop(idx)
            self.refresh_shapefile_menu(); self.canvas.plot_transects()

    # ---- shapefile styling ----
    def set_layer_linewidth(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            cur = float(self.canvas.vector_layers[idx].get("linewidth", 1.0))
            val, ok = QInputDialog.getDouble(self, "Line width", "pixels:", cur, 0.1, 50.0, 2)
            if ok:
                self.canvas.vector_layers[idx]["linewidth"] = float(val)
                self.canvas.plot_transects()

    def set_layer_linecolor(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            color = QColorDialog.getColor()
            if color.isValid():
                self.canvas.vector_layers[idx]["edgecolor"] = color.name()
                self.canvas.plot_transects()

    def set_layer_linealpha(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            cur = float(self.canvas.vector_layers[idx].get("linealpha", 1.0))
            val, ok = QInputDialog.getDouble(self, "Line alpha", "0..1:", cur, 0.0, 1.0, 2)
            if ok:
                self.canvas.vector_layers[idx]["linealpha"] = float(val)
                self.canvas.plot_transects()

    def set_layer_fillcolor(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            color = QColorDialog.getColor()
            if color.isValid():
                self.canvas.vector_layers[idx]["fillcolor"] = color.name()
                self.canvas.plot_transects()

    def set_layer_fillalpha(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            cur = float(self.canvas.vector_layers[idx].get("fillalpha", 0.2))
            val, ok = QInputDialog.getDouble(self, "Fill alpha", "0..1:", cur, 0.0, 1.0, 2)
            if ok:
                self.canvas.vector_layers[idx]["fillalpha"] = float(val)
                self.canvas.plot_transects()

    # ---- transect controls ----
    def choose_colormap(self):
        cmaps = sorted(plt.colormaps())
        text, ok = QInputDialog.getItem(self, "Choose colormap", "Colormap:", cmaps, editable=True)
        if ok and text:
            self.change_colormap(text)

    def set_vmin(self):
        if self.canvas.norm is None:
            return
        val, ok = QInputDialog.getDouble(self, "Set vmin", "vmin:", float(self.canvas.norm.vmin))
        if ok:
            self.canvas.norm.vmin = val; self.canvas.plot_transects()

    def set_vmax(self):
        if self.canvas.norm is None:
            return
        val, ok = QInputDialog.getDouble(self, "Set vmax", "vmax:", float(self.canvas.norm.vmax))
        if ok:
            self.canvas.norm.vmax = val; self.canvas.plot_transects()

    def change_colormap(self, cmap_name):
        cmap = self.canvas._resolve_cmap(cmap_name)
        for i, lc in enumerate(self.canvas.collections):
            if i != self.canvas.selected_index and i != self.canvas.hover_index:
                lc.set_cmap(cmap)
        self.canvas.current_cmap = cmap_name
        self.canvas.plot_transects()

    def update_hover_label(self, index):
        if isinstance(index, int):
            try:
                name = self.canvas.adcps[index].name
            except Exception:
                name = str(index)
            self.hover_label.setText(f"Hovering: {name}")
        else:
            self.hover_label.setText("Hovering: None")


# -----------------------------
# Entrypoint
# -----------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)

    xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
    survey_name = 'Survey 1'

    window = ADCPMainWindow(xml_path, survey_name)
    window.show()
    sys.exit(app.exec_())
