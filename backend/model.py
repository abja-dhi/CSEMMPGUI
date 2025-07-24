from pathlib import Path
from typing import Union
import numpy as np
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from .utils import Utils, Constants
from .utils_dfsu import DfsuUtils
from .plotting import PlottingShell

class ModelSetupGUI:
    """Top-level GUI for creating a model configuration."""

    def __init__(self, name: str) -> None:
        self.root = tk.Tk()
        self.root.title(f"Model Configuration - {name}")

        self.model_name = tk.StringVar(value=name)
        self.filename = tk.StringVar()

        self.config_path: Path = None
        self._build_gui()
        self.root.mainloop()

    def _build_gui(self) -> None:
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(sticky="nsew")
        self.root.columnconfigure(0, weight=1)

        # Model name (readonly)
        ttk.Label(frm, text="Model Name").grid(row=0, column=0, sticky="e")
        name_entry = ttk.Entry(frm, textvariable=self.model_name, width=30, state="readonly")
        name_entry.grid(row=0, column=1, pady=4, sticky="w")

        # File selection
        ttk.Label(frm, text="Model File").grid(row=1, column=0, sticky="e")
        file_entry = ttk.Entry(frm, textvariable=self.filename, width=30)
        file_entry.grid(row=1, column=1, pady=4, sticky="w")

        browse_btn = ttk.Button(frm, text="Browse", command=self._browse_file)
        browse_btn.grid(row=1, column=2, padx=5)

        # Save button
        ttk.Button(frm, text="Save", command=self._on_save).grid(
            row=2, column=0, columnspan=3, sticky="ew", pady=6
        )

    def _browse_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select Model File",
            filetypes=[("DFS-U Files", "*.dfsu")],
        )
        if file_path:
            self.filename.set(file_path)

    def _on_save(self) -> None:
        name = self.model_name.get().strip()
        filename = self.filename.get().strip()

        if not filename:
            messagebox.showerror("Input Error", "Model file cannot be empty.")
            return

        cfg_dir = Path(os.getcwd())
        model_cfg_path = cfg_dir / f"{name}.cfg"

        lines = [
            f"# Model configuration for {name}",
            f"name = {name}",
            f"filename = {filename}",
        ]

        try:
            model_cfg_path.write_text("\n".join(lines), encoding="utf-8")
            self.config_path = model_cfg_path
        except OSError as exc:
            messagebox.showerror("File Error", f"Cannot write config: {exc}")
            return

        self.root.destroy()

class Model:
    def __init__(self, cfg: str | Path, name: str) -> None:
        self.logger = Utils.get_logger()
        self._config_path = Utils._validate_file_path(cfg, Constants._CFG_SUFFIX)
        if self._config_path is None:
            gui = ModelSetupGUI(name=name)
            self._config_path = gui.config_path
        self._cfg = Utils._parse_kv_file(self._config_path)
        if self._cfg is None:
            gui = ModelSetupGUI(name=name)
            self._config_path = gui.config_path
            self._cfg = Utils._parse_kv_file(self._config_path)
        self.name: str = self._cfg.get("name", self._config_path.stem)
        self.fname: str = self._cfg.get("filename", None)
        if self.fname is None:
            Utils.error(
                logger=self.logger,
                msg=f"Model config '{self._config_path}' must contain 'filename' entry with a valid path to a .dfsu file",
                exc=ValueError,
                level=self.__class__.__name__
            )
        self.fname = Utils._validate_file_path(self.fname, Constants._DFSU_SUFFIX).__str__()
        self.dfsu = DfsuUtils(self.fname)
        self.print_info()
        self.plot = Plotting(self)


    # ------------------------------------------------------------------ #
    # Properties                                                          #
    # ------------------------------------------------------------------ #
    @property
    def config_path(self) -> Path:
        """Resolved path to the configuration file."""
        return self._config_path

    # ------------------------------------------------------------------ #
    # Methods                                                            #
    # ------------------------------------------------------------------ #
    def print_info(self) -> None:
        """
        Print information about the model.
        """
        self._print_info(msg=f"Model '{self.name}' loaded from {self.fname}")
        self._print_info(msg=f"Model '{self.name}' number of items: {self.dfsu.n_items}")
        self._print_info(msg=f"Model '{self.name}' number of timesteps: {self.dfsu.n_timesteps}")
        self._print_info(msg=f"Model '{self.name}' number of nodes in 3D domain: {self.dfsu.n_nodes}")
        self._print_info(msg=f"Model '{self.name}' number of elements in 3D domain: {self.dfsu.n_elements}")
        self._print_info(msg=f"Model '{self.name}' number of vertical layers: {self.dfsu.n_layers}")
        self._print_info(msg=f"Model '{self.name}' number of nodes in 2D domain: {self.dfsu.n_nodes_2d}")
        self._print_info(msg=f"Model '{self.name}' number of elements in 2D domain: {self.dfsu.n_elements_2d}")
        
    def _print_info(self, msg: str) -> None:
        Utils.info(
            logger=self.logger,
            msg=msg,
            level=self.__class__.__name__
        )

    def extract_transect(self, x: np.ndarray, y: np.ndarray, t: np.ndarray, item_number: int) -> np.ndarray:
        """
        Extract a transect from the model data.
        Parameters
        ----------
        x : np.ndarray
            X coordinates of the transect points.
        y : np.ndarray
            Y coordinates of the transect points.
        t : np.ndarray
            Time values for the transect points.
        item_number : int
            Item number to extract from the model data.
        Returns
        -------
        np.ndarray
            Extracted transect data.
        """
        data, _, _ = self.dfsu.extract_transect(x=x, y=y, t=t, item_number=item_number)
        return data

    # ------------------------------------------------------------------ #
    # Magic methods                                                       #
    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}(\n"
            f"name='{self.name}'\n)"
            f"config_path='{self._config_path}'\n"
            )
    
from matplotlib.axes import Axes
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

class Plotting:
    

    def __init__(self, model: Model) -> None:
        self.model = model
        self.logger = Utils.get_logger()

    def transect(self, x: np.ndarray, y: np.ndarray, t: np.ndarray, item_number: int, ax: Axes=None, cmap: str=None, cbar_label: str=None) -> Axes:
        """
        Plot a transect from the model data.
        Parameters
        ----------
        x : np.ndarray
            X coordinates of the transect points.
        y : np.ndarray
            Y coordinates of the transect points.
        t : np.ndarray
            Time values for the transect points.
        item_number : int
            Item number to extract from the model data.
        """
        data, t, vertical_columns = self.model.dfsu.extract_transect(x=x, y=y, t=t, item_number=item_number)
        vert = vertical_columns[:, [0, -1]]
        ec = np.stack(self.model.dfsu.dfsu.CalculateElementCenterCoordinates()).T
        layer_fractions = self.model.dfsu.sigma_fractions
        Zs = ec[vert, 2]
        depth = Zs[:, 1] - Zs[:, 0]
        layer_bounds = np.concatenate(([0], np.cumsum(layer_fractions)))
        z_bounds = (Zs[:, 0] + depth * layer_bounds[:, None]).T
        t = t[:, np.newaxis].repeat(layer_fractions.shape[0]+1, axis=1)
        ylim = [np.min(Zs), np.max(Zs)]
        xlim = mdates.date2num(t)
        extent = [xlim[0], xlim[-1], ylim[0], ylim[-1]]
        vmin = np.nanmin(data)
        vmax = np.nanmax(data)
        origin = 'lower'
        cmap = cmap if cmap is not None else plt.cm.turbo
        cbar_label = cbar_label if cbar_label is not None else self.model.dfsu.dfsu.ItemInfo[item_number-1].Name
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3, figwidth=10.5)
        else:
            fig = ax.figure
        
        ax = PlottingShell._mesh_plot(
            X=t,
            Y=z_bounds,
            C=data[1:, :],
            vmin=vmin,
            vmax=vmax,
            cmap=cmap,
            cbar_label=cbar_label,
            ax=ax,
        )

        return ax