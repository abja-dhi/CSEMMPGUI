import pandas as pd
import numpy as np
from mikecore.DfsuFile import DfsuFile
from matplotlib.tri import Triangulation, TriFinder
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patheffects as mpl_path_effects
import os
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Tuple, Union
from datetime import datetime
import matplotlib as mpl
import cycler

from .utils import CSVParser
from .utils_dfsu import DfsuUtils


class PlottingShell:
    _DATETIME_FORMAT = '%d-%b-%y %H:%M'
    _DATE_FORMAT = '%d-%b-%y'
    _TIME_FORMAT = '%H:%M'
    mpl.rcParams['font.size'] = 9
    mpl.rcParams['lines.linewidth'] = 2
    mpl.rcParams['lines.color'] = 'black'
    mpl.rcParams['patch.edgecolor'] = 'white'
    mpl.rcParams['axes.grid.which'] = 'major'
    mpl.rcParams['lines.markersize'] = 1.6
    mpl.rcParams['ytick.labelsize'] = 8
    mpl.rcParams['xtick.labelsize'] = 8
    mpl.rcParams['ytick.labelright'] = False
    mpl.rcParams['xtick.labeltop'] = False
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['ytick.major.right'] = True
    mpl.rcParams['xtick.major.top'] = True
    mpl.rcParams['axes.labelweight'] = 'normal'
    mpl.rcParams['legend.fontsize'] = 8
    mpl.rcParams['legend.framealpha']= 0.5
    mpl.rcParams['axes.titlesize'] = 12
    mpl.rcParams['axes.titleweight'] ='normal'
    mpl.rcParams['font.family'] ='TImes New Roman'
    mpl.rcParams['axes.labelsize'] = 10
    mpl.rcParams['axes.linewidth'] = 1.25
    mpl.rcParams['xtick.major.size'] = 5.0
    mpl.rcParams['xtick.minor.size'] = 3.0
    mpl.rcParams['ytick.major.size'] = 5.0
    mpl.rcParams['ytick.minor.size'] = 3.0
    colors = 2*['#283747','#0051a2', '#41ab5d', '#feb24c', '#93003a']
    line_style = 5*['-'] + 5*['--']
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color',colors) +cycler.cycler('linestyle',line_style)
    alpha = 0.7
    to_rgba = mpl.colors.ColorConverter().to_rgba#
    color_list=[]
    for i, col in enumerate(mpl.rcParams['axes.prop_cycle']):
        color_list.append(to_rgba(col['color'], alpha))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler(color=color_list)
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'

    @staticmethod
    def subplots(figheight: float = None, figwidth: float = None, nrow: int = None, ncol: int = None, sharex: bool = None, sharey: bool = None, width_ratios: list = None, height_ratios: list = None) -> Tuple[Figure, Union[Axes, np.ndarray]]:
        """
        Create a matplotlib figure with subplots and set default parameters.
        Parameters
        ----------
        figheight : float, optional
            Height of the figure in inches. Default is 4.25 * (1 + (5 ** 0.5)) / 2.
        figwidth : float, optional
            Width of the figure in inches. Default is equal to figheight.
        nrow : int, optional
            Number of rows of subplots. Default is 1.
        ncol : int, optional
            Number of columns of subplots. Default is 1.
        sharex : bool, optional
            Whether to share the x-axis among subplots. Default is False.
        sharey : bool, optional
            Whether to share the y-axis among subplots. Default is False.
        width_ratios : list, optional
            List of width ratios for the subplots. Default is equal width for all columns.
        height_ratios : list, optional
            List of height ratios for the subplots. Default is equal height for all rows.
        Returns
        -------
        fig : matplotlib.figure.Figure
            The created figure object.
        axs : numpy.ndarray
            Array of Axes objects for the subplots.
        """
        _FIGHEIGHT = 4.25 * (1 + (5 ** 0.5)) / 2
        _FIGWIDTH = _FIGHEIGHT
        _NROW = 1
        _NCOL = 1
        _SHAREX = False
        _SHAREY = False
        figheight = _FIGHEIGHT if figheight is None else figheight
        figwidth = _FIGWIDTH if figwidth is None else figwidth
        nrow = _NROW if nrow is None else max(1, nrow)
        ncol = _NCOL if ncol is None else max(1, ncol)
        sharex = _SHAREX if sharex is None else sharex
        sharey = _SHAREY if sharey is None else sharey
        width_ratios = [1] * ncol if width_ratios is None else width_ratios
        height_ratios = [1] * nrow if height_ratios is None else height_ratios
        fig, ax = plt.subplots(figsize=(figwidth, figheight), nrows=nrow, ncols=ncol, gridspec_kw={'width_ratios': width_ratios, 'height_ratios': height_ratios}, sharex=sharex, sharey=sharey)
        if nrow == 1 and ncol == 1:
            ax.grid(alpha=0.25)
        else:
            for a in ax.flatten():
                a.grid(alpha=0.25)

        return fig, ax

    @staticmethod
    def add_watermark(ax: Union[Axes, np.ndarray], watermark_text: str, add_date: bool = True) -> Union[Axes, np.ndarray]:
        path_effects = [mpl_path_effects.Stroke(linewidth=2, foreground="black", alpha=0.035)] 
        ax.text(0.5, 0.5, watermark_text, transform=ax.transAxes, fontsize=15, color='gray', alpha=0.1, ha='center', va='center', rotation=0, path_effects=path_effects, fontname='Arial', zorder=1)
        if add_date:
            ax.text(0.985, 0.02, os.getlogin() + '\n' + datetime.now().strftime("%d/%m/%y %H:%M"), transform=ax.transAxes, fontsize=6, color='black', alpha=0.4, ha='right', va='bottom', rotation=0, weight='bold', fontname=r'Arial', zorder=1)
        return ax
    
    @staticmethod
    def _mesh_plot(X: np.ndarray,
                   Y: np.ndarray,
                   C: np.ndarray,
                   vmin: float,
                   vmax: float,
                   cmap: str,
                   cbar_label: str,
                   orientation: str = "vertical",
                   location: str = "right",
                   extend: str = "max",
                   fraction: float = 0.046,
                   rotation: int = 90,
                   fontsize: int = 8,
                   T: np.ndarray = None,
                   Z: np.ndarray = None,
                   color: str = "black",
                   linewidth: float = 1.0,
                   alpha: float = 1.0,
                   Z_label: str = None,
                   ylim: Union[Tuple[float, float], None] = None,
                   ax: Axes = None,
                   ) -> Axes:
        """
        Create a mesh plot on the given axes.
        Parameters
        ----------
        X : np.ndarray
            The x-coordinates of the mesh grid.
        Y : np.ndarray
            The y-coordinates of the mesh grid.
        C : np.ndarray
            The values to be plotted on the mesh grid.
        vmin : float
            The minimum value for the color scale.
        vmax : float
            The maximum value for the color scale.
        cmap : str
            The colormap to use for the plot.
        cbar_label : str
            The label for the colorbar.
        orientation : str, optional
            The orientation of the colorbar, either 'vertical' or 'horizontal'. Default is 'vertical'.
        location : str, optional
            The location of the colorbar, either 'right', 'left', 'top', or 'bottom'. Default is 'right'.
        label_position : str, optional
            The position of the x-axis label, either 'bottom' or 'top'. Default is 'bottom'.
        fraction : float, optional
            The fraction of the original axes to use for the colorbar. Default is 0.046.
        rotation : int, optional
            The rotation angle for the colorbar label. Default is 90.
        fontsize : int, optional
            The font size for the colorbar label. Default is 8.
        T : np.ndarray, optional
            The x-coordinates for the top axis. If None, the x-coordinates from the mesh grid will be used.
        Z : np.ndarray, optional
            The z-coordinates for the mesh grid. If None, the z-coordinates from the mesh grid will be used.
        Z_label : str, optional
            The label for the z-axis. If None, no label will be added.
        ax : Axes, optional
            The matplotlib Axes object to plot on. If None, a new figure and axes will be created.
        Returns
        -------
        Axes
            The matplotlib Axes object with the mesh plot.
        """
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3, figwidth=10.5, sharex=True, sharey=True)
        else:
            fig = ax.figure
        im = ax.pcolor(X, Y, C, vmin=vmin, vmax=vmax, cmap=cmap)
        cbar = fig.colorbar(im, ax=ax, orientation=orientation, location=location, fraction=fraction, extend=extend)
        cbar.set_label(cbar_label, rotation=rotation, fontsize=fontsize)
        if T is not None:
            ax.plot(T, Z, label=Z_label, color=color, lw=linewidth, alpha=alpha)
        ax.grid(alpha=0.1)
        if ylim is None:
            ylim = (np.nanmin(Z), np.nanmax(Z))
        ax.set_ylim(ylim)
        ax.legend()
        return ax
        
    @staticmethod
    def _flood_plot(ax: Axes,
                    data: np.ndarray,
                    origin: str,
                    extent: np.ndarray,
                    cmap: mpl.colors.Colormap,
                    aspect: str,
                    resample: bool,
                    vmin: float,
                    vmax: float,
                    cbar_label: str = "",
                    orientation: str = "vertical",
                    rotation: int = 90,
                    fontsize: int = 8,
                    location: str = "right",
                    fraction: float = 0.046,
                    alpha: float = 0.1) -> Axes:
        im = ax.matshow(
                data,
                origin=origin,
                extent=extent,
                cmap=cmap,
                aspect=aspect,
                resample=resample,
                vmin=vmin,
                vmax=vmax,
            )
        fig = ax.figure
        cbar = fig.colorbar(im, ax=ax, orientation=orientation, location=location, fraction=fraction)
        cbar.set_label(cbar_label, rotation=rotation, fontsize=fontsize)
        ax.grid(alpha=alpha)
        
        return ax



class Curtain:
    def __init__(self, dfsu: str | DfsuFile, trajectory: str | pd.DataFrame | np.ndarray) -> None:
        if isinstance(dfsu, str):
            self.dfsu = DfsuFile(dfsu)
        elif isinstance(dfsu, DfsuFile):
            self.dfsu = dfsu
        else:
            raise TypeError("Input must be a string path to a dfsu file or a mikecore.DfsuFile object.")
        if isinstance(trajectory, (pd.DataFrame, str)):
            parser = CSVParser("trajectory")
            self.trajectory = parser.parse_trajectory(trajectory)
        elif isinstance(trajectory, np.ndarray):
            if trajectory.shape[1] != 3:
                raise ValueError("Trajectory array must have shape (n_points, 3) with x and y coordinates and time.")
            self.trajectory = pd.DataFrame(trajectory, columns=["x", "y", "t"])
            import warnings
            warnings.warn(
                "It is assumed that the trajectory array has columns for x, y, and time respectively.",
                RuntimeWarning,
                stacklevel=2,
            )
        else:
            raise TypeError("Trajectory must be a pandas DataFrame, a string path to a CSV file, or a numpy array.")
        self.dfsu_utils = DfsuUtils(self.dfsu)
        self.trajectory_times = self.trajectory['t'].values.astype('datetime64[ns]')    
        self.vertical_elements = self.dfsu_utils.find_elements_vertical(x=self.trajectory['x'].values, y=self.trajectory['y'].values)
        self.before_indices, self.after_indices = self.dfsu_utils.find_bracketing_timesteps(times=self.trajectory_times)

    def get_curtain_data(self, item_number: int = 2, unit_conversion: float = 1.0) -> np.ndarray:
        """
        Get the required data for the curtain plot.
        Args
        ----
            item_number (int): The item number to retrieve data for. Default is 2.
        Returns
        -------
            np.ndarray: The data for the specified item number.
        """
        if item_number < 1 or item_number > self.dfsu_utils.n_items:
            raise ValueError(f"Item number must be between 1 and {self.dfsu_utils.n_items}, got {item_number}.")
        vertical_columns = self.dfsu_utils.find_elements_vertical(x=self.trajectory['x'].values, y=self.trajectory['y'].values)
        raw_data = []
        for i in range(len(self.trajectory_times)):
            before_data = self.dfsu.ReadItemTimeStep(item_number, self.before_indices[i]).Data * unit_conversion
            after_data = self.dfsu.ReadItemTimeStep(item_number, self.after_indices[i]).Data * unit_conversion
            before_data = before_data[vertical_columns[i]]
            after_data = after_data[vertical_columns[i]]
            row_data = np.column_stack((before_data, after_data))
            raw_data.append(row_data)
        raw_data = np.array(raw_data)
        n_points, n_layers, _ = raw_data.shape
        
        data = np.empty((n_points, n_layers), dtype=float)
        model_times = self.dfsu_utils.model_times
        for i in range(n_points):
            t0 = model_times[self.before_indices[i]]
            t1 = model_times[self.after_indices[i]]
            t = self.trajectory_times[i]

            # Avoid division by zero if t0 == t1 (e.g., on exact timestamp)
            if t0 == t1:
                w0, w1 = 0.5, 0.5
            else:
                total = (t1 - t0) / np.timedelta64(1, 's')
                w0 = (t1 - t) / np.timedelta64(1, 's') / total
                w1 = (t - t0) / np.timedelta64(1, 's') / total

            vals = raw_data[i]  # shape (n_layers, 2)
            data[i] = vals[:, 0] * w0 + vals[:, 1] * w1
        return data
    
    def plot(self, ax=None, figsize=(12, 6), cmap='viridis', cbarlabel='Parameter', xlabel='Time', ylabel='Elevation (m)', title=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        # Convert times to matplotlib float
        time_nums = mdates.date2num(self.trajectory_times)

        # Create time edges
        time_edges = np.concatenate([
            [time_nums[0] - (time_nums[1] - time_nums[0]) / 2],
            (time_nums[1:] + time_nums[:-1]) / 2,
            [time_nums[-1] + (time_nums[-1] - time_nums[-2]) / 2]
        ])

        depth_grid = self.dfsu_utils.get_layer_elevations(self.trajectory['x'].values, self.trajectory['y'].values)
        data = self.get_curtain_data()
        # Create depth edges (layer boundaries) per vertical column
        # depth_grid: shape (n_points, n_layers)
        depth_edges = np.zeros((depth_grid.shape[0], depth_grid.shape[1] + 1))
        depth_edges[:, 1:-1] = (depth_grid[:, 1:] + depth_grid[:, :-1]) / 2
        depth_edges[:, 0] = depth_grid[:, 0] - (depth_grid[:, 1] - depth_grid[:, 0]) / 2
        depth_edges[:, -1] = depth_grid[:, -1] + (depth_grid[:, -1] - depth_grid[:, -2]) / 2

        # Meshgrid: value_grid.T is (n_layers, n_points)
        T, D = np.meshgrid(time_edges, depth_edges[0], indexing='xy')

        # Plot
        c = ax.pcolormesh(T, D, data.T, shading='auto', cmap=cmap)

        # ax.invert_yaxis()
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_title(title)

        ax.xaxis_date()
        fig.autofmt_xdate()

        cb = fig.colorbar(c, ax=ax)
        cb.set_label(cbarlabel)

        return ax