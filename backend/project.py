from pathlib import Path
from typing import Dict, Union
import os
from datetime import datetime
import pandas as pd


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

    def __init__(self, cfg : dict) -> None:
        self._model_names: list[str] = []
        self._survey_names: list[str] = []
        self.name: str = cfg.get("name", self._config_path.stem)
        

    # ------------------------------------------------------------------ #
    # Properties                                                          #
    # ------------------------------------------------------------------ #
    
    @property
    def n_surveys(self) -> int:
        """Number of surveys registered in the project."""
        return len(self.surveys)

    @property
    def n_models(self) -> int:
        """Number of models registered in the project."""
        return len(self.models)

    
    

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