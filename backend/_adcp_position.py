from pathlib import Path
from typing import Union, Dict, Any, Tuple
import pyproj
import pandas as pd
from matplotlib.axes import Axes
import matplotlib.dates as mdates
import numpy as np

from .utils import Utils, Constants, XYZ
from .plotting import PlottingShell


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

        self.x = self._values["X"]
        self.y = self._values["Y"]
        self.z = self._values["Depth"]
        self.pitch = self._values["Pitch"]
        self.roll = self._values["Roll"]
        self.heading = self._values["Heading"]
        self._t = self._values["DateTime"]
        self._broadcast_constants_to_match_variable_dims()

        self._t = pd.to_datetime(self._t, errors='coerce')


    def _resample_to(self, new_times: np.ndarray) -> None:
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
        }, index=pd.to_datetime(self._t))

        df_resampled = df.reindex(new_times, method='nearest', tolerance=pd.Timedelta("30s"))
        if df_resampled.isnull().any().any():
            raise ValueError("Resampling failed for some timestamps. Consider adjusting tolerance.")

        self.x = df_resampled['x'].values
        self.y = df_resampled['y'].values
        self.z = df_resampled['z'].values
        self.pitch = df_resampled['pitch'].values
        self.roll = df_resampled['roll'].values
        self.heading = df_resampled['heading'].values
        self._t = new_times
        
    
    def _broadcast_constants_to_match_variable_dims(self) -> None:
        """
        Broadcast constant-valued position attributes to match the length of variable inputs.
        Assumes 'self.t' is variable and defines the target length.
        """
        if isinstance(self._t, (float, int)):
            raise RuntimeError("Cannot broadcast: 't' is constant and does not define a target length.")
    
        n = len(self._t)
        attrs = ['x', 'y', 'z', 'pitch', 'roll', 'heading']
    
        for attr in attrs:
            val = getattr(self, attr)
            if isinstance(val, (float, int)):
                setattr(self, attr, np.full(n, val, dtype=float))
                