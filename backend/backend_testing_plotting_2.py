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

xml_path = r'C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj'
project = XMLUtils(xml_path)

adcp_cfgs = project.get_survey_adcp_cfgs("Survey 1")
obs_cfgs = project.get_survey_obs_cfgs("Survey 1")

ws_cfgs  = project.get_survey_ws_cfgs("Survey 2")



# load ADCPS
adcps = []
for cfg in adcp_cfgs:
    adcp = ADCPDataset(cfg, name = cfg['name'])
    adcps.append(adcp)
    
# not implement\ed
obs_profiles = []
water_samples = []




#%%To DO 

# on hover, show transect start date alongside name 

# 

#%%
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
                             QAction, QToolBar, QMenuBar, QMenu, QFileDialog,
                             QTabWidget, QInputDialog, QColorDialog, QDialog, QPlainTextEdit)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib import colors as mcolors
import numpy as np
from pyproj import Transformer


class ADCPMapCanvas(FigureCanvas):
    def __init__(self, adcps):
        self.current_label = 'absolute_backscatter'
        self.current_label_display = 'Absolute Backscatter'
        import matplotlib.gridspec as gridspec
        self.fig = Figure()
        super().__init__(self.fig)
        gs = self.fig.add_gridspec(2, 3, height_ratios=[20, 1], hspace=0.2)
        self.ax = self.fig.add_subplot(gs[0, :])
        self.cax = self.fig.add_subplot(gs[1, 2])
        self.ax.set_aspect('equal', adjustable='datalim')

        self.adcps = adcps
        self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        self.collections = []
        self.current_cmap = 'turbo_r'
        self.norm = None
        self.hover_index = None
        self.selected_index = None
        self.hover_callback = None
        self.tolerance = 15  # pixel distance tolerance for hover detection

        
        self.vector_layers = []
        self.setAcceptDrops(True)

        self.backscatter_cache = []
        self.plot_transects()
        self.mpl_connect("motion_notify_event", self.on_hover)
        self.mpl_connect("button_press_event", self.on_click)

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
            import geopandas as gpd, os
        except ImportError as e:
            raise RuntimeError("geopandas is required to load shapefiles") from e
        gdf = gpd.read_file(path)
        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        if gdf.crs.to_string().upper() != "EPSG:3857":
            gdf = gdf.to_crs("EPSG:3857")
        name = os.path.basename(path)
        self.vector_layers.append({
            "name": name,
            "gdf": gdf,
            "edgecolor": edgecolor,
            "linewidth": linewidth,
            "linealpha": 1.0,
            "fillcolor": "#cccccc",
            "fillalpha": 0.2,
            "visible": True
        })

    def plot_transects(self):
        # preserve current view limits
        try:
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()
        except Exception:
            cur_xlim, cur_ylim = None, None

        self.ax.clear()
        all_values = np.concatenate([
            np.nanmax(np.nanmax(adcp.get_beam_data('absolute_backscatter', mask = True),axis=2),axis=1)[:-1]
            for adcp in self.adcps
        ])
        self.norm = Normalize(vmin=all_values.min(), vmax=all_values.max())

        all_x, all_y = [], []
        self.collections.clear()
        self.backscatter_cache.clear()

        for i, adcp in enumerate(self.adcps):
            lon = np.array(adcp.position.x)
            lat = np.array(adcp.position.y)
            x, y = self.transformer.transform(lon, lat)
            all_x.extend(x)
            all_y.extend(y)

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            color = np.nanmax(np.nanmax(adcp.get_beam_data('absolute_backscatter', mask = True),axis=2),axis=1)[:-1]
            self.backscatter_cache.append(color)

            lc = LineCollection(segments, array=color, cmap='turbo_r',
                                linewidth=2, norm=self.norm)
            self.ax.add_collection(lc)
            self.collections.append(lc)

        # set data limits based on transects
        if all_x and all_y:
            try:
                self.ax.set_xlim(min(all_x), max(all_x))
                self.ax.set_ylim(min(all_y), max(all_y))
            except Exception:
                pass

        # draw shapefiles beneath transects
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

        import matplotlib.cm as cm
        if isinstance(self.current_cmap, str) and self.current_cmap.startswith("cmo."):
            import cmocean
            cmap_obj = getattr(cmocean.cm, self.current_cmap[4:])
        else:
            cmap_obj = self.current_cmap
        sm = cm.ScalarMappable(cmap=cmap_obj, norm=self.norm)
        sm.set_array([])
        # refresh colorbar axis then draw
        self.cax.cla()
        self.fig.colorbar(sm, cax=self.cax, orientation='horizontal', label=self.current_label_display)
        self.draw()

    def on_hover(self, event):
        if event.inaxes != self.ax:
            return
        closest = self.find_closest_transect(event.xdata, event.ydata, self.tolerance)
        if closest != self.hover_index:
            self.hover_index = closest
            if self.hover_callback:
                self.hover_callback(closest if closest is not None else "None")
            self.update_colors()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        idx = self.find_closest_transect(event.xdata, event.ydata, self.tolerance)
        if idx is None:
            return
        # left click: select and show instrument summary popup
        if event.button == 1:
            self.selected_index = idx
            self.update_colors()
            adcp = self.adcps[idx]
            # capture printed output or return value
            import io, contextlib
            buf = io.StringIO()
            summary_text = ""
            try:
                with contextlib.redirect_stdout(buf):
                    ret = adcp._pd0.instrument_summary()
                out = buf.getvalue().strip()
                summary_text = out if out else (ret if isinstance(ret, str) else str(ret) if ret is not None else "")
            except Exception as e:
                summary_text = f"Error generating summary: {e}"
            self.show_text_popup(f"Instrument Summary: {getattr(adcp, 'name', idx)}", summary_text)
        # right click opens context menu
        elif event.button == 3:
            qme = getattr(event, 'guiEvent', None)
            global_pos = qme.globalPos() if qme is not None else None
            self.show_transect_menu(idx, global_pos)

    def show_transect_menu(self, idx, global_pos=None):
        from PyQt5.QtWidgets import QMenu
        menu = QMenu()
        a_beam_geom = menu.addAction("beam_geometry_animation")
        a_four_beam = menu.addAction("four_beam_flood_plot")
        a_platform  = menu.addAction("platform_orientation")
        a_single    = menu.addAction("single_beam_flood_plot")
        a_tr_anim   = menu.addAction("transect_animation")
        a_tr_vel    = menu.addAction("transect_velocities")
        a_vel_flood = menu.addAction("velocity_flood_plot")

        chosen = menu.exec_(global_pos) if global_pos is not None else menu.exec_()
        if not chosen:
            return

        adcp = self.adcps[idx]
        # one explicit call per option; adjust args later as needed
        if chosen == a_beam_geom:
            adcp.plot.beam_geometry_animation()
        elif chosen == a_four_beam:
            try:
                adcp.plot.four_beam_flood_plot(field_name=self.current_label, cmap=self.current_cmap)
            except TypeError:
                adcp.plot.four_beam_flood_plot(variable=self.current_label, cmap=self.current_cmap)
        elif chosen == a_platform:
            adcp.plot.platform_orientation()
        elif chosen == a_single:
            try:
                adcp.plot.single_beam_flood_plot(field_name=self.current_label, cmap=self.current_cmap)
            except TypeError:
                adcp.plot.single_beam_flood_plot(variable=self.current_label, cmap=self.current_cmap)
        elif chosen == a_tr_anim:
            adcp.plot.transect_animation()
        elif chosen == a_tr_vel:
            adcp.plot.transect_velocities()
        elif chosen == a_vel_flood:
            try:
                adcp.plot.velocity_flood_plot(field_name=self.current_label, cmap=self.current_cmap)
            except TypeError:
                adcp.plot.velocity_flood_plot(variable=self.current_label, cmap=self.current_cmap)
    def find_closest_transect(self, x, y, tol):
        min_dist = float("inf")
        closest_index = None
        for i, lc in enumerate(self.collections):
            for seg in lc.get_segments():
                dist = np.min(np.linalg.norm(seg - np.array([x, y]), axis=1))
                if dist < tol and dist < min_dist:
                    min_dist = dist
                    closest_index = i
        return closest_index

    def update_colors(self):
        for i, lc in enumerate(self.collections):
            if i == self.selected_index:
                lc.set_color("red")
                lc.set_array(None)
            elif i == self.hover_index and i != self.selected_index:
                lc.set_color("yellow")
                lc.set_array(None)
            else:
                lc.set_array(self.backscatter_cache[i])
                lc.set_color(None)
                lc.set_cmap(self.current_cmap)
                lc.set_norm(self.norm)
        self.draw()

    def show_text_popup(self, title: str, text: str):
        dlg = QDialog(self.window())
        dlg.setWindowTitle(title)
        edit = QPlainTextEdit(dlg)
        edit.setPlainText(text or "(no output)")
        edit.setReadOnly(True)
        edit.setMinimumSize(640, 480)
        layout = QVBoxLayout(dlg)
        layout.addWidget(edit)
        dlg.setLayout(layout)
        dlg.exec_()


class ADCPMainWindow(QMainWindow):
    def __init__(self, adcps):
        super().__init__()
        self.setWindowTitle("ADCP Transect Viewer")
        self.canvas = ADCPMapCanvas(adcps)
        self.canvas.layers_changed_callback = self.refresh_shapefile_menu
        self.hover_label = QLabel("Hover index: None")
        self.canvas.hover_callback = self.update_hover_label

        # Tabs at top
        tabs = QTabWidget()
        map_tab = QWidget()
        layout = QVBoxLayout(map_tab)
        layout.addWidget(self.canvas, stretch=1)
        layout.addWidget(self.hover_label, stretch=0)
        tabs.addTab(map_tab, "Map")
        self.setCentralWidget(tabs)

        # Zoom/pan toolbar under menubar
        navtb = NavigationToolbar(self.canvas, self)
        self.addToolBar(Qt.TopToolBarArea, navtb)

        # Menubar with single "Options" menu
        menubar = QMenuBar(self)
        options_menu = menubar.addMenu("Options")

        # Transect submenu
        transect_menu = QMenu("Transect", self)
        options_menu.addMenu(transect_menu)
        act_colormap = QAction("Colormap...", self); act_colormap.triggered.connect(self.choose_colormap)
        act_vmin    = QAction("Set vmin...", self);  act_vmin.triggered.connect(self.set_vmin)
        act_vmax    = QAction("Set vmax...", self);  act_vmax.triggered.connect(self.set_vmax)
        transect_menu.addActions([act_colormap, act_vmin, act_vmax])

        # Shapefiles submenu
        self.shapefile_menu = QMenu("Shapefiles", self)
        options_menu.addMenu(self.shapefile_menu)
        self.setMenuBar(menubar)
        self.refresh_shapefile_menu()

    # ---- dynamic shapefile menu ----
    def refresh_shapefile_menu(self):
        self.shapefile_menu.clear()
        load_action = QAction("Load shapefile...", self)
        load_action.triggered.connect(self.load_shapefile_dialog)
        self.shapefile_menu.addAction(load_action)
        self.shapefile_menu.addSeparator()
        for idx, layer in enumerate(self.canvas.vector_layers):
            sub = QMenu(layer["name"], self)
            # visibility toggle
            vis_act = QAction("Visible", self, checkable=True)
            vis_act.setChecked(layer.get("visible", True))
            vis_act.triggered.connect(lambda checked, i=idx: self.toggle_layer_visibility(i, checked))
            sub.addAction(vis_act)
            # styling actions
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

            # remove
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
            self.refresh_shapefile_menu()
            self.canvas.plot_transects()

    # ---- shapefile style setters ----
    def set_layer_linewidth(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            cur = float(self.canvas.vector_layers[idx].get("linewidth", 1.0))
            val, ok = QInputDialog.getDouble(self, "Line width", "pixels:", cur, 0.1, 50.0, 2)
            if ok:
                self.canvas.vector_layers[idx]["linewidth"] = float(val)
                self.canvas.plot_transects()

    def set_layer_linecolor(self, idx):
        if 0 <= idx < len(self.canvas.vector_layers):
            cur = self.canvas.vector_layers[idx].get("edgecolor", "#444444")
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
            cur = self.canvas.vector_layers[idx].get("fillcolor", "#cccccc")
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
        import matplotlib.pyplot as plt
        cmaps = sorted(plt.colormaps())
        text, ok = QInputDialog.getItem(self, "Choose colormap", "Colormap:", cmaps, editable=True)
        if ok and text:
            self.change_colormap(text)

    def set_vmin(self):
        if self.canvas.norm is None:
            return
        val, ok = QInputDialog.getDouble(self, "Set vmin", "vmin:", float(self.canvas.norm.vmin))
        if ok:
            self.canvas.norm.vmin = val
            self.canvas.plot_transects()

    def set_vmax(self):
        if self.canvas.norm is None:
            return
        val, ok = QInputDialog.getDouble(self, "Set vmax", "vmax:", float(self.canvas.norm.vmax))
        if ok:
            self.canvas.norm.vmax = val
            self.canvas.plot_transects()

    def change_colormap(self, cmap_name):
        import cmocean
        if isinstance(cmap_name, str) and cmap_name.startswith("cmo."):
            cmap = getattr(cmocean.cm, cmap_name[4:])
        else:
            cmap = cmap_name
        for i, lc in enumerate(self.canvas.collections):
            if i != self.canvas.selected_index and i != self.canvas.hover_index:
                lc.set_cmap(cmap)
        self.canvas.current_cmap = cmap_name
        self.canvas.plot_transects()

    def update_hover_label(self, index):
        if isinstance(index, int):
            name = self.canvas.adcps[index].name
            self.hover_label.setText(f"Hovering: {name}")
        else:
            self.hover_label.setText("Hovering: None")

# Usage example
import sys
app = QApplication(sys.argv)
window = ADCPMainWindow(adcps)
window.show()
sys.exit(app.exec_())
