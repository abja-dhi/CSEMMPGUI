import xml.etree.ElementTree as ET
import pandas as pd
from numpy.typing import NDArray
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
from dateutil import parser

from .utils import Constants

class OBS():
    def __init__(self, cfg: str) -> None:
        self._cfg = cfg
        self.name = self._cfg.get('name', "MyOBS")
        self.filename = self._cfg.get('filename', None)
        header = self._cfg.get('header', 0)
        sep = self._cfg.get('sep', ',')
        if sep == "Tab":
            sep = "\t"
        elif sep == "WhiteSpaces":
            sep = "\s+"
        df = pd.read_csv(self.filename, header=header, sep=sep, skiprows=header-1)
        
        date_col = self._cfg.get('date_col', 'Date')
        time_col = self._cfg.get('time_col', 'Time')
        depth_col = self._cfg.get('depth_col', 'Depth')
        ntu_col = self._cfg.get('ntu_col', 'NTU')
        df["DateTime"] = pd.to_datetime(df[date_col] + ' ' + df[time_col], errors='coerce')
        df.drop(columns=[date_col, time_col], inplace=True)

        @dataclass
        class OBSData:
            datetime: NDArray[np.datetime64] = field(metadata={"desc": "Datetime values"})
            depth: NDArray[np.float64] = field(metadata={"desc": "Depth values"})
            ntu: NDArray[np.float64] = field(metadata={"desc": "NTU values"})

        self.data = OBSData(
            datetime=df["DateTime"].to_numpy(dtype=np.datetime64),
            depth=df[depth_col].to_numpy(dtype=np.float64),
            ntu=df[ntu_col].to_numpy(dtype=np.float64)
        )
        
        
        @dataclass
        class MaskParams:
            start_datetime: datetime = field(metadata={"desc": "Start datetime for masking"})
            end_datetime: datetime = field(metadata={"desc": "End datetime for masking"})
            depthMin: float = field(metadata={"desc": "Minimum depth for masking"})
            depthMax: float = field(metadata={"desc": "Maximum depth for masking"})
            ntuMin: float = field(metadata={"desc": "Minimum NTU for masking"})
            ntuMax: float = field(metadata={"desc": "Maximum NTU for masking"})
            OBSMask: NDArray = field(metadata={"desc": "Mask for OBS data"})

        self.masking = MaskParams(
            start_datetime=np.datetime64(parser.parse(self._cfg.get('start_datetime', Constants._FAR_PAST_DATETIME))),
            end_datetime=np.datetime64(parser.parse(self._cfg.get('end_datetime', Constants._FAR_FUTURE_DATETIME))),
            depthMin=self._cfg.get('depthMin', Constants._LOW_NUMBER),
            depthMax=self._cfg.get('depthMax', Constants._HIGH_NUMBER),
            ntuMin=self._cfg.get('ntuMin', Constants._LOW_NUMBER),
            ntuMax=self._cfg.get('ntuMax', Constants._HIGH_NUMBER),
            OBSMask=None
        )

        self.generate_OBSMask()


    def generate_OBSMask(self):
        datetimes = self.data.datetime
        datetime_mask = (datetimes >= self.masking.start_datetime) & (datetimes <= self.masking.end_datetime)

        depths = self.data.depth
        depth_mask = (depths >= self.masking.depthMin) & (depths <= self.masking.depthMax)

        ntus = self.data.ntu
        ntu_mask = (ntus >= self.masking.ntuMin) & (ntus <= self.masking.ntuMax)

        master_mask = np.logical_or.reduce([datetime_mask, depth_mask, ntu_mask])
        self.masking.OBSMask = master_mask