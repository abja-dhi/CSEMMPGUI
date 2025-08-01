from pathlib import Path
from typing import Union, Dict, Any, Tuple
import pyproj
import pandas as pd
from matplotlib.axes import Axes
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import numpy as np

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

    Attributes
    ----------
    fname : str
        Path to the position data file.
    epsg : int
        EPSG code for the coordinate reference system.
    """
    _Vars = ["X", "Y", "Depth", "Pitch", "Roll", "Heading", "DateTime"]

    def __init__(self, cfg: Dict[str, Any]) -> None:
        self._cfg = cfg
        fname = self._cfg.get("filename", "")
        self._fname = Utils._validate_file_path(fname, Constants._TABLE_SUFFIX)
        self._extension = self._fname.suffix.lower()
        self.epsg = self._cfg.get("epsg", "4326")
        self._skiprows = int(self._cfg.get("skiprows", 0))
        self._sep = self._cfg.get("sep", ",")
        self._header = int(self._cfg.get("header", 0))

        self._modes = {}
        self._values = {}
        self._columns = {}

        for var in self._Vars:
            self._modes[var] = self._cfg.get(f"{var}_mode", "Variable")
            if self._modes[var] == "Variable":
                col = self._cfg.get(f"{var}_value", "")
                if col:
                    self._columns[var] = col
                else:
                    raise ValueError(f"Variable {var} is set to 'Variable' but no column is specified.")
            else:
                val = self._cfg.get(f"{var}_value", 0.0)
                self._values[var] = float(val)

        self._all_const = len(self._columns) == 0

        if not self._all_const:
            if self._fname.suffix.lower() == ".csv":
                self._df = pd.read_csv(self._fname, skiprows=self._skiprows, sep=self._sep, header=self._header)
            elif self._fname.suffix.lower() in {".xls", ".xlsx"}:
                self._df = pd.read_excel(self._fname, skiprows=self._skiprows, header=self._header)
            else:
                raise ValueError(f"Unsupported file format: {self._fname.suffix}. Supported formats are .csv, .xls, .xlsx.")
            for var in self._columns.keys():
                self._values[var] = self._df[self._columns[var]].to_numpy()

        # self.z_convention = self._cfg.get("z_convention", "normal")
        # self.resample_method = self._cfg.get("resample_method", "nearest")

        self.x = self._values["X"]
        self.y = self._values["Y"]
        self.z = self._values["Depth"]
        self.pitch = self._values["Pitch"]
        self.roll = self._values["Roll"]
        self.heading = self._values["Heading"]
        self.t = self._values["DateTime"]
        self._broadcast_constants_to_match_variable_dims()

        self.t = pd.to_datetime(self.t, errors='coerce')

    def load(self) -> None:
        pass

    def resample_to(self, new_times: np.ndarray) -> None:
        """
        Resample position and orientation data to match a new datetime index.

        Parameters
        ----------
        new_times : pd.DatetimeIndex
            Target time series to resample to.
        """
        df = pd.DataFrame({
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'pitch': self.pitch,
            'roll': self.roll,
            'heading': self.heading
        }, index=pd.to_datetime(self.t))

        df_resampled = df.reindex(new_times, method='nearest', tolerance=pd.Timedelta("30s"))
        if df_resampled.isnull().any().any():
            raise ValueError("Resampling failed for some timestamps. Consider adjusting tolerance.")

        self.x = df_resampled['x'].values
        self.y = df_resampled['y'].values
        self.z = df_resampled['z'].values
        self.pitch = df_resampled['pitch'].values
        self.roll = df_resampled['roll'].values
        self.heading = df_resampled['heading'].values
        self.t = new_times
        #print(new_times)
        #print(f'New length is {len(self.t)}')
    
    def _broadcast_constants_to_match_variable_dims(self) -> None:
        """
        Broadcast constant-valued position attributes to match the length of variable inputs.
        Assumes 'self.t' is variable and defines the target length.
        """
        if isinstance(self.t, (float, int)):
            raise RuntimeError("Cannot broadcast: 't' is constant and does not define a target length.")
    
        n = len(self.t)
        attrs = ['x', 'y', 'z', 'pitch', 'roll', 'heading']
    
        for attr in attrs:
            val = getattr(self, attr)
            if isinstance(val, (float, int)):
                setattr(self, attr, np.full(n, val, dtype=float))
                


    def __repr__(self):
        return (
            f"{self.__class__.__name__}(\n"
            f"fname={self._fname}\n"
            f"epsg={self.epsg}\n"
            f"columns={list(self._df.columns)}\n)"
        )