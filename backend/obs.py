import xml.etree.ElementTree as ET
import pandas as pd
from numpy.typing import NDArray
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np

class OBS():
    def __init__(self, cfg: str) -> None:
        self._cfg = ET.fromstring(cfg)
        self.id = self._cfg.attrib['id']
        self.name = self._cfg.attrib.get('name', '')
        filinfo = self._cfg.find("FileInfo")
        self._fname = filinfo.find("Path").text
        self._header = int(filinfo.find("HeaderLine").text)
        self._sep = filinfo.find("Delimiter").text
        self._date_col = filinfo.find("DateTimeColumn").text
        self._depth_col = filinfo.find("DepthColumn").text
        self._ntu_col = filinfo.find("NTUColumn").text
        masking = self._cfg.find("Masking")
        maskDateTime = masking.find("MaskDateTime")
        enabled = maskDateTime.attrib.get("enabled", "false").lower() == "true"
        dateTimeStart = maskDateTime.find("Start").text if enabled else datetime.min
        dateTimeEnd = maskDateTime.find("End").text if enabled else datetime.max
        maskDepth = masking.find("MaskDepth")
        enabled = maskDepth.attrib.get("enabled", "false").lower() == "true"
        depthMin = float(maskDepth.find("Min").text) if enabled else -np.inf
        depthMax = float(maskDepth.find("Max").text) if enabled else np.inf
        maskNTU = masking.find("MaskNTU")
        enabled = maskNTU.attrib.get("enabled", "false").lower() == "true"
        ntuMin = float(maskNTU.find("Min").text) if enabled else -np.inf
        ntuMax = float(maskNTU.find("Max").text) if enabled else np.inf

        df = pd.read_csv(self._fname, header=self._header, sep=self._sep)
        
        @dataclass
        class Data:
            datetime: NDArray[np.datetime64] = field(metadata={"desc": "Datetime values"})
            depth: NDArray[np.float64] = field(metadata={"desc": "Depth values"})
            ntu: NDArray[np.float64] = field(metadata={"desc": "NTU values"})

        self.data = Data(
            datetime=df[self._date_col].to_numpy(dtype=datetime),
            depth=df[self._depth_col].to_numpy(dtype=np.float64),
            ntu=df[self._ntu_col].to_numpy(dtype=np.float64)
        )

        @dataclass
        class MaskParams:
            dateTimeStart: datetime = field(metadata={"desc": "Start datetime for masking"})
            dateTimeEnd: datetime = field(metadata={"desc": "End datetime for masking"})
            depthMin: float = field(metadata={"desc": "Minimum depth for masking"})
            depthMax: float = field(metadata={"desc": "Maximum depth for masking"})
            ntuMin: float = field(metadata={"desc": "Minimum NTU for masking"})
            ntuMax: float = field(metadata={"desc": "Maximum NTU for masking"})
            OBSMask=None

        self.masking = MaskParams(
            start_datetime=pd.to_datetime(dateTimeStart),
            end_datetime=pd.to_datetime(dateTimeEnd),
            depthMin=depthMin,
            depthMax=depthMax,
            ntuMin=ntuMin,
            ntuMax=ntuMax
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