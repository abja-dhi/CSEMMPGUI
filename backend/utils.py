import os
from mikecore.DfsuFile import DfsuFile
import numpy as np
import pandas as pd
import warnings
from typing import Union, Dict, Any
from matplotlib.tri import Triangulation, TriFinder
import logging
import tkinter as tk
from tkinter import ttk, messagebox
import pickle
    
from pathlib import Path
from typing import Dict, List, Tuple, Sequence

from .handlers import ErrorHandler

class Constants:
    """Global constants for the pyEMMP package."""
    _CFG_SUFFIX = ".cfg"
    _PD0_SUFFIX = [".pd0", ".000"]
    _TABLE_SUFFIX = [".csv", ".xlsx"]
    _SSC_PAR_SUFFIX = ".sscpar"
    _VALID_ENSEMBLE_NAMES = ('ECHO INTENSITY', 'PERCENT GOOD', 'CORRELATION MAGNITUDE', 'SIGNAL TO NOISE RATIO', 'ABSOLUTE BACKSCATTER')
    _ENSEMBLE_COUNT_THRESHOLD = 65536
    _DFSU_SUFFIX = [".dfsu"]
    _DFS0_SUFFIX = [".dfs0"]
    _LOW_NUMBER = -9.0e99
    _HIGH_NUMBER = 9.0e99
    _OLD_DATETIME = "1950-01-01T00:00:00"
    _FAR_DATETIME = "2100-01-01T00:00:00"
    
class Utils:
    @staticmethod
    def _validate_file_path(path: str | Path, suffix: str | Sequence[str] = ".cfg") -> Path:
        p = Path(path).expanduser().resolve()
        if not p.is_file():
            return None
        suffixes = ([suffix.lower()] if isinstance(suffix, str) else [s.lower() for s in suffix])

        if p.suffix.lower() not in suffixes:
            raise ValueError(
                f"Configuration file must have one of the following extensions: "
                f"{', '.join(suffixes)}"
            )
        return p

    @staticmethod
    def _parse_kv_file(path: Path) -> Dict[str, str]:
        kv: Dict[str, str] = {}
        with path.open("r", encoding="utf-8") as fh:
            for n, raw in enumerate(fh, 1):
                line = raw.split("#", 1)[0].strip()  # strip comments & whitespace
                if not line:
                    continue
                if "=" not in line:
                    raise ValueError(f"Malformed line {n} in '{path}': {raw!r}")
                key, value = (s.strip() for s in line.split("=", 1))
                if key in kv:
                    raise ValueError(f"Duplicate key '{key}' in '{path}'.")
                kv[key] = value
        if not kv:
            return None
        return kv
    
    @staticmethod
    def gen_rot_x(theta):
        """
        Generate a 3*3 matrix that rotates a vector by angle theta about the x-axis

        Parameters
        ----------
        theta : float
            angle to rotate by.

        Returns
        -------
        numpy array
            Rotation matrix (Rx).

        """
        theta = theta * np.pi / 180
        return np.array([(1, 0, 0), 
                         (0, np.cos(theta), -np.sin(theta)),
                         (0, np.sin(theta), np.cos(theta))])

    @staticmethod
    def gen_rot_y(theta):
        """
        Generate a 3*3 matrix that rotates a vector by angle theta about the y-axis

        Parameters
        ----------
        theta : float
            angle to rotate by.

        Returns
        -------
        numpy array
            Rotation matrix (Ry).

        """
        theta = theta * np.pi / 180
        return np.array([(np.cos(theta), 0, np.sin(theta)), 
                         (0, 1, 0),
                         (-np.sin(theta), 0, np.cos(theta))])

    @staticmethod
    def gen_rot_z(theta):
        """
        Generate a 3*3 matrix that rotates a vector by angle theta about the z-axis

        Parameters
        ----------
        theta : float
            angle to rotate by.

        Returns
        -------
        numpy array
            Rotation matrix (Rz).

        """
        theta = theta * np.pi / 180
        return np.array([(np.cos(theta), -np.sin(theta), 0), 
                         (np.sin(theta), np.cos(theta), 0),
                         (0, 0, 1)])
    

    @staticmethod
    def get_logger(name: str = "pyEMMP", log_file: str | Path = "pyEMMP.log") -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:  # Prevent adding handlers multiple times
            logger.setLevel(logging.DEBUG)
            
            fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            fh.setFormatter(formatter)
            
            logger.addHandler(fh)
        
        return logger

    @staticmethod
    def error(logger: logging.Logger, msg: str, exc: type, level: str) -> None:
        """
        Log an error message and raise an exception if provided.
        
        Parameters
        ----------
        msg : str
            The error message to log.
        exc : type, optional
            An exception to raise after logging the message.
        """
        logger.error(f"({level}) {msg}")
        if exc:
            raise exc(f"({level}) {msg}") from None

    @staticmethod
    def warning(logger: logging.Logger, msg: str, level: str) -> None:
        """
        Log an error message and raise an exception if provided.
        
        Parameters
        ----------
        msg : str
            The error message to log.
        exc : type, optional
            An exception to raise after logging the message.
        """
        logger.warning(f"({level}) {msg}")

    @staticmethod
    def info(logger: logging.Logger, msg: str, level: str) -> None:
        """
        Log an info message.
        
        Parameters
        ----------
        msg : str
            The info message to log.
        """
        logger.info(f"({level}) {msg}")
       
        
    @staticmethod
    def all_nan(arr: np.ndarray, logger: logging.Logger, msg: str, class_name: str, arrname: str = "x") -> None:
        """
        Check if all elements in the array are NaN and log a warning if true.
        
        Parameters
        ----------
        arr : np.ndarray
            The array to check.
        logger : logging.Logger
            The logger to use for logging the warning.
        msg : str
            The message to log if all values are NaN.
        """
        try:
            if np.all(np.isnan(arr)):
                Utils.warning(
                    logger=logger,
                    msg=msg,
                    level=class_name
                )
        except:
            try:
                if np.all([x is np.nan for x in arr]):
                    Utils.warning(
                        logger=logger,
                        msg=msg,
                        level=class_name
                    )
            except:
                Utils.error(
                    logger,
                    f"Error checking NaN values in array: {arrname} with type {type(arr)}",
                    ValueError,
                    level=class_name
                )

    @staticmethod
    def extern_to_csv_single(filepath: str | Path) -> int:
        colspecs = [
            (1, 11), (12, 25), (27, 50), (50, 70), (70, 93),
            (112, 135), (135, 162), (162, 170), (170, 195), (195, 220)
        ]
        column_names = [
            "Date", "Time", "Ensemble", "Latitude", "Longitude",
            "Speed", "Course", "PosFix", "EastVesselDisplacement", "NorthVesselDisplacement"
        ]

        
        fname = filepath.replace(".dat", ".csv")
        if os.path.exists(fname):
            print(f"File {fname} already exists, skipping.")
            return 1
        try:
            df = pd.read_fwf(filepath, colspecs=colspecs, names=column_names)
            df = df.iloc[1:]  # drop header row
            df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
            df = df.set_index("Datetime").drop(columns=["Date", "Time"])

            df["Ensemble"] = (
                df["Ensemble"]
                .str.replace("ENSEMBLE", "", case=False)
                .str.replace(":", "", regex=False)
                .str.strip()
                .astype(int)
            )

            float_cols = df.columns.difference(["Ensemble"])
            df[float_cols] = df[float_cols].astype(float)

            df["Latitude"] = df["Latitude"] / 3600
            df["Longitude"] = df["Longitude"] / 3600

            try:
                df.to_csv(fname, index_label="DateTime")
                return 0
            except Exception as e:
                print(f"Failed to save {fname}: {e}")
                return -1

        except Exception as e:
            print(f"Failed to read {filepath}: {e}")
            return -1


    def extern_to_csv_batch(directory):
        """
        Locate, parse, and convert all 'extern.dat' fixed-width files in a directory tree to CSV.
        
        Parameters
        ----------
        directory : str or Path
            Root directory to search recursively for extern.dat files.
        """
        n_success = 0
        n_failed = 0
        n_already_converted = 0
        print(f"Identifying extern.dat files within {directory}")
        files = [str(p) for p in Path(directory).rglob("*extern.dat")]
        print(f"Identified {len(files)} files. Parsing...")

        colspecs = [
            (1, 11), (12, 25), (27, 50), (50, 70), (70, 93),
            (112, 135), (135, 162), (162, 170), (170, 195), (195, 220)
        ]
        column_names = [
            "Date", "Time", "Ensemble", "Latitude", "Longitude",
            "Speed", "Course", "PosFix", "EastVesselDisplacement", "NorthVesselDisplacement"
        ]

        for file in files:
            fname = file.replace(".dat", ".csv")
            if os.path.exists(fname):
                print(f"File {fname} already exists, skipping.")
                n_already_converted += 1
                continue
            try:
                df = pd.read_fwf(file, colspecs=colspecs, names=column_names)
                df = df.iloc[1:]  # drop header row
                df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
                df = df.set_index("Datetime").drop(columns=["Date", "Time"])

                df["Ensemble"] = (
                    df["Ensemble"]
                    .str.replace("ENSEMBLE", "", case=False)
                    .str.replace(":", "", regex=False)
                    .str.strip()
                    .astype(int)
                )

                float_cols = df.columns.difference(["Ensemble"])
                df[float_cols] = df[float_cols].astype(float)

                df["Latitude"] = df["Latitude"] / 3600
                df["Longitude"] = df["Longitude"] / 3600

                try:
                    df.to_csv(fname, index_label="DateTime")
                    n_success += 1
                except Exception as e:
                    print(f"Failed to save {fname}: {e}")
                    n_failed += 1

            except Exception as e:
                print(f"Failed to read {file}: {e}")
                n_failed += 1
        return n_success, n_failed, n_already_converted

class ColumnSelectorGUI:
    def __init__(self, filepath: str, variables: list[str], description: str, skiprows: int = 0, sep: str = ',', header: int = 0, sheet_name: int = 0):
        """
        Initialize the GUI for selecting columns from a table.
        """
        self.logger = Utils.get_logger()
        self.filepath = Path(filepath)
        self.colfile = self.filepath.with_suffix('.col')
        self.skiprows = skiprows
        self.sep = sep
        self.header = header
        self.sheet_name = sheet_name
        self.variables = variables
        self.description = description
        if self.colfile.is_file():
            with open(self.colfile, 'rb') as f:
                self.selections = pickle.load(f)
                self.df = self._read_file()
                self._process()
                Utils.warning(
                    logger=self.logger,
                    msg=f"Column selections loaded from {self.colfile}.",
                    level=self.__class__.__name__
                )
        else:
            self.df = self._read_file()
            self.root = tk.Tk()
            self.root.title("Variable Selector")
            self.comboboxes = {}
            self.selections = None
            self.result = None
            self._build_gui()
            self.root.mainloop()

    def _read_file(self):
        if self.filepath.suffix == '.csv':
            try:
                return pd.read_csv(self.filepath, encoding='utf-8', skiprows=self.skiprows, sep=self.sep, index_col=False, header=self.header)
            except:
                try:
                    return pd.read_csv(self.filepath, encoding='utf-16', skiprows=self.skiprows, sep=self.sep, index_col=False, header=self.header)
                except:
                    return pd.read_csv(self.filepath, encoding='latin1', skiprows=self.skiprows, sep=self.sep, index_col=False, header=self.header)
        elif self.filepath.suffix in ['.xls', '.xlsx']:
            return pd.read_excel(self.filepath, skiprows=self.skiprows, index_col=False, header=self.header, sheet_name=self.sheet_name)
        else:
            Utils.error(
                logger=self.logger,
                msg=f"Unsupported file type: {self.filepath}. Supported types are: {Constants._TABLE_SUFFIX}",
                exc=ValueError,
                level=self.__class__.__name__
            )

    def _build_gui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=self.description, wraplength=400, foreground='blue').pack(anchor='w', pady=(0, 10))

        ttk.Label(frame, text="File Name:").pack(anchor='w')
        ttk.Label(frame, text=str(self.filepath), foreground='gray').pack(anchor='w', pady=(0, 10))

        for var in self.variables:
            ttk.Label(frame, text=var).pack(anchor='w')
            cb = ttk.Combobox(frame, values=self.df.columns.tolist(), state='readonly')
            cb.pack(fill='x', pady=(0, 10))
            self.comboboxes[var] = cb

        process_btn = ttk.Button(frame, text="Process", command=self._process)
        process_btn.pack(pady=(10, 0))

    def _process(self):
        if self.selections is None:
            self.selections = {var: cb.get() for var, cb in self.comboboxes.items()}
            if not all(self.selections.values()):
                Utils.error(
                    logger=self.logger,
                    msg=f"Please select all columns from {self.filepath}",
                    exc=ValueError,
                    level=self.__class__.__name__
                )
            with open(self.colfile, 'wb') as f:
                pickle.dump(self.selections, f)
            Utils.info(
                logger=self.logger,
                msg=f"Column selections saved to {self.colfile}.",
                level=self.__class__.__name__
            )
            self.root.destroy()
        self.result = self.df[[v for v in self.selections.values()]].copy()
        self.result.columns = list(self.selections.keys())
        

class CSVParser:
    COLUMNS = ["x", "y", "z", "t", "roll", "pitch", "heading"]
    _ALIAS_X = {"easting", "lon", "east", "longitude", "x"}
    _ALIAS_Y = {"northing", "north", "latitude", "lat", "y"}
    _ALIAS_Z = {"depth", "z", "elevation"}
    _ALIAS_T = {"times", "t", "time"}
    _ALIAS_ROLL = {"roll", "roll_angle", "rolling", "roll_angle_deg"}
    _ALIAS_PITCH = {"pitch", "pitch_angle", "pitching", "pitch_angle_deg"}
    _ALIAS_HEADING = {"heading", "heading_angle", "heading_deg", "hdg", "hdg_angle"}
    def __init__(self, fname: str | Path, cfg: Dict[str, Any]) -> None:
        self.fname = Utils._validate_file_path(fname, Constants._TABLE_SUFFIX)
        self._cfg = cfg
        self.requested_columns = self._cfg.get("requested_columns", None)
        self.header = self._cfg.get("header", 0)
        self.sep = self._cfg.get("sep", ",")
        if self.requested_columns is None:
            warnings.warn(
                f"Parsing all columns from {self.fname} by default. It is recommended to specify 'requested_columns' to improve performance.",
                RuntimeWarning,
                stacklevel=2,)
        self.df = self.parse()
        
        
    def parse(self) -> pd.DataFrame:
        """
        Parse the CSV file and return a DataFrame with canonical column names.
        
        Returns
        -------
        pd.DataFrame
            DataFrame with requested columns.
        """
        df = pd.read_csv(self.fname, header=self.header, sep=self.sep)
        if len(df.columns) == 0:
            raise ValueError(
                f"CSV file '{self.fname}' is empty or has no valid columns."
                )
        if self.requested_columns is None:
            self.requested_columns = df.columns.tolist()
        if len(df.columns) < len(self.requested_columns):
            raise ValueError(
                f"CSV file '{self.fname}' has only {len(df.columns)} columns but {len(self.requested_columns)} were requested."
                )
        df_columns = [self._map_aliases(col) for col in df.columns]
        df.columns = df_columns
        self.requested_columns = [self._map_aliases(col) for col in self.requested_columns]
        missing_columns = set(self.requested_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"CSV file '{self.fname}' is missing requested columns: {', '.join(missing_columns)}."
            )
        df = df[self.requested_columns]
        df['t'] = pd.to_datetime(df['t'], errors='coerce')
        return df
        
    
    def _map_aliases(self, col: str) -> str:
        """
        Map column aliases to canonical names.
        
        Parameters
        ----------
        col : str
            The column name to map.
        
        Returns
        -------
        str
            The canonical column name.
        """
        key = col.strip().lower()
        for elem in self._ALIAS_HEADING:
            if elem in key.lower():
                return "heading"
        for elem in self._ALIAS_PITCH:
            if elem in key.lower():
                return "pitch"
        for elem in self._ALIAS_ROLL:
            if elem in key.lower():
                return "roll"
        for elem in self._ALIAS_X:
            if elem in key.lower():
                return "x"
        for elem in self._ALIAS_Y:
            if elem in key.lower():
                return "y"
        for elem in self._ALIAS_Z:
            if elem in key.lower():
                return "z"
        for elem in self._ALIAS_T:
            if elem in key.lower():
                return "t"
        return col  # Return the original column name if no alias matches


    def _is_number(self, s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False
        
class XYZ:
    def __init__(self, x: float | np.ndarray, y: float | np.ndarray, z: float | np.ndarray) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.xy = np.array([x, y]).T
        self.xyz = np.array([x, y, z]).T

    def __repr__(self) -> str:
        return (
            f"XYZ(\n"
            f"Number of points: {len(self.x)}\n)"
        )