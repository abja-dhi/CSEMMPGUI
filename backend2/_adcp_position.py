from pathlib import Path
from typing import Union, Dict, Any, Tuple
import pyproj
import pandas as pd
from matplotlib.axes import Axes
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


from .utils import Utils, Constants, XYZ, ColumnSelectorGUI
from .plotting import PlottingShell

class PositionSetupGUI:
    _vars = ["X", "Y", "Depth", "Pitch", "Roll", "Heading"]

    def __init__(self, master=None):
        self.top = tk.Toplevel(master)
        self.top.title("Position data setup")
        self.top.grab_set()

        self.path = tk.StringVar()
        self.header = tk.IntVar(value=0)
        self.skiprows = tk.IntVar(value=0)
        self.sep = tk.StringVar(value=",")
        self.epsg = tk.IntVar(value=4326)

        self.df = None
        self.mode = {}
        self.value = {}
        self.widgets = {}
        self.row_index = {}
        self.datetime_row = None

        self._build()
        self.result = None
        self.top.wait_window()

    def _build(self):
        frm = ttk.Frame(self.top, padding=8)
        frm.grid(sticky="nsew")
        self.top.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)

        ttk.Label(frm, text="Position file").grid(row=0, column=0, sticky="e")
        ttk.Entry(frm, textvariable=self.path, state="readonly", width=55).grid(row=0, column=1, sticky="we")
        ttk.Button(frm, text="Select File", command=self._choose_file).grid(row=0, column=2, padx=4)
        ttk.Button(frm, text="Reset", command=self._reset).grid(row=0, column=3)

        self.opt_frame = ttk.Frame(frm)
        self.opt_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(6, 4))

        ttk.Label(frm, text="EPSG Code").grid(row=2, column=0, sticky="e")
        ttk.Entry(frm, textvariable=self.epsg, width=10).grid(row=2, column=1, sticky="w")

        self.var_frame = ttk.Frame(frm, borderwidth=1, relief="sunken")
        self.var_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=4)
        frm.rowconfigure(3, weight=1)
        self._make_var_rows(file_loaded=False)

        ttk.Button(frm, text="Save", command=self._on_save).grid(row=4, column=0, columnspan=4, sticky="ew", pady=4)

    def _choose_file(self):
        p = filedialog.askopenfilename(parent=self.top, title="CSV / Excel",
                                       filetypes=[("CSV/Excel", "*.csv *.xlsx *.xls")])
        if not p:
            return
        self.path.set(p)
        self._show_options_row()

    def _show_options_row(self):
        for w in self.opt_frame.winfo_children():
            w.destroy()
        ttk.Label(self.opt_frame, text="Header Row").grid(row=0, column=0, sticky="e")
        ttk.Entry(self.opt_frame, textvariable=self.header, width=4).grid(row=0, column=1, sticky="w")
        ttk.Label(self.opt_frame, text="Number of Rows to Skip").grid(row=0, column=2, sticky="e")
        ttk.Entry(self.opt_frame, textvariable=self.skiprows, width=4).grid(row=0, column=3, sticky="w")
        ttk.Label(self.opt_frame, text="Separator").grid(row=0, column=4, sticky="e")
        ttk.Entry(self.opt_frame, textvariable=self.sep, width=4).grid(row=0, column=5, sticky="w")
        ttk.Button(self.opt_frame, text="Process File", command=self._process_file).grid(row=0, column=6, padx=4)

    def _process_file(self):
        try:
            suf = Path(self.path.get()).suffix.lower()
            if suf in {".xls", ".xlsx"}:
                self.df = pd.read_excel(self.path.get(), skiprows=self.skiprows.get(), header=self.header.get())
            else:
                self.df = pd.read_csv(self.path.get(), skiprows=self.skiprows.get(), header=self.header.get(), sep=self.sep.get())
        except Exception as exc:
            messagebox.showerror("Read error", str(exc), parent=self.top)
            return

        self._make_var_rows(file_loaded=True)

    def _make_var_rows(self, file_loaded=False):
        for w in self.var_frame.winfo_children():
            w.destroy()
        self.mode.clear()
        self.value.clear()
        self.widgets.clear()
        self.row_index.clear()

        def add_row(var, r, allow_const=True, default_var=False):
            self.row_index[var] = r
            ttk.Label(self.var_frame, text=var).grid(row=r, column=0, sticky="e")
            m = tk.StringVar(value="Variable" if default_var else "Constant")
            self.mode[var] = m
            v = tk.StringVar()
            self.value[var] = v

            if default_var:
                w = ttk.Combobox(self.var_frame, textvariable=v, values=list(self.df.columns), state="readonly", width=25)
            else:
                w = ttk.Entry(self.var_frame, textvariable=v, width=25)
            w.grid(row=r, column=1, sticky="w")
            self.widgets[var] = w

            rb_const = ttk.Radiobutton(self.var_frame, text="Constant", variable=m, value="Constant",
                                       command=lambda v=var: self._swap_widget(v))
            rb_var = ttk.Radiobutton(self.var_frame, text="Variable", variable=m, value="Variable",
                                     command=lambda v=var: self._swap_widget(v))
            rb_const.grid(row=r, column=2); rb_var.grid(row=r, column=3)
            if not allow_const:
                rb_const.state(["disabled"])

            if file_loaded:
                rb_var.state(["!disabled"])
                if default_var:
                    m.set("Variable"); self._swap_widget(var)
            else:
                rb_var.state(["disabled"])

        r = 0
        for var in self._vars:
            add_row(var, r, allow_const=True, default_var=file_loaded)
            r += 1

        if file_loaded and any(self.mode[v].get() == "Variable" for v in self._vars):
            
            self._add_datetime_row(r)

    def _add_datetime_row(self, r):
        var = "DateTime"
        self.row_index[var] = r
        ttk.Label(self.var_frame, text=var).grid(row=r, column=0, sticky="e")
        m = tk.StringVar(value="Variable")
        v = tk.StringVar()
        self.mode[var] = m; self.value[var] = v

        w = ttk.Combobox(self.var_frame, textvariable=v, values=list(self.df.columns), state="readonly", width=25)
        w.grid(row=r, column=1, sticky="w")
        self.widgets[var] = w

        rb_const = ttk.Radiobutton(self.var_frame, text="Constant", variable=m, value="Constant")
        rb_const.grid(row=r, column=2)
        rb_const.state(["disabled"])
        rb_var = ttk.Radiobutton(self.var_frame, text="Variable", variable=m, value="Variable")
        rb_var.grid(row=r, column=3)
        self.datetime_row = r

    def _remove_datetime_row(self):
        var = "DateTime"
        if var in self.mode:
            row = self.row_index[var]
            for w in self.var_frame.grid_slaves(row=row):
                w.destroy()
            del self.mode[var], self.value[var], self.widgets[var], self.row_index[var]
            self.datetime_row = None

    def _swap_widget(self, var):
        row = self.row_index[var]
        old = self.widgets[var]; old.destroy()
        if self.mode[var].get() == "Constant":
            w = ttk.Entry(self.var_frame, textvariable=self.value[var], width=25)
        else:
            w = ttk.Combobox(self.var_frame, textvariable=self.value[var], values=list(self.df.columns), state="readonly", width=25)
        w.grid(row=row, column=1, sticky="w")
        self.widgets[var] = w

    def _reset(self):
        self.path.set(""); self.df = None
        self.header.set(0); self.skiprows.set(0); self.sep.set(",")
        for w in self.opt_frame.winfo_children():
            w.destroy()
        self._make_var_rows(file_loaded=False)

    def _on_save(self):
        if any(m.get() == "Variable" for m in self.mode.values()) and self.df is None:
            messagebox.showerror("Missing file", "Load and process a CSV/Excel file first.", parent=self.top)
            return

        mapping = {}
        for var in self.mode:
            if var == "DateTime" and self.mode[var].get() == "Constant":
                continue
            if self.mode[var].get() == "Constant":
                txt = self.value[var].get().strip()
                try:
                    val = float(txt)
                except ValueError:
                    messagebox.showerror("Invalid constant", f"{var}: enter a number.", parent=self.top); return
                mapping[var] = {"mode": "Constant", "value": val}
            else:
                col = self.value[var].get().strip()
                if not col:
                    messagebox.showerror("Missing column", f"Select column for {var}.", parent=self.top); return
                mapping[var] = {"mode": "Variable", "value": col}

        self.result = {
            "filename": self.path.get(),
            "header": self.header.get(),
            "skiprows": self.skiprows.get(),
            "sep": self.sep.get(),
            "epsg": self.epsg.get(),
        }
        for var, val in mapping.items():
            for key, value in val.items():
                self.result[f"{var}_{key}"] = value

        self.top.destroy()


class ADCPPosition:
    """
    Class to handle ADCP position data.
    
    Attributes:
        fname (str): Path to the position data file.
        epsg (int): EPSG code for the coordinate reference system.
    """
    _Vars = ["X", "Y", "Depth", "Pitch", "Roll", "Heading", "DateTime"]
    def __init__(self, cfg: Dict[str, Any]) -> None:
        self.logger = Utils.get_logger()
        _cfg = cfg
        fname = _cfg.get("position_data", "")
        fname = Utils._validate_file_path(fname, Constants._CFG_SUFFIX)
        self._cfg = Utils._parse_kv_file(fname)
        fname = self._cfg.get("filename", "")
        self.fname = Utils._validate_file_path(fname, Constants._TABLE_SUFFIX)
        self.extension = self.fname.suffix.lower()
        self.epsg = self._cfg.get("epsg", "4326")
        self.skiprows = int(self._cfg.get("skiprows", 0))
        self.sep = self._cfg.get("sep", ",")
        self.header = int(self._cfg.get("header", 0))

        self.modes = {}
        self.values = {}
        self.columns = {}

        for var in self._Vars:
            self.modes[var] = self._cfg.get(f"{var}_mode", "Variable")
            if self.modes[var] == "Variable":
                col = self._cfg.get(f"{var}_value", "")
                if col:
                    self.columns[var] = col
                else:
                    raise ValueError(f"Variable {var} is set to 'Variable' but no column is specified.")
            else:
                val = self._cfg.get(f"{var}_value", 0.0)
                self.values[var] = float(val)

        self.all_const = False
        if len(self.columns) == 0:
            self.all_const = True

        if not self.all_const:
            if self.fname.suffix.lower() == ".csv":
                self.df = pd.read_csv(self.fname, skiprows=self.skiprows, sep=self.sep, header=self.header)
            elif self.fname.suffix.lower() in {".xls", ".xlsx"}:
                self.df = pd.read_excel(self.fname, skiprows=self.skiprows, header=self.header)
            else:
                raise ValueError(f"Unsupported file format: {self.fname.suffix}. Supported formats are .csv, .xls, .xlsx.")
            for var in self.columns.keys():
                self.values[var] = self.df[self.columns[var]].to_numpy()
            

        
        #TODO: Add support for z_convention and resample_method
        # self.z_convention = self._cfg.get("z_convention", "normal")
        # self.resample_method = self._cfg.get("resample_method", "nearest")
        
        self.x = self.values["X"]
        self.y = self.values["Y"]
        self.z = self.values["Depth"]
        self.pitch = self.values["Pitch"]
        self.roll = self.values["Roll"]
        self.heading = self.values["Heading"]
        self.t = self.values["DateTime"]

        Utils.info(
            logger=self.logger,
            msg=f"ADCP position data loaded from {self.fname}",
            level=self.__class__.__name__
            )
            
        self.t = pd.to_datetime(self.t, errors='coerce')
        # self.coords = XYZ(x=self.df.x.to_numpy(), y=self.df.y.to_numpy(), z=self.df.z.to_numpy())

    def load(self) -> None:
        pass

    def plot_position(self, ax: Axes = None) -> Axes:
        if ax is None:
            fig, ax = PlottingShell.subplots()
        s = ax.scatter(self.df.x, self.df.y, s=5, c=self.df.z, cmap='jet_r')
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Northing (m)")
        ax.set_aspect('equal')
        ax.grid(alpha=0.3, color='white')
        ax.set_facecolor('lightgray')
        fig = ax.figure
        fig.colorbar(s, ax=ax, label='Depth (m)')
        return ax

    def plot_depth(self, ax: Axes = None) -> Axes:
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3.5, figwidth=10)
        ax.scatter(self.df.t, self.df.z, s=5, c=self.df.z, cmap='jet_r')
        ax.set_ylabel("Depth (m)")
        ax.grid(alpha=0.3, color='white')
        ax.set_facecolor('lightgray')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter(PlottingShell._DATETIME_FORMAT))
        return ax

    def plot_pitch_roll(self, ax: Axes = None) -> Axes:
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3.5, figwidth=10)
        ax.plot(self.df.t, self.df.pitch, lw=1, ls='--', c='black', alpha=0.9, label='Pitch')
        ax.plot(self.df.t, self.df.roll, lw=1, ls='-', c='black', alpha=0.9, label='Roll')
        ax.set_ylabel("Pitch/Roll (degrees)")
        ax.grid(alpha=0.3, color='white')
        ax.set_facecolor('lightgray')
        ax.legend(loc='upper right')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter(PlottingShell._DATETIME_FORMAT))
        return ax

    def plot(self, ax: Tuple[Axes, Axes, Axes]=None):
        """
        Plot the ADCP position data on the given axes.
        
        Parameters
        ----------
            ax (Tuple[Axes, Axes, Axes], optional): Axes to plot on. If None, a new figure and axes will be created.
        
        Returns
        -------
            Tuple[Axes, Axes, Axes]: The axes with the plotted data.
        """
        plot_position = False
        plot_depth = False
        plot_pitch_roll = False
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=3, ncol=1, figheight=8, figwidth=11)
            plot_position = True
            plot_depth = True
            plot_pitch_roll = True
        else:
            if isinstance(ax, Axes):
                ax = (ax)
                plot_position = True
            elif len(ax) == 2:
                plot_position = True
                plot_depth = True
            elif len(ax) == 3:
                plot_position = True
                plot_depth = True
                plot_pitch_roll = True
        if plot_position:
            ax[0] = self.plot_position(ax[0])
            ax[0].set_title("Position")
        if plot_depth:
            ax[1] = self.plot_depth(ax[1])
            ax[1].set_title("Depth")
        if plot_pitch_roll:
            ax[2] = self.plot_pitch_roll(ax[2])
            ax[2].set_title("Pitch and Roll")

        return ax

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(\n"
            f"fname={self.fname}\n"
            f"epsg={self.epsg}\n"
            f"columns={list(self.df.columns)}\n)"
        )