from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Union, Tuple
import os
import tkinter as tk
from tkinter import ttk, messagebox

from .utils import Utils, Constants
from .adcp import ADCP, ADCPSetupGUI
from .ctd import CTD


class SurveySetupGUI:
    def __init__(self, name: str) -> None:
        self.root = tk.Tk()
        self.root.title(f"Survey Configuration - {name}")

        self.survey_name = tk.StringVar(value=name)
        self.n_instruments = tk.IntVar(value=1)

        self.instrument_vars: List[tk.StringVar] = []
        self.instrument_type_vars: List[tk.StringVar] = []
        self.generated_cfgs: List[Tuple[str, str]] = []

        self.ntu_ssc_mode = tk.StringVar(value="automatic")
        self.bs_ssc_mode = tk.StringVar(value="automatic")
        self.ntu_ssc_eqtype = tk.IntVar(value=1)
        self.bs_ssc_eqtype = tk.IntVar(value=1)
        self.ntu_coeff_vars: List[tk.StringVar] = []
        self.bs_coeff_vars: List[tk.StringVar] = []

        self._build_static_widgets()
        self._rebuild_dynamic_rows()
        self.config_path: Path | None = None
        self.root.mainloop()

    def _build_static_widgets(self) -> None:
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(sticky="nsew")
        self.root.columnconfigure(0, weight=1)

        ttk.Label(frm, text="Survey Name").grid(row=0, column=0, sticky="e")
        ttk.Entry(frm, textvariable=self.survey_name, width=30, state="readonly").grid(row=0, column=1, pady=4, sticky="w")

        ttk.Label(frm, text="Number of Instruments").grid(row=1, column=0, sticky="e")
        tk.Spinbox(frm, from_=1, to=100, textvariable=self.n_instruments, width=5, command=self._rebuild_dynamic_rows).grid(row=1, column=1, sticky="w")

        self.dynamic_frame = ttk.Frame(frm)
        self.dynamic_frame.grid(row=2, column=0, columnspan=2, pady=8, sticky="ew")

        # --- Calibration Parameters Section --- #
        cal_frame = ttk.LabelFrame(frm, text="SSC Calibration Setup")
        cal_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        self._build_calibration_block(cal_frame, "NTU–SSC Relationship", self.ntu_ssc_mode, self.ntu_ssc_eqtype, self.ntu_coeff_vars)
        self._build_calibration_block(cal_frame, "Backscatter–SSC Relationship", self.bs_ssc_mode, self.bs_ssc_eqtype, self.bs_coeff_vars)

        ttk.Button(frm, text="Save", command=self._on_save).grid(row=4, column=0, columnspan=2, sticky="ew", pady=6)

    def _build_calibration_block(self, parent, title, mode_var, eqtype_var, coeff_vars):
        frm = ttk.LabelFrame(parent, text=title)
        frm.pack(fill="x", pady=4)

        ttk.Label(frm, text="Mode:").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(frm, text="Automatic", variable=mode_var, value="automatic", command=lambda: self._toggle_coeff_block(frm, False)).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(frm, text="Manual", variable=mode_var, value="manual", command=lambda: self._toggle_coeff_block(frm, True)).grid(row=0, column=2, sticky="w")

        # Equation types
        ttk.Label(frm, text="Equation type:").grid(row=1, column=0, sticky="w")
        eqs = [
            ("Linear (A·x + B)", 1),
            ("Quadratic (A·x² + B·x + C)", 2),
            ("Log-linear (A·ln(x) + B)", 3),
            ("Exponential (A·e^(B·x))", 4)
        ]
        for i, (label, val) in enumerate(eqs):
            ttk.Radiobutton(
                frm,
                text=label,
                variable=eqtype_var,
                value=val,
                command=lambda f=frm, v=eqtype_var, c=coeff_vars: self._rebuild_coeff_inputs(f.coeff_frame, v, c)
            ).grid(row=2+i, column=0, columnspan=3, sticky="w")

        # Coefficient entries (shown only if manual)
        coeff_frame = ttk.Frame(frm)
        coeff_frame.grid(row=6+len(eqs), column=0, columnspan=3, sticky="ew", pady=4)
        frm.coeff_frame = coeff_frame  # save for toggling visibility
        self._build_coeff_inputs(coeff_frame, coeff_vars)
        self._toggle_coeff_block(frm, mode_var.get() == "manual")

    def _rebuild_coeff_inputs(self, frame, eqtype_var, coeff_vars):
        for w in frame.winfo_children():
            w.destroy()
        coeff_vars.clear()

        n_coeffs = {1: 2, 2: 3, 3: 2, 4: 2}.get(eqtype_var.get(), 2)
        labels = ["A", "B", "C"]

        for i in range(n_coeffs):
            var = tk.StringVar()
            coeff_vars.append(var)
            ttk.Label(frame, text=f"{labels[i]}:").grid(row=0, column=2*i, sticky="e")
            ttk.Entry(frame, textvariable=var, width=8).grid(row=0, column=2*i+1, sticky="w")

    def _toggle_coeff_block(self, frm, show: bool):
        if show:
            frm.coeff_frame.grid()
        else:
            frm.coeff_frame.grid_remove()

    def _build_coeff_inputs(self, frame, coeff_vars):
        for w in frame.winfo_children():
            w.destroy()
        coeff_vars.clear()

        # Determine how many coefficients based on selected type
        try:
            eqtype = int(frame.master.master.eqtype_var.get())
        except Exception:
            eqtype = 1

        n_coeffs = {1: 2, 2: 3, 3: 2, 4: 2}.get(eqtype, 2)
        labels = ["A", "B", "C"]

        for i in range(n_coeffs):
            var = tk.StringVar(value=0.5)
            coeff_vars.append(var)
            ttk.Label(frame, text=f"{labels[i]}:").grid(row=0, column=2*i, sticky="e")
            ttk.Entry(frame, textvariable=var, width=8).grid(row=0, column=2*i+1, sticky="w")

    def _rebuild_dynamic_rows(self) -> None:
        for w in self.dynamic_frame.winfo_children():
            w.destroy()

        self.instrument_vars = self._resize_vars(self.instrument_vars, self.n_instruments.get(), "Instrument")
        self.instrument_type_vars = self._resize_vars(self.instrument_type_vars, self.n_instruments.get(), "", dropdown=True)

        for i, (name_var, type_var) in enumerate(zip(self.instrument_vars, self.instrument_type_vars), start=1):
            ttk.Label(self.dynamic_frame, text=f"Instrument {i} Name").grid(row=i-1, column=0, sticky="e")
            ttk.Entry(self.dynamic_frame, textvariable=name_var, width=20).grid(row=i-1, column=1, sticky="w", pady=2)

            ttk.Label(self.dynamic_frame, text="Type").grid(row=i-1, column=2, sticky="e")
            ttk.Combobox(self.dynamic_frame, textvariable=type_var, state="readonly", width=15,
                         values=["ADCP", "CTD", "Water Sample"]).grid(row=i-1, column=3, sticky="w")

    @staticmethod
    def _resize_vars(lst: List[tk.StringVar], n: int, prefix: str = "", dropdown: bool = False) -> List[tk.StringVar]:
        while len(lst) < n:
            default = "" if dropdown else f"{prefix.lower()}_{len(lst)+1}"
            lst.append(tk.StringVar(value=default))
        return lst[:n]

    def _on_save(self) -> None:
        name = self.survey_name.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Survey name cannot be empty.")
            return

        cfg_dir = Path(os.getcwd())
        survey_cfg = cfg_dir / f"{name}.cfg"
        lines = [f"# Survey configuration for {name}", f"name = {name}"]

        index = 1
        instrument_names = {}
        for name_var, type_var in zip(self.instrument_vars, self.instrument_type_vars):
            inst_name = name_var.get().strip()
            inst_type = type_var.get().strip().lower()
            instrument_names[inst_type] = instrument_names.get(inst_type, []) + [inst_name]

            if inst_type == "adcp":
                adcp_gui = ADCPSetupGUI(inst_name, master=self.root)
                inst_config = adcp_gui.cfg.copy()
                base_config = "\n".join(f"{k} = {v}" for k, v in inst_config.items() if k != "files" and v is not None)

                if adcp_gui.cfg["mode"] == "folder":
                    for pd0 in adcp_gui.files:
                        sub_name = f"{inst_name}_{Path(pd0).stem}"
                        inst_cfg_path = cfg_dir / f"{sub_name}.cfg"

                        # Insert position file if available
                        posfile = adcp_gui.position_files.get(pd0, None)
                        pos_line = f"position_data = {posfile}" if posfile else ""

                        inst_text = (
                            f"# ADCP configuration\n"
                            f"name = {sub_name}\n"
                            f"filename = {pd0}\n"
                            f"{base_config}\n"
                            f"{pos_line}"
                        ).strip()

                        inst_cfg_path.write_text(inst_text, encoding="utf-8")
                        lines.append(f"inst_{index} = {sub_name}.cfg")
                        lines.append(f"inst_{index}_type = adcp")
                        index += 1
                else:
                    sub_name = inst_name
                    inst_cfg_path = cfg_dir / f"{sub_name}.cfg"

                    # Insert position file if available
                    posfile = adcp_gui.position_files.get(adcp_gui.files[0], None)
                    pos_line = f"position_data = {posfile}" if posfile else ""

                    inst_text = (
                        f"# ADCP configuration\n"
                        f"name = {sub_name}\n"
                        f"filename = {adcp_gui.files[0]}\n"
                        f"{base_config}\n"
                        f"{pos_line}"
                    ).strip()

                    inst_cfg_path.write_text(inst_text, encoding="utf-8")
                    lines.append(f"inst_{index} = {sub_name}.cfg")
                    lines.append(f"inst_{index}_type = adcp")
                    index += 1

            elif inst_type in ("ctd", "water sample"):
                inst_cfg_path = cfg_dir / f"{inst_name}.cfg"
                inst_cfg_path.write_text(
                    f"# {inst_type} configuration\nname = {inst_name}\nfilename = TBD\ntype = {inst_type}",
                    encoding="utf-8")
                lines.append(f"inst_{index} = {inst_name}.cfg")
                lines.append(f"inst_{index}_type = {inst_type}")
                index += 1

        lines.insert(2, f"n_instruments = {index-1}")

        # Write NTU–SSC relationship
        self._handle_calib_block(lines, "ntu_ssc", self.ntu_ssc_mode, self.ntu_ssc_eqtype, self.ntu_coeff_vars, instrument_names, required=["ctd", "water sample"])
        self._handle_calib_block(lines, "bs_ssc", self.bs_ssc_mode, self.bs_ssc_eqtype, self.bs_coeff_vars, instrument_names, required=["adcp", "water sample"])

        survey_cfg.write_text("\n".join(lines), encoding="utf-8")
        self.config_path = survey_cfg
        self.root.destroy()

    def _handle_calib_block(self, lines, key_prefix, mode_var, eqtype_var, coeff_vars, instrument_names, required):
        lines.append(f"{key_prefix}_mode = {mode_var.get()}")
        lines.append(f"{key_prefix}_eqtype = {eqtype_var.get()}")
        if mode_var.get() == "automatic":
            for req in required:
                if req not in instrument_names:
                    messagebox.showwarning("Missing Instrument", f"{key_prefix.upper()}: Required instrument type '{req}' is missing.")
        else:
            path = f"{key_prefix}.sscpar"
            with open(path, "w") as f:
                f.write(f"type,{eqtype_var.get()}\n")
                labels = ["A", "B", "C"]
                for label, var in zip(labels, coeff_vars):
                    if var.get().strip():
                        f.write(f"{label},{var.get().strip()}\n")
            lines.append(f"{key_prefix}_file = {path}")


class Survey:
    """Survey-level container that loads instruments from its config."""

    def __init__(self, cfg: str | Path, name: str = None) -> None:
        self.logger = Utils.get_logger()
        self._config_path = Utils._validate_file_path(cfg, Constants._CFG_SUFFIX)
        if self._config_path is None:
            gui = SurveySetupGUI(name=name)
            self._config_path = gui.config_path
        self._cfg = Utils._parse_kv_file(self._config_path)
        if self._cfg is None:
            gui = SurveySetupGUI(name=name)
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


    
