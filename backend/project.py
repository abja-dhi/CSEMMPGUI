from __future__ import annotations

from pathlib import Path
from typing import Dict, Union
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

from .survey import Survey
from .model import Model
from .utils import Constants, Utils

class ProjectSetupGUI:
    def __init__(self):
        self.project_dir = Path(filedialog.askdirectory(title="Select Project Folder"))
        if not self.project_dir:
            raise RuntimeError("Project folder selection cancelled.")

        self.root = tk.Tk()
        self.root.title("Project Configuration")
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(100, lambda: self.root.attributes("-topmost", False))
        self.project_name = tk.StringVar(value="Test6GUI")
        self.log_file_name = tk.StringVar(value="Test6GUI")
        self.n_surveys = tk.IntVar(value=1)
        self.n_models = tk.IntVar(value=1)
        self.surveys = []
        self.models = []
        self.survey_vars = []
        self.model_vars = []

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        self.setup_tab = ttk.Frame(self.tabs)
        self.utility_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.setup_tab, text="Project Setup")
        self.tabs.add(self.utility_tab, text="Utilities")

        self._build_static_widgets()
        self._build_utilities_tab()
        self._rebuild_dynamic_rows()
        self.config_path: Path = None
        self.root.mainloop()

    def _build_static_widgets(self):
        frm = ttk.Frame(self.setup_tab, padding=10)
        frm.grid(sticky="nsew")
        self.setup_tab.columnconfigure(0, weight=1)

        ttk.Label(frm, text="Project Name").grid(row=0, column=0, sticky="e")
        ttk.Entry(frm, textvariable=self.project_name, width=30).grid(row=0, column=1, pady=4, sticky="w")
        ttk.Label(frm, text="Log File Name").grid(row=1, column=0, sticky="e")
        ttk.Entry(frm, textvariable=self.log_file_name, width=30).grid(row=1, column=1, pady=4, sticky="w")

        ttk.Label(frm, text="Number of Surveys").grid(row=2, column=0, sticky="e")
        tk.Spinbox(frm, from_=1, to=100, textvariable=self.n_surveys, width=5,
                   command=self._rebuild_dynamic_rows).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Number of Models").grid(row=3, column=0, sticky="e")
        tk.Spinbox(frm, from_=1, to=100, textvariable=self.n_models, width=5,
                   command=self._rebuild_dynamic_rows).grid(row=3, column=1, sticky="w")

        self.dynamic_frame = ttk.Frame(frm)
        self.dynamic_frame.grid(row=4, column=0, columnspan=2, pady=8, sticky="ew")

        ttk.Button(frm, text="Process", command=self._on_process).grid(row=5, column=0, columnspan=2, sticky="ew", pady=6)

    def _build_utilities_tab(self):
        btn = ttk.Button(self.utility_tab, text="Batch Position Conversion (extern.dat → .csv)", command=self._run_batch_conversion)
        btn.pack(padx=10, pady=20)

    def _run_batch_conversion(self):
        folder = filedialog.askdirectory(title="Select folder for extern.dat conversion")
        if folder:
            self.externdat_to_csv(folder)
            messagebox.showinfo("Conversion Complete", "Batch conversion of extern.dat files completed.")

    def _rebuild_dynamic_rows(self):
        for child in self.dynamic_frame.winfo_children():
            child.destroy()
        self.survey_vars = self._resize_var_list(self.survey_vars, self.n_surveys.get(), "Survey")
        self.model_vars = self._resize_var_list(self.model_vars, self.n_models.get(), "Model")
        row = 0
        for i, var in enumerate(self.survey_vars, start=1):
            ttk.Label(self.dynamic_frame, text=f"Survey {i} name").grid(row=row, column=0, sticky="e")
            ttk.Entry(self.dynamic_frame, textvariable=var, width=25).grid(row=row, column=1, pady=2, sticky="w")
            row += 1
        for i, var in enumerate(self.model_vars, start=1):
            ttk.Label(self.dynamic_frame, text=f"Model {i} name").grid(row=row, column=0, sticky="e")
            ttk.Entry(self.dynamic_frame, textvariable=var, width=25).grid(row=row, column=1, pady=2, sticky="w")
            row += 1

    @staticmethod
    def _resize_var_list(lst: list, new_len: int, prefix: str) -> list:
        while len(lst) < new_len:
            lst.append(tk.StringVar(value=f"{prefix.lower()}_{len(lst)+1}"))
        return lst[:new_len]

    def _on_process(self):
        name = self.project_name.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Project name cannot be empty.")
            return
        log_file_name = self.log_file_name.get().strip()
        if not log_file_name.endswith(".log"):
            log_file_name += ".log"
        cfg_dir = self.project_dir
        cfg_dir.mkdir(exist_ok=True)
        proj_cfg_path = cfg_dir / f"{name}.cfg"
        lines = [
            f"# Project configuration for {name}",
            f"name = {name}",
            f"log_filename = {log_file_name}",
            f"n_surveys = {self.n_surveys.get()}",
        ]
        for i, var in enumerate(self.survey_vars, start=1):
            lines.append(f"survey_{i} = {var.get().strip()}.cfg")
            self.surveys.append(var.get().strip())
        lines.append(f"n_models = {self.n_models.get()}")
        for i, var in enumerate(self.model_vars, start=1):
            lines.append(f"model_{i} = {var.get().strip()}.cfg")
            self.models.append(var.get().strip())
        proj_cfg_text = "\n".join(lines)
        try:
            proj_cfg_path.write_text(proj_cfg_text, encoding="utf-8")
            self.config_path = proj_cfg_path
        except OSError as exc:
            messagebox.showerror("File Error", f"Cannot write config: {exc}")
            return
        self.root.destroy()

    # -*- coding: utf-8 -*-
    """
    Parse and convert all 'extern.dat' files in a directory tree to CSV format.
    """
    def externdat_to_csv(self, directory):
        """
        Locate, parse, and convert all 'extern.dat' fixed-width files in a directory tree to CSV.
        
        Parameters
        ----------
        directory : str or Path
            Root directory to search recursively for extern.dat files.
        """
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
                except Exception as e:
                    print(f"Failed to save {fname}: {e}")

            except Exception as e:
                print(f"Failed to read {file}: {e}")

            


class Project:
    """Top-level container for a project.

    Parameters
    ----------
    config_path : str | Path
        Path to the project ``.cfg`` file.

    Raises
    ------
    FileNotFoundError
        If *config_path* does not exist or is not a file.
    ValueError
        If *config_path* does not have a ``.cfg`` suffix, is empty,
        or cannot be read.
    """

    def __init__(self, config_path: str | Path = None) -> None:
        self._model_names: list[str] = []
        self._survey_names: list[str] = []
        if config_path is None:
            gui = ProjectSetupGUI()
            config_path = gui.config_path
            self._survey_names = gui.surveys
            self._model_names = gui.models

        self._config_path = Utils._validate_file_path(config_path, Constants._CFG_SUFFIX)
        self._cfg_dir = self._config_path.parent
        os.chdir(self._cfg_dir)
        cfg = Utils._parse_kv_file(self._config_path)
        self.name: str = cfg.get("name", self._config_path.stem)
        self.log_filename = cfg.get("log_filename", f"{self.name} - {datetime.now().strftime('%Y%m%d_%H%M')}.log")
        self.logger = Utils.get_logger(log_file=self.log_filename)
        Utils.info(
            logger=self.logger,
            msg=f"Initializing Project '{self.name}' from {self._config_path}",
            level=self.__class__.__name__
            )
        Utils.info(
            logger=self.logger,
            msg="Started reading project configuration file...",
            level=self.__class__.__name__
        )
        # ------------------------------------------------------------------ #
        # Surveys                                                            #
        # ------------------------------------------------------------------ #
        n_surveys = int(cfg.get("n_surveys", 0))
        if n_surveys < 1:
            Utils.error(
                logger=self.logger,
                msg=f"n_surveys={n_surveys} but must be at least 1 in '{self._config_path}'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        Utils.info(
            logger=self.logger,
            msg=f"Found {n_surveys} surveys in the project configuration.",
            level=self.__class__.__name__
        )
        survey_keys = [k for k in cfg if k.startswith("survey_")]
        if len(survey_keys) != n_surveys:
            Utils.error(
                logger=self.logger,
                msg=f"n_surveys={n_surveys} but {len(survey_keys)} survey entries found in '{self._config_path}'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
            
        self.surveys: Dict[str, Survey] = {}
        for i, key in enumerate(survey_keys):
            survey_name = None
            if len(self._survey_names) > 0:
                survey_name = self._survey_names[i]
            survey_number = key.split("_")[-1]
            survey_cfg = self._cfg_dir / cfg[key]
            Utils.info(
                logger=self.logger,
                msg=f"Survey '{survey_number}' configuration file: {survey_cfg}",
                level=self.__class__.__name__
            )
            survey = Survey(cfg=survey_cfg, name=survey_name)
            if hasattr(self, key):
                Utils.error(
                    logger=self.logger,
                    msg=f"Attribute '{survey.name}' already exists in Project. Surveys must have unique names.",
                    exc=AttributeError,
                    level=self.__class__.__name__
                )
            setattr(self, survey.name, survey)
            
            self.surveys[survey.name] = survey

        # ------------------------------------------------------------------ #
        # Models                                                             #
        # ------------------------------------------------------------------ #
        n_models = int(cfg.get("n_models", 0))
        if n_models < 1:
            Utils.error(
                logger=self.logger,
                msg=f"n_models={n_models} but must be at least 1 in '{self._config_path}'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        Utils.info(
            logger=self.logger,
            msg=f"Found {n_models} models in the project configuration.",
            level=self.__class__.__name__
        )
        model_keys = [k for k in cfg if k.startswith("model_")]
        if len(model_keys) != n_models:
            Utils.error(
                logger=self.logger,
                msg=f"n_models={n_models} but {len(model_keys)} model entries found in '{self._config_path}'.",
                exc=ValueError,
                level=self.__class__.__name__
            )

        self.models: Dict[str, Model] = {}
        for i, key in enumerate(model_keys):
            model_name = None
            if len(self._model_names) > 0:
                model_name = self._model_names[i]
            model_number = key.split("_")[-1]
            model_cfg = self._cfg_dir / cfg[key]
            Utils.info(
                logger=self.logger,
                msg=f"Model '{model_number}' configuration file: {model_cfg}",
                level=self.__class__.__name__
            )
            model = Model(cfg=model_cfg, name=model_name)
            if hasattr(self, key):
                Utils.error(
                    logger=self.logger,
                    msg=f"Attribute '{model.name}' already exists in Project. Models must have unique names.",
                    exc=AttributeError,
                    level=self.__class__.__name__
                )
            setattr(self, model.name, model)
            self.models[model.name] = model
        Utils.info(
            logger=self.logger,
            msg=f"Project '{self.name}' initialized successfully.",
            level=self.__class__.__name__
        )
        

    # ------------------------------------------------------------------ #
    # Properties                                                          #
    # ------------------------------------------------------------------ #
    @property
    def config_path(self) -> Path:
        """Resolved path to the configuration file."""
        return self._config_path

    @property
    def n_surveys(self) -> int:
        """Number of surveys registered in the project."""
        return len(self.surveys)

    @property
    def n_models(self) -> int:
        """Number of models registered in the project."""
        return len(self.models)

    
    # ------------------------------------------------------------------ #
    # Magic methods                                                       #
    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}(\n"
            f"config_path='{self._config_path}',\n"
            f"n_surveys={self.n_surveys},\n"
            f"n_models={self.n_models}\n)"
        )
    

class Plotting:
    """Placeholder for future plotting functionality."""
    
    def __init__(self, project: Project) -> None:
        self.project = project

    def plot_survey(self, survey_name: str) -> None:
        """Placeholder method to plot a survey."""
        raise NotImplementedError("Plotting functionality is not yet implemented.")
    
    def plot_model(self, model_name: str) -> None:
        """Placeholder method to plot a model."""
        raise NotImplementedError("Plotting functionality is not yet implemented.")