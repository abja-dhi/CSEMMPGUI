from pathlib import Path
from typing import Union
import pandas as pd

from .utils import Utils, Constants

class CTD:
    """
    Class to handle CTD (Conductivity, Temperature, Depth) data.
    """

    def __init__(self, cfg: dict) -> None:
        self._cfg = cfg
        self.name: str = self._cfg.get("name", "CTD")
        self._csv_path: str = self._cfg.get("filename", None)
        self._t_column = self._cfg.get("t_column", "t")
        self._depth_column = self._cfg.get("depth_column", "depth")
        self._turbidity_column = self._cfg.get("turbidity_column", "turbidity")
        self._skiprows = self._cfg.get("skiprows", 0)
        self._header = self._cfg.get("header", 0)
        self.data = pd.read_csv(self._csv_path, usecols=[self._t_column, self._depth_column, self._turbidity_column], skiprows=self._skiprows, header=self._header)
        self.data.columns = ['t', 'depth', 'turbidity']
        self.t = pd.to_datetime(self.data.t, errors='coerce').to_numpy().astype('datetime64[ns]')
        self.depth = self.data.depth.to_numpy()
        self.turbidity = self.data.turbidity.to_numpy()