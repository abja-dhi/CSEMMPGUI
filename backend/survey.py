from pathlib import Path
from typing import Dict, List, Union, Tuple
import os

from .utils import Utils, Constants
from .adcp import ADCP
from .ctd import CTD

class Survey:
    """Survey-level container that loads instruments from its config."""

    def __init__(self, cfg: str | Path, name: str = None) -> None:
        self.logger = Utils.get_logger()
        self._config_path = Utils._validate_file_path(cfg, Constants._CFG_SUFFIX)
        if self._config_path is None:
            #gui = SurveySetupGUI(name=name)
            self._config_path = gui.config_path
        self._cfg = Utils._parse_kv_file(self._config_path)
        if self._cfg is None:
            #gui = SurveySetupGUI(name=name)
            self._config_path = gui.config_path
            self._cfg = Utils._parse_kv_file(self._config_path)
        self._cfg_dir = self._config_path.parent
        

        self.name: str = self._cfg.get("name", self._config_path.stem)
        Utils.info(logger=self.logger,
                   msg=f"Initializing Survey: {self.name} from {self._config_path}",
                   level=self.__class__.__name__
                   )
        n_instruments = int(self._cfg.get("n_instruments", 0))
        if n_instruments < 1:
            Utils.error(
                logger=self.logger,
                msg=f"{self.name}: n_instruments={n_instruments} but must be at least 1 in '{self._config_path}'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        Utils.info(
            logger=self.logger,
            msg=f"Found {n_instruments} instruments in the {self.name} survey configuration.",
            level=self.__class__.__name__
        )
        inst_keys = [k for k in self._cfg if k.startswith("inst_") and not k.endswith("_type")]
        inst_type_keys = [k for k in self._cfg if k.endswith("_type")]
        if len(inst_keys) != n_instruments:
            Utils.error(
                logger=self.logger,
                msg=f"{self.name}: n_instruments={n_instruments} but {len(inst_keys)} instrument entries found in '{self._config_path}'.",
                exc=ValueError,
                level=self.__class__.__name__
            )

        self.instruments: Dict[str, Union[ADCP, CTD]] = {}
        for i, key in enumerate(inst_keys):
            instrument_number = key.split("_")[-1]
            inst_cfg = self._cfg_dir / self._cfg[key]
            inst_name = inst_cfg.stem
            inst_type = self._cfg[inst_type_keys[i]].lower()
            inst_cfg = Utils._validate_file_path(inst_cfg, Constants._CFG_SUFFIX)
            Utils.info(
                logger=self.logger,
                msg=f"Instrument {instrument_number} configuration file: {inst_cfg}",
                level=self.__class__.__name__
            )
            if inst_type == "adcp":
                # Read instrument specific configuration that are required to instantiate the ADCP object.
                inst = ADCP(cfg=inst_cfg, name=inst_name)
            elif inst_type == "ctd":
                # Read instrument specific configuration that are required to instantiate the CTD object.
                inst = CTD(cfg=inst_cfg, name=inst_name)
            else:
                Utils.error(
                    logger=self.logger,
                    msg=f"{self.name}: Instrument type '{inst_type}' not recognized in '{inst_cfg}'.",
                    exc=ValueError,
                    level=self.__class__.__name__
                )
            if hasattr(self, inst.name):
                Utils.error(
                    logger=self.logger,
                    msg=f"Attribute '{inst.name}' already exists in Survey. Instruments must have unique names.",
                    exc=AttributeError,
                    level=self.__class__.__name__
                )
            setattr(self, inst.name, inst)
            self.instruments[inst.name] = inst

        mode_keys = {"automatic": "will be calculated automatically", "manual": "are defined manually"}
        type_keys = {1: "linear", 2: "quadratic", 3: "log-linear", 4: "exponential"}
        
        self.ntu_ssc_mode: str = self._cfg.get("ntu_ssc_mode", "automatic")
        self.ntu_ssc_eqtype: int = int(self._cfg.get("ntu_ssc_eqtype", 1))

        Utils.info(
            logger=self.logger,
            msg=f"{self.name}: NTU-SSC coefficients {mode_keys[self.ntu_ssc_mode]}",
            level=self.__class__.__name__
        )
        Utils.info(
            logger=self.logger,
            msg=f"{self.name}: NTU-SSC equation type is {type_keys[self.ntu_ssc_eqtype]}",
            level=self.__class__.__name__
        )

        if self.ntu_ssc_mode == "manual":
            self.ntu_ssc_coefs = self._cfg.get("ntu_ssc_file", None)
            self.ntu_ssc_coefs = Utils._validate_file_path(self.ntu_ssc_coefs, Constants._SSC_PAR_SUFFIX)
            self.ntu_ssc_coefs = self._parse_sscpar(self.ntu_ssc_coefs)
            for key, value in self.ntu_ssc_coefs.items():
                Utils.info(
                    logger=self.logger,
                    msg=f"{self.name}: NTU-SSC coefficient '{key}' = {value}",
                    level=self.__class__.__name__
                )
            

        self.bs_ssc_mode: str = self._cfg.get("bs_ssc_mode", "automatic")
        self.bs_ssc_eqtype: int = int(self._cfg.get("bs_ssc_eqtype", 1))

        Utils.info(
            logger=self.logger,
            msg=f"{self.name}: Backscatter-SSC coefficients {mode_keys[self.bs_ssc_mode]}",
            level=self.__class__.__name__
        )
        Utils.info(
            logger=self.logger,
            msg=f"{self.name}: Backscatter-SSC equation type is {type_keys[self.bs_ssc_eqtype]}",
            level=self.__class__.__name__
        )

        if self.bs_ssc_mode == "manual":
            self.bs_ssc_coefs = self._cfg.get("bs_ssc_file", None)
            self.bs_ssc_coefs = Utils._validate_file_path(self.bs_ssc_coefs, Constants._SSC_PAR_SUFFIX)
            self.bs_ssc_coefs = self._parse_sscpar(self.bs_ssc_coefs)
            for key, value in self.bs_ssc_coefs.items():
                Utils.info(
                    logger=self.logger,
                    msg=f"{self.name}: Backscatter-SSC coefficient '{key}' = {value}",
                    level=self.__class__.__name__
                )
        
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
    
    # ------------------------------------------------------------------ #
    # Properties                                                          #
    # ------------------------------------------------------------------ #
    @property
    def n_instruments(self) -> int:
        return len(self.instruments)

    # ------------------------------------------------------------------ #
    # Magic method                                                        #
    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}(\n"
            f"name='{self.name}',\n"
            f"config_path='{self._config_path}',\n"
            f"n_instruments={self.n_instruments}\n)"
        )


    
