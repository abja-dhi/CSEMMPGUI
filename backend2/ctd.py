from pathlib import Path
from typing import Union
import pandas as pd

from .utils import Utils, Constants, ColumnSelectorGUI

class CTD:
    """
    Class to handle CTD (Conductivity, Temperature, Depth) data.
    """

    def __init__(self, cfg: str | Path) -> None:
        self.logger = Utils.get_logger()
        self._config_path = Utils._validate_file_path(cfg, Constants._CFG_SUFFIX)
        self._cfg = Utils._parse_kv_file(self._config_path)
        self.name: str = self._cfg.get("name", self._config_path.stem)
        self._csv_path: str = self._cfg.get("filename", None)
        if self._csv_path is None:
            Utils.error(
                logger=self.logger,
                msg=f"CTD config '{self._config_path}' must contain 'filename' entry with a valid path to a CSV file",
                exc=ValueError,
                level=self.__class__.__name__
            )
        else:
            self._csv_path = Utils._validate_file_path(self._csv_path, Constants._TABLE_SUFFIX)
        table = ColumnSelectorGUI(
            filepath=self._csv_path,
            variables=["t", "depth", "turbidity"],
            description="Select the columns from the CTD data file.",
            skiprows=int(self._cfg.get("skiprows", 0)),
            sep=self._cfg.get("sep", ","),
            header=int(self._cfg.get("header", 0)),
            sheet_name=self._cfg.get("sheet_name", 0)
        )
        self.data = table.result
        Utils.info(
            logger=self.logger,
            msg=f"CTD data loaded from {self._csv_path}",
            level=self.__class__.__name__
        )
        self.t = pd.to_datetime(self.data.t, errors='coerce').to_numpy().astype('datetime64[ns]')
        self.depth = self.data.depth.to_numpy()
        self.turbidity = self.data.turbidity.to_numpy()