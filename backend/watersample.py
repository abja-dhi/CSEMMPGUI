import xml.etree.ElementTree as ET
import pandas as pd
from numpy.typing import NDArray
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np

from utils import Constants

class WaterSample():
    # read in the water sample xml file as the corresponding XML element
    def __init__(self, cfg: ET) -> None:
        self.root = cfg

        self.name = self.root.attrib.get('name', "MyWaterSample")
        self.position = None
        rows = []
        for sample in self.root.findall("Sample"):
            rows.append(sample.attrib)
        df = pd.DataFrame(rows)

        @dataclass
        class WaterSampleData:
            datetime: NDArray[np.datetime64] = field(metadata={"desc": "Datetime values"})
            depth: NDArray[np.float64] = field(metadata={"desc": "Depth values"})
            ssc: NDArray[np.float64] = field(metadata={"desc": "SSC values"})

        self.data = WaterSampleData(
            datetime=df["DateTime"].to_numpy(dtype=np.datetime64),
            depth=df["Depth"].to_numpy(dtype=np.float64),
            ssc=df["SSC"].to_numpy(dtype=np.float64)
        )
        
        
        