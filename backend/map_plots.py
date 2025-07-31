
import sys
import os

# Add the project root (one level up from /tests/) to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend
from backend.pd0 import Pd0Decoder
from backend.adcp import ADCP as DatasetADCP
from backend._adcp_position import ADCPPosition
from backend.utils import Utils, CSVParser
from backend.plotting import PlottingShell

#%%

util = Utils()

#%%
import os

root = r'\\USDEN1-STOR.DHI.DK\Projects\61803553-05\2024_survey_data\10. Oct\20241009_F3(F)'

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



#%% init position datasets
pos_cfgs = []
position_datasets = []
for i,fpath in enumerate(pos_fpaths):
    print(i)
    cfg = {'filename':fpath,
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
    pos_cfgs.append(cfg)
    #position_datasets.append(ADCPPosition(cfg))


#%%
cfgs = []
position_datasets = []
adcps = []
for i,fpath in enumerate(pd0_fpaths):
    print(i)
    
    
    try:
        name = fpath.split(os.sep)[-1].split('.000')[0]
        cfg = {'filename':fpath,
               'name':name,
               'pos_cfg':pos_cfgs[i]}
        
        adcp = DatasetADCP(cfg, name = name)
        adcps.append(adcp)
    except:
        None
#%%


import numpy as np
from pyproj import Transformer
import contextily as ctx
from xyzservices import TileProvider, providers
from rasterio.enums import Resampling

import numpy as np
from pyproj import Transformer
import contextily as ctx



from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np
import contextily as ctx
from pyproj import Transformer
from rasterio.enums import Resampling

class ADCPTransectMap:
    def __init__(self, adcp_transects):
        self.adcp_transects = adcp_transects
        self._transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        self._collections = []  # Stores LineCollection objects for each transect

    def plot(self):
        fig, ax = PlottingShell.subplots()
        all_x, all_y = [], []

        # Normalize across all transects
        all_values = np.concatenate([
            adcp.get_absolute_backscatter().max(axis=2).max(axis=1)[:-1]
            for adcp in self.adcp_transects
        ])
        norm = Normalize(vmin=all_values.min(), vmax=all_values.max())

        self._collections.clear()

        for adcp in self.adcp_transects:
            lon = np.array(adcp.position.x)
            lat = np.array(adcp.position.y)
            x, y = self._transformer.transform(lon, lat)
            all_x.extend(x)
            all_y.extend(y)

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            color = adcp.get_absolute_backscatter().max(axis=2).max(axis=1)[:-1]

            lc = LineCollection(segments, array=color, cmap='turbo_r',
                                linewidth=2, norm=norm)
            ax.add_collection(lc)
            self._collections.append(lc)  # Store LineCollection

        x_min, x_max = np.min(all_x), np.max(all_x)
        y_min, y_max = np.min(all_y), np.max(all_y)
        x_pad = 0.05 * (x_max - x_min)
        y_pad = 0.05 * (y_max - y_min)
        ax.set_xlim(x_min - x_pad, x_max + x_pad)
        ax.set_ylim(y_min - y_pad, y_max + y_pad)

        ctx.add_basemap(ax, source=ctx.providers.CartoDB.PositronNoLabels,
                        crs="EPSG:3857", zoom=17, resampling=Resampling.bilinear)

        sm = plt.cm.ScalarMappable(cmap='turbo_r', norm=norm)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, label='Mean Absolute Backscatter')

        ax.set_aspect("equal")
        fig.tight_layout()

    
ADCPTransectMap(adcps).plot()

#%%
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import contextily as ctx
from pyproj import Transformer
import numpy as np

class ADCPMapCanvas(FigureCanvas):
    def __init__(self, adcps):
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
        self.norm = None
        self.hover_index = None
        self.selected_index = None
        self.hover_callback = None
        self.tolerance = 15  # pixel distance tolerance for hover detection

        self.backscatter_cache = []
        self.plot_transects()
        self.mpl_connect("motion_notify_event", self.on_hover)
        self.mpl_connect("button_press_event", self.on_click)

    def plot_transects(self):
        self.ax.clear()
        all_values = np.concatenate([
            adcp.get_absolute_backscatter().max(axis=2).max(axis=1)[:-1]
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
            color = adcp.get_absolute_backscatter().max(axis=2).max(axis=1)[:-1]
            self.backscatter_cache.append(color)

            lc = LineCollection(segments, array=color, cmap='turbo_r',
                                linewidth=2, norm=self.norm)
            self.ax.add_collection(lc)
            self.collections.append(lc)

        xrange = max(all_x) - min(all_x)
        yrange = max(all_y) - min(all_y)
        pad_x = 1 * xrange
        pad_y = 1 * yrange
        xlim = (min(all_x) - pad_x, max(all_x) + pad_x)
        ylim = (min(all_y) - pad_y, max(all_y) + pad_y)
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_ylim(min(all_y), max(all_y))
        ctx.add_basemap(self.ax, source=ctx.providers.CartoDB.PositronNoLabels,
                        crs="EPSG:3857", zoom=17, reset_extent=True)
        sm = plt.cm.ScalarMappable(cmap='turbo_r', norm=self.norm)
        sm.set_array([])
        self.fig.colorbar(sm, cax=self.cax, orientation='horizontal', label='Abs. Backscatter')
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
        if self.hover_index is not None:
            self.selected_index = self.hover_index
            self.update_colors()
            self.adcps[self.selected_index].plot.four_beam_flood_plot(variable='Absolute Backscatter')

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
                lc.set_cmap("turbo_r")
                lc.set_norm(self.norm)
        self.draw()


class ADCPMainWindow(QMainWindow):
    def __init__(self, adcps):
        super().__init__()
        self.setWindowTitle("ADCP Transect Viewer")
        self.canvas = ADCPMapCanvas(adcps)
        self.hover_label = QLabel("Hover index: None")
        self.canvas.hover_callback = self.update_hover_label

        layout = QVBoxLayout()
        layout.addWidget(self.canvas, stretch=1)
        layout.addWidget(self.hover_label, stretch=0)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_hover_label(self, index):
        if isinstance(index, int):
            name = self.canvas.adcps[index].name
            self.hover_label.setText(f"Hovering: {name}")
        else:
            self.hover_label.setText("Hovering: None")


# Usage example:
# import sys
# app = QApplication(sys.argv)
# window = ADCPMainWindow(adcps)
# window.show()
# sys.exit(app.exec_())



# Usage example:
import sys
app = QApplication(sys.argv)
window = ADCPMainWindow(adcps)
window.show()
sys.exit(app.exec_())
