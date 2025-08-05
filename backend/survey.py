from pathlib import Path
from typing import Dict, List, Union, Tuple
import os

from .utils import Utils, Constants
from .adcp import ADCP
from .ctd import CTD

class Survey:
    """Survey-level container that loads instruments from its config."""

    def __init__(self, cfg: dict) -> None:
        self._cfg = cfg
        self.name: str = self._cfg.get("name", "Survey")
        n_instruments = int(self._cfg.get("n_instruments", 0))
        inst_keys = [k for k in self._cfg if k.startswith("inst_") and not k.endswith("_type")]
        inst_type_keys = [k for k in self._cfg if k.endswith("_type")]
        self.instruments: Dict[str, Union[ADCP, CTD]] = {}
        for i, key in enumerate(inst_keys):
            instrument_number = key.split("_")[-1]
            inst_cfg = self._cfg_dir / self._cfg[key]
            inst_name = inst_cfg.stem
            inst_type = self._cfg[inst_type_keys[i]].lower()
            inst_cfg = Utils._validate_file_path(inst_cfg, Constants._CFG_SUFFIX)
            if inst_type == "adcp":
                # Read instrument specific configuration that are required to instantiate the ADCP object.
                inst = ADCP(cfg=inst_cfg, name=inst_name)
            elif inst_type == "ctd":
                # Read instrument specific configuration that are required to instantiate the CTD object.
                inst = CTD(cfg=inst_cfg, name=inst_name)
            setattr(self, inst.name, inst)
            self.instruments[inst.name] = inst

        mode_keys = {"automatic": "will be calculated automatically", "manual": "are defined manually"}
        type_keys = {1: "linear", 2: "quadratic", 3: "log-linear", 4: "exponential"}
        
        
        
    def _parse_sscpar(self, fname: str | Path) -> Dict[str, float]:
        """Parse coefficients from a file."""
        coefs = {}
        with open(fname, 'r') as f:
            for line in f:
                try:
                    key, value = line.strip().split(',')
                    coefs[key] = float(value)
                except ValueError:
                    pass
        del coefs["type"]
        return coefs
    
    
    

    
