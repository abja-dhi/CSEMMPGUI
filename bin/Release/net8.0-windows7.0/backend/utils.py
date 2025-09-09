import os
from mikecore.DfsuFile import DfsuFile
import numpy as np
import pandas as pd
import warnings
from typing import Union, Dict, Any, List, Tuple, Sequence
from matplotlib.tri import Triangulation, TriFinder
import pickle
from pathlib import Path
from mikecore.DfsFileFactory import DfsFileFactory
from mikecore.DfsuBuilder import DfsuBuilder, DfsuFileType
from mikecore.DfsFactory import DfsFactory
from mikecore.eum import eumQuantity, eumItem, eumUnit
from datetime import datetime, timedelta

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
    _FAR_PAST_DATETIME = "1950-01-01T00:00:00"
    _FAR_FUTURE_DATETIME = "2100-01-01T00:00:00"
    
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
            return f"File {fname} already exists, skipping."
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
                return True
            except Exception as e:
                return f"Failed to save {fname}: {e}"

        except Exception as e:
            return f"Failed to read {filepath}: {e}"

    @staticmethod
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
        files = [str(p) for p in Path(directory).rglob("*extern.dat")]
        
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
                    n_failed += 1

            except Exception as e:
                n_failed += 1
        return n_success, n_failed, n_already_converted

    @staticmethod
    def Dfs2ToDfsu(in_path, out_dfsu):
        """
        Convert a DFS2 file to a DFSU file.
        """
        # Check if out file already exists and give warning if true
        if os.path.exists(out_dfsu): 
            os.remove(out_dfsu)
        z_level = 0.0                 # node Z
        mask_with_nan = False         # drop cells where chosen item at t=0 is NaN
        item_for_mask = 1             # 1-based item index for mask
        
        
        # -------------------
        # open DFS2
        # -------------------
        
        dfs2 = DfsFileFactory.Dfs2FileOpen(str(in_path))
        
        # spatial axis
        ax = dfs2.SpatialAxis
        nx = int(ax.XCount); ny = int(ax.YCount)
        dx = float(ax.Dx);   dy = float(ax.Dy)
        x0 = float(ax.X0);   y0 = float(ax.Y0)
        theta_deg = float(getattr(ax, "Orientation", 0.0))
        ct = np.cos(np.deg2rad(theta_deg)); st = np.sin(np.deg2rad(theta_deg))
        
        # items
        n_items = len(dfs2.ItemInfo)
        
        # -------------------
        # time axis (FileInfo.TimeAxis)
        # -------------------
        ta = dfs2.FileInfo.TimeAxis  # .NET temporal axis
        def _times_seconds(ta_obj):
            dt_attr = getattr(ta_obj, "TimeStep", None)
            n_attr = getattr(ta_obj, "NumberOfTimeSteps", None) or getattr(ta_obj, "Count", None)
            if (dt_attr is not None) and (n_attr is not None):
                n = int(n_attr)
                dt_s = float(dt_attr)
                return np.arange(n, dtype=float) * dt_s
            times = getattr(ta_obj, "Times", None)  # seconds since start if present
            if times is not None:
                return np.asarray(list(times), dtype=float)
            # fallback: probe by reads
            t = []
            it = 0
            while True:
                try:
                    dfs2.ReadItemTimeStep(1, it)
                    t.append(float(it))
                    it += 1
                except: break
            return np.asarray(t, dtype=float)
        
        start_time = getattr(ta, "StartDateTime", None)
        if not isinstance(start_time, datetime):
            start_time = datetime(2000, 1, 1)
        
        tsec = _times_seconds(ta).astype(float)
        n_steps = int(tsec.size) if tsec.size else 1
        if tsec.size == 0:
            tsec = np.array([0.0], dtype=float)
        dt_header = float(tsec[1] - tsec[0]) if n_steps > 1 else 1.0
        
        # -------------------
        # nodes (corner grid) with rotation about (x0,y0)
        # -------------------
        
        ii = np.arange(nx + 1, dtype=float)
        jj = np.arange(ny + 1, dtype=float)
        X = x0 + ii[None, :] * dx
        Y = y0 + jj[:, None] * dy
        Xr = x0 + ct * (X - x0) - st * (Y - y0)
        Yr = y0 + st * (X - x0) + ct * (Y - y0)
        
        node_id = (np.arange((ny + 1) * (nx + 1)).reshape(ny + 1, nx + 1) + 1).astype(np.int32)
        
        
        # -------------------
        # elements as quads [n1,n2,n3,n4] CCW, 1-based indices
        # -------------------
        
        elements = []
        for j in range(ny):
            for i in range(nx):
                n00 = node_id[j,     i    ]
                n10 = node_id[j,     i + 1]
                n11 = node_id[j + 1, i + 1]
                n01 = node_id[j + 1, i    ]
                elements.append(np.asarray([n00, n10, n11, n01], dtype=np.int32))
        
        n_elem = len(elements)
        n_node = (ny + 1) * (nx + 1)
        if n_elem == 0:
            return "No valid cells to convert."
        
        # -------------------
        # flatten nodes
        # -------------------
        Xn = Xr.ravel(order="C").astype(np.float64)
        Yn = Yr.ravel(order="C").astype(np.float64)
        Zn = np.full(n_node, z_level, dtype=np.float32)
        codes = np.ones(n_node, dtype=np.int32)  # 1 = water
        
        # -------------------
        # projection
        # -------------------
        proj_str = dfs2.FileInfo.Projection.WKTString
        proj = DfsFactory().CreateProjection(proj_str)
        
        # pick 2D dfsu enum member
        two_d = None
        for m in DfsuFileType:
            if "2D" in m.name.upper() or "MESH2" in m.name.upper():
                two_d = m
                break
        if two_d is None:
            for name in ("Dfsu2D", "Mesh2D", "Type2D", "TwoD"):
                try:
                    two_d = getattr(DfsuFileType, name)
                    break
                except:
                    return 'Not a Dfs2 file'
        if two_d is None:
            return "No 2D DfsuFileType found."
        
        # -------------------
        # build DFSU (clone item schema)
        # -------------------
        builder = DfsuBuilder.Create(two_d)
        builder.SetNodes(Xn, Yn, Zn, codes)
        builder.SetElements(elements)
        builder.SetProjection(proj)
        builder.SetTimeInfo(start_time, float(dt_header))
        
        # find all items in the dfs2
        for k in range(n_items):
            info = dfs2.ItemInfo[k]
            name = getattr(info, "Name", f"item{k+1}")
            qty = getattr(info, "Quantity", None)
            if qty is None:
                qty = eumQuantity.Create(eumItem.eumIGeneral, eumUnit.eumUunitUndefined)
            builder.AddDynamicItem(name, qty)
            
        dfsu = builder.CreateFile(str(out_dfsu))
        # -------------------
        # stream data
        # ------------------
        for it in range(n_steps):
            t_sec = float(tsec[it])
            for k in range(1, n_items + 1):  # 1-based
                vals = dfs2.ReadItemTimeStep(k, it).Data  # len nx*ny
                mask = vals == dfs2.FileInfo.DeleteValueFloat
                vals[mask] = dfsu.DeleteValueFloat
                elem_vals = vals.reshape(ny, nx).ravel(order="C").astype(np.float32, copy=False)
                dfsu.WriteItemTimeStepNext(t_sec, elem_vals)
        dfsu.Close()
        dfs2.Close()
        
        return True

class ColumnSelectorGUI:
    def __init__(self, filepath: str, variables: list[str], description: str, skiprows: int = 0, sep: str = ',', header: int = 0, sheet_name: int = 0):
        """
        Initialize the GUI for selecting columns from a table.
        """
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
                
        else:
            self.df = self._read_file()
            self.comboboxes = {}
            self.selections = None
            self.result = None
            

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
        

    

    def _process(self):
        if self.selections is None:
            self.selections = {var: cb.get() for var, cb in self.comboboxes.items()}
            with open(self.colfile, 'wb') as f:
                pickle.dump(self.selections, f)
            
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
    'class for efficient handling of x,y,z data'
    def __init__(self, x: float | np.ndarray, y: float | np.ndarray, z: float | np.ndarray) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.xy = np.array([x, y]).T
        self.xyz = np.array([x, y, z]).T