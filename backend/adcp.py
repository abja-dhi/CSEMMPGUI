from pathlib import Path
from typing import List, Tuple
import warnings
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm
from dateutil import parser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


from .utils import Utils, Constants, XYZ
from .pd0 import Pd0Decoder, FixedLeader, VariableLeader
from ._adcp_position import ADCPPosition, PositionSetupGUI
from .plotting import PlottingShell


class ADCPSetupGUI:
    """Scrollable ADCP-setup dialog with independent scrolling per pane."""

    # ──────────────────────────────────────────────────────────────────
    def __init__(self, inst_name: str, master: tk.Tk | tk.Toplevel | None = None):
        self.top = tk.Toplevel(master)
        self.top.title(f"ADCP configuration - {inst_name}")
        self.top.transient(master)
        self.top.grab_set()

        # ── shared vars ───────────────────────────────────────────────
        self.name_var = tk.StringVar(self.top, value=inst_name)
        self.mode_var = tk.StringVar(self.top, value="folder")
        self.path_var = tk.StringVar(self.top)
        self.file_vars: dict[str, tk.IntVar] = {}
        self.cfg: dict | None = None
        self._active_scroll_widget: tk.Canvas | None = None  # keeps track of which canvas should scroll
        self.position_files: dict[str, str] = {}

        # ── dynamic parameter list (extend as needed) ────────────────
        self.param_definitions = [
            {"name": "magnetic_declination", "label": "Magnetic Declination (°)"       , "var": tk.DoubleVar(master=self.top, value=0.0)    , "widget": "entry"},
            {"name": "utc_offset", "label": "UTC Offset (minutes)", "var": tk.DoubleVar(master=self.top, value=0.3)     , "widget": "entry"},
            {"name": "rotation_angle", "label": "Rotation Angle (°)"   , "var": tk.DoubleVar(master=self.top, value=0.5)     , "widget": "entry"},
            {"name": "offset_x", "label": "Offset X (m)"   , "var": tk.DoubleVar(master=self.top, value=0.0)     , "widget": "entry"},
            {"name": "offset_y", "label": "Offset Y (m)"   , "var": tk.DoubleVar(master=self.top, value=0.0)     , "widget": "entry"},
            {"name": "offset_z", "label": "Offset Z (m)"   , "var": tk.DoubleVar(master=self.top, value=0.0)     , "widget": "entry"},
            {"name": "site_name", "label": "Site Name"   , "var": tk.StringVar(master=self.top, value="")     , "widget": "entry"},
            {"name": "surveyor", "label": "Surveyor"   , "var": tk.StringVar(master=self.top, value="")     , "widget": "entry"},
            {"name": "rssi_beam_1", "label": "RSSI Beam 1"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "rssi_beam_2", "label": "RSSI Beam 2"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "rssi_beam_3", "label": "RSSI Beam 3"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "rssi_beam_4", "label": "RSSI Beam 4"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "rssi_beam_5", "label": "RSSI Beam 5"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "rssi_beam_6", "label": "RSSI Beam 6"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "pg_min", "label": "Minimum Percent Good"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "cormag_min", "label": "Minimum Correlation Magnitude"   , "var": tk.IntVar(master=self.top, value=0)     , "widget": "entry"},
            {"name": "cormag_max", "label": "Maximum Correlation Magnitude"   , "var": tk.IntVar(master=self.top, value=255)     , "widget": "entry"},
            {"name": "echo_min", "label": "Minimum Echo Intensity"   , "var": tk.IntVar(master=self.top, value=0)     , "widget": "entry"},
            {"name": "echo_max", "label": "Maximum Echo Intensity"   , "var": tk.IntVar(master=self.top, value=255)     , "widget": "entry"},
            {"name": "errv_max", "label": "Maximum Error Velocity"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "vel_max", "label": "Maximum Velocity"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "vel_min", "label": "Minimum Velocity"   , "var": tk.DoubleVar(master=self.top, value=0.45)     , "widget": "entry"},
            {"name": "start_datetime", "label": "Start Date/Time"   , "var": tk.StringVar(master=self.top, value="2000-Jan-01 00:00:00.0")     , "widget": "entry"},
            {"name": "end_datetime", "label": "End Date/Time"   , "var": tk.StringVar(master=self.top, value="2030-Dec-31 00:00:00.0")     , "widget": "entry"},
            # {"name": "position_data", "label": "Position Data", "var": tk.StringVar(master=self.top, value="") , "widget": "position_file"},
        ]

        self._build_widgets()
        self.top.wait_window()

    # ──────────────────────────────────────────────────────────────────
    # GUI LAYOUT
    # ──────────────────────────────────────────────────────────────────
    def _build_widgets(self):
        # make dialog resizable
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)

        frm = ttk.Frame(self.top, padding=8)
        frm.grid(sticky="nsew")
        for col in (0, 1):
            frm.columnconfigure(col, weight=1)

        # row 0 – instrument name
        ttk.Label(frm, text="Instrument name").grid(row=0, column=0, sticky="e")
        ttk.Entry(frm, textvariable=self.name_var, state="readonly", width=30)\
            .grid(row=0, column=1, sticky="w", pady=2)

        # row 1 – PD0 source
        src_lf = ttk.LabelFrame(frm, text="PD0 source")
        src_lf.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Radiobutton(src_lf, text="Folder", value="folder", variable=self.mode_var,
                        command=self._reset).pack(side="left", padx=10)
        ttk.Radiobutton(src_lf, text="Single file", value="file", variable=self.mode_var,
                        command=self._reset).pack(side="left", padx=10)

        # row 2 – path + button
        ttk.Entry(frm, textvariable=self.path_var, width=80).grid(row=2, column=0, sticky="ew")
        ttk.Button(frm, text="Select", command=self._select_path).grid(row=2, column=1, sticky="w")

        # row 3 – scrollable .000 file list
        frm.rowconfigure(3, weight=1)
        self._build_file_list_pane(frm, row=3)

        # row 4/5 – scrollable parameters
        frm.rowconfigure(5, weight=2)
        self._build_param_pane(frm, label_row=4, canvas_row=5)

        # row 6 – save
        ttk.Button(frm, text="Save", command=self._save)\
            .grid(row=6, column=0, columnspan=2, sticky="ew", pady=6)

    # ── file-list pane ────────────────────────────────────────────────
    def _build_file_list_pane(self, parent: ttk.Frame, row: int):
        self.file_canvas = tk.Canvas(parent, height=120)
        self.file_vsb = ttk.Scrollbar(parent, orient="vertical", command=self.file_canvas.yview)
        self.file_frame = ttk.Frame(self.file_canvas)

        self.file_frame.bind("<Configure>", lambda e: self.file_canvas.configure(
            scrollregion=self.file_canvas.bbox("all")))
        self.file_canvas.create_window((0, 0), window=self.file_frame, anchor="nw")
        self.file_canvas.configure(yscrollcommand=self.file_vsb.set)

        # show only when in folder mode
        self.file_canvas.grid(row=row, column=0, sticky="nsew")
        self.file_vsb.grid(row=row, column=1, sticky="ns")
        self.file_canvas.grid_remove()
        self.file_vsb.grid_remove()

        # hover-scroll binding
        self.file_canvas.bind("<Enter>", lambda e: self._bind_mouse(self.file_canvas))
        self.file_canvas.bind("<Leave>", lambda e: self._unbind_mouse())

    # ── param pane ────────────────────────────────────────────────────
    def _build_param_pane(self, parent: ttk.Frame, label_row: int, canvas_row: int):
        lbl = ttk.LabelFrame(parent, text="Additional Parameters")
        lbl.grid(row=label_row, column=0, columnspan=2, sticky="ew")
        lbl.columnconfigure(0, weight=1)

        self.param_canvas = tk.Canvas(parent, height=260, width=700)
        self.param_vsb = ttk.Scrollbar(parent, orient="vertical", command=self.param_canvas.yview)
        self.param_inner = ttk.Frame(self.param_canvas)

        self.param_inner.bind("<Configure>", lambda e: self.param_canvas.configure(
            scrollregion=self.param_canvas.bbox("all")))
        self.param_canvas.create_window((0, 0), window=self.param_inner, anchor="nw")
        self.param_canvas.configure(yscrollcommand=self.param_vsb.set)

        self.param_canvas.grid(row=canvas_row, column=0, sticky="nsew")
        self.param_vsb.grid(row=canvas_row, column=1, sticky="ns")

        self.param_canvas.bind("<Enter>", lambda e: self._bind_mouse(self.param_canvas))
        self.param_canvas.bind("<Leave>", lambda e: self._unbind_mouse())

        self._populate_param_inner()

    def _populate_param_inner(self):
        for i, prm in enumerate(self.param_definitions):
            ttk.Label(self.param_inner, text=prm["label"]).grid(row=i, column=0, sticky="e", padx=6, pady=2)
            wtype = prm["widget"]
            var = prm["var"]

            if wtype == "entry":
                ttk.Entry(self.param_inner, textvariable=var, width=40).grid(row=i, column=1, sticky="w")
            elif wtype == "spinbox":
                ttk.Spinbox(self.param_inner, from_=prm.get("from_", 0), to=prm.get("to", 100),
                            increment=prm.get("increment", 1), textvariable=var, width=12).grid(row=i, column=1, sticky="w")
            elif wtype == "combobox":
                ttk.Combobox(self.param_inner, textvariable=var, values=prm["values"],
                             state="readonly", width=38).grid(row=i, column=1, sticky="w")
            elif wtype == "file":
                sub = ttk.Frame(self.param_inner)
                sub.grid(row=i, column=1, sticky="w")
                ttk.Entry(sub, textvariable=var, width=40).pack(side="left")
                ttk.Button(sub, text="Select",
                           command=lambda v=var, t=prm["types"]:
                           v.set(filedialog.askopenfilename(parent=self.top, filetypes=t))).pack(side="left", padx=3)
            elif wtype == "position_file":
                sub = ttk.Frame(self.param_inner)
                sub.grid(row=i, column=1, sticky="w")
                ttk.Entry(sub, textvariable=var, width=40, state="readonly").pack(side="left")
                ttk.Button(self.param_inner, text="Load Position Information",
                           command=self._open_position_setup, width=30).grid(row=i, column=2, padx=4)

    # ──────────────────────────────────────────────────────────────────
    # EVENT HELPERS
    # ──────────────────────────────────────────────────────────────────
    def _bind_mouse(self, canvas: tk.Canvas):
        self._active_scroll_widget = canvas
        self.top.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self):
        self.top.unbind_all("<MouseWheel>")
        self._active_scroll_widget = None

    def _on_mousewheel(self, event):
        if self._active_scroll_widget:
            self._active_scroll_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ──────────────────────────────────────────────────────────────────
    # FILE SELECTION / POPULATE
    # ──────────────────────────────────────────────────────────────────
    def _reset(self):
        self.path_var.set("")
        for w in self.file_frame.winfo_children():
            w.destroy()
        self.file_vars.clear()
        self.file_canvas.grid_remove()
        self.file_vsb.grid_remove()

    def _select_path(self):
        if self.mode_var.get() == "folder":
            folder = filedialog.askdirectory(parent=self.top, title="Select folder with .000 files")
            if folder:
                self._reset()
                self.path_var.set(folder)
                self._populate_files(Path(folder))
        else:
            f = filedialog.askopenfilename(parent=self.top, title="Select .000 file",
                                           filetypes=[("PD0 files", "*.000")])
            if f:
                self._reset()
                self.path_var.set(f)

    def _populate_files(self, folder: Path):
        files = sorted(folder.glob("*.000"))
        if not files:
            messagebox.showinfo("No files", "No .000 files found in selected folder.", parent=self.top)
            return
        self.file_canvas.grid()
        self.file_vsb.grid()

        self.position_file_vars = {}

        for i, f in enumerate(files):
            f_str = str(f)
            var = tk.IntVar(self.top, value=0)
            self.file_vars[f_str] = var

            chk = ttk.Checkbutton(self.file_frame, text=f.name, variable=var)
            chk.grid(row=i, column=0, sticky="w")

            pos_var = tk.StringVar(value="")
            pos_entry = ttk.Entry(self.file_frame, textvariable=pos_var, width=30, state="readonly")
            pos_entry.grid(row=i, column=1, padx=5)

            btn = ttk.Button(self.file_frame, text="Load Position Information",
                            command=lambda file=f, pv=pos_var: self._open_position_setup(file, pv))
            btn.grid(row=i, column=2, padx=5)
            btn.state(['!disabled'] if var.get() else ['disabled'])

            # track and bind checkbox
            self.position_file_vars[f_str] = {"var": pos_var, "btn": btn}
            var.trace_add("write", lambda *args, v=var, b=btn: b.state(['!disabled'] if v.get() else ['disabled']))


    def _open_position_setup(self, file: Path, pos_var: tk.StringVar):
        gui = PositionSetupGUI(master=self.top)
        if gui.result:
            pos_path = f"{Path(file).stem}.pos.cfg"
            with open(pos_path, "w") as f:
                for k, v in gui.result.items():
                    f.write(f"{k} = {v}\n")
            pos_var.set(pos_path)
            self.position_files[str(file)] = pos_path
            messagebox.showinfo("Saved", f"Position info saved as {pos_path}", parent=self.top)



    # def _open_position_setup(self):
    #     gui = PositionSetupGUI(master=self.top)
    #     if gui.result:
    #         # store in cfg dict later
    #         self.position_info = gui.result
    #         var = [i for i in range(len(self.param_definitions)) if self.param_definitions[i]["name"] == "position_data"][0]
    #         messagebox.showinfo("Saved", "Position information captured.", parent=self.top)
    #         with open(self.name_var.get() + ".pos.cfg", "w") as f:
    #             for key, value in gui.result.items():
    #                 f.write(f"{key} = {value}\n")
    #         self.param_definitions[var]["var"].set(self.name_var.get() + ".pos.cfg")

    # ──────────────────────────────────────────────────────────────────
    # SAVE
    # ──────────────────────────────────────────────────────────────────
    def _save(self):
        if self.mode_var.get() == "folder":
            selected = [p for p, v in self.file_vars.items() if v.get()]
            positions = [v.get() for v in self.position_file_vars.values() if v["var"].get()]
            if not selected:
                messagebox.showerror("Input error", "Choose at least one .000 file.", parent=self.top)
                return
            files = selected
        else:
            if not self.path_var.get():
                messagebox.showerror("Input error", "Select a PD0 file.", parent=self.top)
                return
            files = [self.path_var.get()]

        self.cfg = {
            "type": "adcp",
            "files": files,
            "positions": positions,
            **{d["name"]: d["var"].get() for d in self.param_definitions}
        }
        self.top.destroy()

    def _populate(self, folder: Path):
        files = sorted(folder.glob("*.000"))
        if not files:
            messagebox.showinfo("No files", "No .000 files found in that folder.", parent=self.top)
            return
        self.file_canvas.grid()
        self.file_scrollbar.grid()
        for i, f in enumerate(files):
            v = tk.IntVar(master=self.top, value=1)
            self.file_vars[str(f)] = v
            ttk.Checkbutton(self.file_scroll_frame, text=f.name, variable=v).grid(row=i, column=0, sticky="w")

    def _save(self):
        if not self.path_var.get():
            messagebox.showerror("Input error", "Please select a PD0 file or folder.", parent=self.top)
            return

        config = {
            "type": "adcp",
            "mode": self.mode_var.get(),
        }

        if self.mode_var.get() == "folder":
            selected = [p for p, v in self.file_vars.items() if v.get()]
            if not selected:
                messagebox.showerror("Input error", "Choose at least one .000 file.", parent=self.top)
                return
            self.files = selected
        else:
            self.files = [self.path_var.get()]

        for param in self.param_definitions:
            config[param["name"]] = param["var"].get()

        self.cfg = config
        self.top.destroy()





class ADCP():
    def __init__(self, cfg: str | Path, name: str) -> None:
        self.logger = Utils.get_logger()
        #self._config_path = Utils._validate_file_path(cfg, Constants._CFG_SUFFIX)
        self._cfg = cfg #Utils._parse_kv_file(self._config_path)
        
        self._pd0_path = self._cfg.get("filename", None)
        self.name = self._cfg.get("name", 'MyADCP') #self._cfg.get("name", self._config_path.stem)
        
        Utils.info(
            logger=self.logger,
            msg=f"Initializing ADCP from configuration file: {cfg}",
            level=self.__class__.__name__
            )
        
        
        if self._pd0_path is not None:
            self._pd0_path = Utils._validate_file_path(self._pd0_path, Constants._PD0_SUFFIX)
        else:
            Utils.error(
                logger=self.logger,
                msg=f"ADCP config '{self._config_path}' must contain 'filename' entry with a valid path to a PD0 file.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        self._pd0 = Pd0Decoder(self._pd0_path, self._cfg)
        self.datetimes = None
        self.time_mask = None
        self.fixed_leaders = None
        self.variable_leaders = None
        self.velocity = None
        self.echo_intensity = None
        self.correlation_magnitude = None
        self.percent_good = None
        self.bottom_track = None
        self.sensor_temperature = None
        self.sensor_transmit_pulse_length = None
        self.absolute_backscatter = None
        self.signal_to_noise_ratio = None
        self.relative_beam_midpoint_positions = None
        self.absolute_beam_midpoint_positions = None
        self.absolute_beam_midpoint_positions_hab = None
        self._pg_min      = float(self._cfg.get('pg_min'     , Constants._LOW_NUMBER))
        self._cormag_min  = int(self._cfg.get('cormag_min' , Constants._LOW_NUMBER))
        self._cormag_max  = int(self._cfg.get('cormag_max' , Constants._HIGH_NUMBER))
        self._echo_min    = int(self._cfg.get('echo_min'   , Constants._LOW_NUMBER))
        self._echo_max    = int(self._cfg.get('echo_max'   , Constants._HIGH_NUMBER))
        self._vel_min     = float(self._cfg.get('vel_min'    , Constants._LOW_NUMBER))
        self._vel_max     = float(self._cfg.get('vel_max'    , Constants._HIGH_NUMBER))
        self._err_vel_max = float(self._cfg.get('err_vel_max', Constants._HIGH_NUMBER))
        self._start_datetime = parser.parse(self._cfg.get('start_datetime', Constants._OLD_DATETIME))
        self._end_datetime = parser.parse(self._cfg.get('end_datetime', Constants._FAR_DATETIME))
        
        self.rssi_beam_1  = float(self._cfg.get('rssi_beam1'     , 0.41))
        self.rssi_beam_2  = float(self._cfg.get('rssi_beam2'     , 0.41))
        self.rssi_beam_3  = float(self._cfg.get('rssi_beam3'     , 0.41))
        self.rssi_beam_4  = float(self._cfg.get('rssi_beam4'     , 0.41))
        
        
        self.position: ADCPPosition | None = ADCPPosition(self._cfg['pos_cfg'])
        #self.position.resample_to(self.get_datetimes())
        
        self.instrument_depth = float(self._cfg.get('instrument_depth', 0.0))
        self.instrument_HAB = float(self._cfg.get('instrument_HAB', 0.0))
        self.plot = Plotting(self)
        
        self.calculate_beam_geometry()
        self.print_info()

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}(\n"
            f"config_path='{self._config_path}'\n)"
        )

    def print_info(self) -> None:
        """
        Print information about the model.
        """
        self._print_info(msg=f"ADCP '{self.name}' configuration loaded successfully.")
        self._print_info(msg=f"ADCP '{self.name}' number of ensembles: {self.n_ensembles}")
        self._print_info(msg=f"ADCP '{self.name}' number of beams: {self.n_beams}")
        self._print_info(msg=f"ADCP '{self.name}' number of cells: {self.n_cells}")
        self._print_info(msg=f"ADCP '{self.name}' beam facing direction: {self.beam_facing}.")
        self._print_info(msg=f"ADCP '{self.name}' depth cell length: {self.depth_cell_length} m.")
        self._print_info(msg=f"ADCP '{self.name}' bin 1 distance: {self.bin_1_distance} m.")
        self._print_info(msg=f"ADCP '{self.name}' beam angle: {self.beam_angle} degrees.")
        self._print_info(msg=f"ADCP '{self.name}' instrument depth: {self.instrument_depth} m.")
        self._print_info(msg=f"ADCP '{self.name}' first ensemble datetime: {self.datetimes[0]}")
        self._print_info(msg=f"ADCP '{self.name}' last ensemble datetime: {self.datetimes[-1]}")

        
    def _print_info(self, msg: str) -> None:
        Utils.info(
            logger=self.logger,
            msg=msg,
            level=self.__class__.__name__
        )

    @property
    def pd0(self) -> Pd0Decoder:
        """Return the PD0 object."""
        return self._pd0
    
    @property
    def n_beams(self) -> int:
        """Return the number of beams."""
        return self._pd0._n_beams
    
    @property
    def n_cells(self) -> int:
        """Return the number of cells."""
        return self._pd0._n_cells
    n_bins = n_cells  # Alias

    @property
    def n_ensembles(self) -> int:
        """Return the number of ensembles."""
        dt = self.get_datetimes()  # Ensure datetimes are loaded
        return dt.shape[0]

    @property
    def beam_facing(self) -> str:
        """
        Return the beam facing direction.
        
        Returns:
        -------
        str
            'up' if the beams are facing upwards, 'down' if they are facing downwards.
        """
        return self._pd0._beam_facing

    @property
    def depth_cell_length(self) -> float:
        """
        Return the depth cell length in meters.
        
        Returns:
        -------
        float
            The depth cell length in meters.
        """
        return self._pd0._depth_cell_length
    
    @property
    def bin_1_distance(self) -> float:
        """
        Return the distance to the first bin in meters.
        
        Returns:
        -------
        float
            The distance to the first bin in meters.
        """
        return self._pd0._bin_1_distance
    
    @property
    def beam_angle(self) -> float:
        """
        Return the beam angle in degrees.
        
        Returns:
        -------
        float
            The beam angle in degrees.
        """
        return self._pd0._beam_angle

    def get_fixed_leader(self) -> List[FixedLeader]:
        """
        Get the fixed leader data from the PD0 file.
        
        Returns:
        -------
        List[FixedLeader]
            A list of FixedLeader objects containing fixed leader data for each ensemble.
        """
        if self.fixed_leaders is None:
            self.fixed_leaders = self._pd0._get_fixed_leader()
        if self.time_mask is None:
            self.get_datetimes()
        self.fixed_leaders = np.array(self.fixed_leaders)[self.time_mask]
        return self.fixed_leaders

    def get_variable_leader(self) -> List[VariableLeader]:
        """
        Get the variable leader data from the PD0 file.
        
        Returns:
        -------
        List[VariableLeader]
            A list of VariableLeader objects containing variable leader data for each ensemble.
        """
        if self.variable_leaders is None:
            self.variable_leaders = self._pd0._get_variable_leader()
        if self.time_mask is None:
            self.get_datetimes()
        self.variable_leaders = np.array(self.variable_leaders)[self.time_mask]
        return self.variable_leaders

    def get_datetimes(self) -> List[datetime]:
        """
        Get the datetimes for each ensemble in the PD0 file.
        
        Returns:
        -------
        List[datetime]
            A list of datetime objects corresponding to each ensemble.
        """
        if self.datetimes is None:
            self.datetimes = self.pd0._get_datetimes()
            utc_offset = self._cfg.get("utc_offset", 0)
            for d in range(len(self.datetimes)):
                self.datetimes[d] += timedelta(hours=float(utc_offset))
            self.time_mask = (self.datetimes >= self._start_datetime) & (self.datetimes <= self._end_datetime)
            self.datetimes = self.datetimes[self.time_mask]
            if self.datetimes.size == 0:
                Utils.warning(
                    logger=self.logger,
                    msg=f"No ensembles found within the specified time range: {self._start_datetime} to {self._end_datetime}. Please check the start_datetime and end_datetime in the {self.name} configuration file ({self._config_path}).",
                    level=self.__class__.__name__
                )
        return self.datetimes
            
    def _process_velocity(self, velocity: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Process the velocity data to ensure it has the correct shape and type.
        
        Parameters:
        ----------
        velocity : np.ndarray
            The raw velocity data from the PD0 file of shape (n_ensembles, n_bins, n_beams).
        
        Returns:
        -------
        np.ndarray
            Processed velocity data with shape (n_ensembles, n_cells, n_beams).
        """
        vel_data = velocity.astype(np.float32)
        vel_data[(vel_data == -32768) | (vel_data == 32768)] = np.nan  # Replace invalid values with NaN
        vel_data = vel_data * 0.001  # Convert from mm/s to m/s
        u = vel_data[:, :, 0]
        v = vel_data[:, :, 1]
        w = vel_data[:, :, 2]
        ev = vel_data[:, :, 3] if self.n_beams > 3 else np.zeros_like(u)

        magnetic_declination = float(self._cfg.get("magnetic_declination", 0.0))
        if magnetic_declination != 0.0:
            X = np.stack((u, v), axis=-1)  # Shape (n_ensembles, n_cells, n_beams)
            rot = Utils.gen_rot_z(magnetic_declination)[:2, :2]  # 2x2 rotation matrix
            X_rot = np.einsum('ij,klj->kli', rot, X)  # Efficient matrix multiplication
            u, v = X_rot[:, :, 0], X_rot[:, :, 1]  # Unpack rotated components

        t = self.get_datetimes()
        u = u[self.time_mask, :]
        v = v[self.time_mask, :]
        w = w[self.time_mask, :]
        ev = ev[self.time_mask, :] if self.n_beams > 3 else np.zeros_like(u)
        dt = np.diff(t).astype('timedelta64[s]') / np.timedelta64(1, 's')  # Convert time differences to seconds
        dt = np.append(dt, dt[-1])  # Append last value to match ensemble count
        dt = dt[:, np.newaxis]  # Reshape to (n_ensembles, 1) for broadcasting
        du = u * dt
        dv = v * dt
        dz = w * dt
        return u, v, w, du, dv, dz, ev
        
    def get_velocity(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Get the velocity data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Velocity data with shape (n_ensembles, n_cells, n_beams).
        """
        if self.velocity is None:
            velocity = self._pd0._get_velocity()
            self.velocity = self._process_velocity(velocity)
        u, v, w, du, dv, dz, ev = self.velocity
        # Apply velocity masks
        mask = (
            (u < self._vel_min) | (u > self._vel_max) |
            (v < self._vel_min) | (v > self._vel_max) |
            (w < self._vel_min) | (w > self._vel_max) |
            (ev > self._err_vel_max)
            )
        u[mask] = np.nan
        v[mask] = np.nan
        w[mask] = np.nan
        du[mask] = np.nan
        dv[mask] = np.nan
        dz[mask] = np.nan
        ev[mask] = np.nan
        msg = "No valid {var} velocities found within the specified limits: {vel_min} to {vel_max} m/s. Please check the vel_min and vel_max in the {name} configuration file ({config_path})."
        Utils.all_nan(u , self.logger, msg.format(var='u'    , vel_min=self._vel_min, vel_max=self._vel_max, name=self.name, config_path=self._config_path), arrname="u", class_name=self.__class__.__name__)
        Utils.all_nan(v , self.logger, msg.format(var='v'    , vel_min=self._vel_min, vel_max=self._vel_max, name=self.name, config_path=self._config_path), arrname="v", class_name=self.__class__.__name__)
        Utils.all_nan(w , self.logger, msg.format(var='w'    , vel_min=self._vel_min, vel_max=self._vel_max, name=self.name, config_path=self._config_path), arrname="w", class_name=self.__class__.__name__)
        Utils.all_nan(ev, self.logger, msg.format(var='error', vel_min=self._vel_min, vel_max=self._vel_max, name=self.name, config_path=self._config_path), arrname="ev", class_name=self.__class__.__name__)
        self.velocity = (u, v, w, du, dv, dz, ev)
        return self.velocity
    
    def get_echo_intensity(self) -> np.ndarray:
        """
        Get the echo intensity data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Echo intensity data with shape (n_ensembles, n_cells).
        """
        if self.echo_intensity is None:
            self.echo_intensity = self._pd0._get_echo_intensity()
        if self.time_mask is None:
            self.get_datetimes()
        self.echo_intensity = self.echo_intensity[self.time_mask, :]
        mask = (
            (self.echo_intensity < self._echo_min) |
            (self.echo_intensity > self._echo_max)
        )
        self.echo_intensity[mask] = 32675
        Utils.all_nan(
            arr = self.echo_intensity,
            logger= self.logger,
            msg = f"No valid echo intensity values found within the specified limits: {self._echo_min} to {self._echo_max}. Please check the echo_min and echo_max in the {self.name} configuration file ({self._config_path}).",
            arrname= "echo_intensity",
            class_name= self.__class__.__name__
        )
        return self.echo_intensity

    def get_correlation_magnitude(self) -> np.ndarray:
        """
        Get the correlation magnitude data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Correlation magnitude data with shape (n_ensembles, n_cells).
        """
        if self.correlation_magnitude is None:
            self.correlation_magnitude = self._pd0._get_correlation_magnitude()
        if self.time_mask is None:
            self.get_datetimes()
        self.correlation_magnitude = self.correlation_magnitude[self.time_mask, :]
        mask = (
            (self.correlation_magnitude < self._cormag_min) |
            (self.correlation_magnitude > self._cormag_max)
        )
        self.correlation_magnitude[mask] = np.nan
        Utils.all_nan(
            arr = self.correlation_magnitude,
            logger= self.logger,
            msg = f"No valid correlation magnitude values found within the specified limits: {self._cormag_min} to {self._cormag_max}. Please check the cormag_min and cormag_max in the {self.name} configuration file ({self._config_path}).",
            arrname= "correlation_magnitude",
            class_name= self.__class__.__name__
        )
        return self.correlation_magnitude
    
    def get_percent_good(self) -> np.ndarray:
        """
        Get the percent good data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Percent good data with shape (n_ensembles, n_cells).
        """
        if self.percent_good is None:
            self.percent_good = self._pd0._get_percent_good().astype(np.float32)
        if self.time_mask is None:
            self.get_datetimes()
        self.percent_good = self.percent_good[self.time_mask, :]
        mask = (self.percent_good < self._pg_min)
        self.percent_good[mask] = np.nan
        Utils.all_nan(
            arr = self.percent_good,
            logger= self.logger,
            msg = f"No valid percent good values found above the minimum threshold: {self._pg_min}. Please check the pg_min in the {self.name} configuration file ({self._config_path}).",
            arrname= "percent_good",
            class_name= self.__class__.__name__
        )
        return self.percent_good
    
    def _get_bottom_track(self) -> np.ndarray:
        """
        Get the bottom track data from the PD0 file.

        Returns:
        -------
        np.ndarray
            Bottom track data with shape (n_ensembles, n_beams).
        """
        if self.bottom_track is None:
            bottom_track = self._pd0._get_bottom_track()
            beam_range_attributes = [f"beam{i+1}_bt_range" for i in range(self.n_beams)]
            self.bottom_track = np.array([[getattr(bt, attr)/100.0 for attr in beam_range_attributes] for bt in bottom_track], dtype=np.float32)
        if self.time_mask is None:
            self.get_datetimes()
        self.bottom_track = self.bottom_track[self.time_mask, :]
        return self.bottom_track

    def get_bottom_track(self) -> np.ndarray:
        """
        Get the bottom track data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Bottom track data with shape (n_ensembles, n_beams).
        """
        return self.bottom_track

    def get_sensor_temperature(self) -> np.ndarray:
        """
        Get the sensor temperature data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Sensor temperature data with shape (n_ensembles,).
        """
        if self.sensor_temperature is None:
            self.sensor_temperature = self._pd0._get_sensor_temperature()
        if self.time_mask is None:
            self.get_datetimes()
        self.sensor_temperature = self.sensor_temperature[self.time_mask]
        return self.sensor_temperature
    
    def get_sensor_transmit_pulse_length(self) -> np.ndarray:
        """
        Get the sensor transmit pulse length data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Sensor transmit pulse length data with shape (n_ensembles,).
        """
        if self.sensor_transmit_pulse_length is None:
            self.sensor_transmit_pulse_length = self._pd0._get_sensor_transmit_pulse_length()
        if self.time_mask is None:
            self.get_datetimes()
        self.sensor_transmit_pulse_length = self.sensor_transmit_pulse_length[self.time_mask]
        return self.sensor_transmit_pulse_length

    def get_absolute_backscatter(self) -> np.ndarray:
        """
        Get the absolute backscatter data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Absolute backscatter data with shape (n_ensembles, n_cells, n_beams).
        """
        if self.absolute_backscatter is None:
            self.absolute_backscatter = self._pd0._get_absolute_backscatter()[0]
        if self.time_mask is None:
            self.get_datetimes()
        self.absolute_backscatter = self.absolute_backscatter[self.time_mask, :, :]
        return self.absolute_backscatter
    
    def get_signal_to_noise_ratio(self) -> np.ndarray:
        """
        Get the signal to noise ratio data from the PD0 file.
        
        Returns:
        -------
        np.ndarray
            Signal to noise ratio data with shape (n_ensembles, n_cells, n_beams).
        """
        if self.signal_to_noise_ratio is None:
            self.signal_to_noise_ratio = self._pd0._get_absolute_backscatter()[1]
        if self.time_mask is None:
            self.get_datetimes()
        self.signal_to_noise_ratio = self.signal_to_noise_ratio[self.time_mask, :, :]
        return self.signal_to_noise_ratio

    def get_bin_midpoints(self) -> np.ndarray:
        """
        Get the midpoints of the bins.
        
        Returns:
        -------
        np.ndarray
            Midpoints of the bins with shape (n_cells,).
        """
        return self.pd0._get_bin_midpoints()

    def get_bin_midpoints_depth(self) -> np.ndarray:
        """
        Get the midpoints of the bins in depth.
        
        Returns:
        -------
        np.ndarray
            Midpoints of the bins in depth with shape (n_cells,).
        """
        return self.pd0._get_bin_midpoints_depth()

    def get_bin_midpoints_hab(self) -> np.ndarray:
        """
        Get the midpoints of the bins in height above bed (HAB).
        
        Returns:
        -------
        np.ndarray
            Midpoints of the bins in HAB with shape (n_cells,).
        """
        return self.pd0._get_bin_midpoints_hab()
    
    def calculate_beam_geometry(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        #TODO: Check the logic and update the function to 1. work with the correct shapes instead of transposing outputs, 2. use vectorized operations where possible
        """
        Calculate the beam geometry coordinates.
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: Arrays of x, y, z coordinates for the beams.
        """
        theta    = float(self._cfg.get('rotation_angle', 0.0))
        offset_x = float(self._cfg.get('offset_x', 0.0))
        offset_y = float(self._cfg.get('offset_y', 0.0))
        offset_z = float(self._cfg.get('offset_z', 0.0))
        dr       = float(self._cfg.get('radial_distance', 0.1))
        bt_range = self._get_bottom_track().T
        R = Utils.gen_rot_z(theta)
        if self.beam_facing == "down":
            relative_beam_origin = np.array([(dr, 0, 0),
                                             (-dr, 0, 0),
                                             (0, dr, 0),
                                             (0, -dr, 0)])
        else:
            relative_beam_origin = np.array([(-dr, 0, 0),
                                             (dr, 0, 0),
                                             (0, dr, 0),
                                             (0, -dr, 0)])
        relative_beam_origin = np.array([offset_x, offset_y, offset_z]) + relative_beam_origin
        relative_beam_origin = relative_beam_origin.dot(R).T
        relative_beam_midpoint_positions = np.full((3, self.n_beams, self.n_cells, self.n_ensembles), 0, dtype=float)
        
        if isinstance(self.position.x, float):
            xx = np.ones(self.n_ensembles) * self.position.x
        else:
            xx = self.position.x
        if isinstance(self.position.y, float):
            yy = np.ones(self.n_ensembles) * self.position.y
        else:
            yy = self.position.y
        if isinstance(self.position.z, float):
            zz = np.ones(self.n_ensembles) * self.position.z
        else:
            zz = self.position.z
        X = np.repeat(np.stack([xx, yy, zz])[:, np.newaxis, :], self.n_cells, axis=1)
        X = np.repeat(X[:, np.newaxis, :, :], self.n_beams, axis=1)
        X_hab = X.copy()
        bt_vec = np.full((3, self.n_beams, self.n_ensembles), 0, dtype=float)
        
        if any(~np.isnan(bt_range).flatten()):
            bt_vec[2] = -bt_range
        for b in range(self.n_beams):
            beam_midpoints = np.repeat(np.outer((0, 0, 0), np.ones(self.n_cells))[:, :, np.newaxis], self.n_ensembles, axis=2)
            if self.beam_facing == "down":
                beam_midpoints[2] += -np.repeat(self.get_bin_midpoints()[:, np.newaxis], self.n_ensembles, axis=1)
            else:
                beam_midpoints[2] += np.repeat(self.get_bin_midpoints()[:, np.newaxis], self.n_ensembles, axis=1)
            theta_beam = self.beam_angle
            Ry_cw = Utils.gen_rot_y(-theta_beam)
            Rx_cw = Utils.gen_rot_x(-theta_beam)
            Ry_ccw = Utils.gen_rot_y(theta_beam)
            Rx_ccw = Utils.gen_rot_x(theta_beam)

            for e in range(self.n_ensembles):
                if b == 0:
                    relative_beam_midpoint_positions[:, 0, :, e] = Ry_cw.dot(beam_midpoints[:, :, e])
                    bt_vec[:, b, e] = Ry_cw.dot(bt_vec[:, b, e])
                elif b == 1:
                    relative_beam_midpoint_positions[:, 1, :, e] = Ry_ccw.dot(beam_midpoints[:, :, e])
                    bt_vec[:, b, e] = Ry_ccw.dot(bt_vec[:, b, e])
                elif b == 2:
                    relative_beam_midpoint_positions[:, 2, :, e] = Rx_ccw.dot(beam_midpoints[:, :, e])
                    bt_vec[:, b, e] = Rx_ccw.dot(bt_vec[:, b, e])
                elif b == 3:
                    relative_beam_midpoint_positions[:, 3, :, e] = Rx_cw.dot(beam_midpoints[:, :, e])
                    bt_vec[:, b, e] = Rx_cw.dot(bt_vec[:, b, e])
                
                if isinstance(self.position.heading, float):
                    yaw = self.position.heading
                else:
                    yaw = self.position.heading[e]
                if isinstance(self.position.pitch, float):
                    pitch = self.position.pitch
                else:
                    pitch = self.position.pitch[e]
                if isinstance(self.position.roll, float):
                    roll = self.position.roll
                else:
                    roll = self.position.roll[e]
                
                R = np.dot(Utils.gen_rot_x(roll), Utils.gen_rot_z(yaw).dot(Utils.gen_rot_y(pitch)))
                relative_beam_midpoint_positions[:, b, :, e] = relative_beam_midpoint_positions[:, b, :, e].T.dot(R).T
                bt_vec[:, b, e] = bt_vec[:, b, e].dot(R).T

                X[:, b, :, e] += relative_beam_midpoint_positions[:, b, :, e]
                X_hab[:, b, :, e] += relative_beam_midpoint_positions[:, b, :, e]
                X_hab[2, b, :, e] = relative_beam_midpoint_positions[2, b, :, e] - bt_vec[2, b, e]
        
        self.bottom_track = np.abs(bt_vec[2, :, :])
        instrument_range = (self.bin_1_distance + self.depth_cell_length * self.n_cells) / 100
        
        relative_beam_midpoint_positions = relative_beam_midpoint_positions.transpose(0, 3, 2, 1)
        self.bottom_track[self.bottom_track > instrument_range] = bt_range[self.bottom_track > instrument_range]
        absolute_beam_midpoint_positions = X.copy().transpose(0, 3, 2, 1)
        absolute_beam_midpoint_positions_hab = X_hab.copy().transpose(0, 3, 2, 1)
        self.absolute_beam_midpoint_positions_hab = absolute_beam_midpoint_positions_hab

        self.relative_beam_midpoint_positions = XYZ(x=relative_beam_midpoint_positions[0, :, :, :],
                                                   y=relative_beam_midpoint_positions[1, :, :, :],
                                                   z=relative_beam_midpoint_positions[2, :, :, :])
        self.bottom_track = self.bottom_track.T
        self.absolute_beam_midpoint_positions = XYZ(x=absolute_beam_midpoint_positions[0, :, :, :],
                                                    y=absolute_beam_midpoint_positions[1, :, :, :],
                                                    z=absolute_beam_midpoint_positions[2, :, :, :])
        self.absolute_beam_midpoint_positions_hab = XYZ(x=absolute_beam_midpoint_positions_hab[0, :, :, :],
                                                        y=absolute_beam_midpoint_positions_hab[1, :, :, :],
                                                        z=absolute_beam_midpoint_positions_hab[2, :, :, :])
        
        
        
    def _scalar_counts_to_absolute_backscatter(self,E,E_r,k_c,alpha,C,R,Tx_T, Tx_PL, P_DBW):
        """
        Absolute Backscatter Equation from Deines (Updated - Mullison 2017 TRDI Application Note FSA031)
    
        Parameters
        ----------
        E_r : float
            Measured RSSI amplitude in the absence of any signal (noise), in counts.
        C : float
            Constant combining several parameters specific to each instrument.
        k_c : float
            Factor to convert amplitude counts to decibels (dB).
        E : float
            Measured Returned Signal Strength Indicator (RSSI) amplitude, in counts.
        Tx_T : float
            Tranducer temperature in deg C.
        R : float
            Along-beam range to the measurement in meters
        alpha : float
            Acoustic absorption (dB/m). 
        Tx_PL : float
            Transmit pulse length in dBm.
        P_DBW : float
            Transmit pulse power in dBW.
    
        Returns
        -------
        tuple
            Tuple containing two elements:
            - Sv : float
                Apparent volume scattering strength.
            - StN : float
                True signal to noise ratio.
    
        Notes
        -----
        - The use of the backscatter equation should be limited to ranges beyond π/4 * Rayleigh Distance for the given instrument.
        - Rayleigh Distance is calculated as transmit pulse length * α / width, representing the distance at which the beam can be considered to have fully formed.
        - For further details, refer to the original documentation by Deines.
        - 𝑘_c is a factor used to convert the amplitude counts reported by the ADCP’s receive circuitry to decibels (dB).
        - 𝐸 is the measured Returned Signal Strength Indicator (RSSI) amplitude reported by the ADCP for each bin along each beam, in counts.
        - 𝐸_r is the measured RSSI amplitude seen by the ADCP in the absence of any signal (the noise), in counts, and which is constant for a given ADCP.
        """
        StN = (10**(k_c * E / 10) - 10**(k_c * E_r / 10)) / (10**(k_c * E_r / 10))
        L_DBM = 10 * np.log10(Tx_PL)
        #P_DBW = 10 * np.log10(Tx_Pw)
        Sv = C + 10 * np.log10((Tx_T + 273.16) * (R**2)) - L_DBM - P_DBW + 2 * alpha * R + 10 * np.log10((10**(0.1 * k_c * (E - E_r)) - 1))
    
        return Sv, StN

        
    def _scalar_water_absorption_coeff(self,T, S, z, f, pH):
        '''
        Calculate water absorption coefficient.
    
        Parameters
        ----------
        T : float
            Temperature in degrees Celsius.
        S : float
            Salinity in practical salinity units (psu).
        z : float
            Depth in meters.
        f : float
            Frequency in kHz.
        pH : float
            Acidity.
    
        Returns
        -------
        float
            Water absorption coefficient in dB/km.
        '''
        c = 1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 + (0.0134 * T) * (S - 35) + 0.016 * z
        #c = 1412 + 3.21 * T + 1.19 * S + 0.0167 * z
    
        # Boric acid component
        A1 = (8.68 / c) * 10**(0.78 * pH - 5)
        P1 = 1
        f1 = 2.8 * ((S / 35)**0.5) * 10**(4 - (1245 / (273 + T)))
    
        # Magnesium sulphate component
        A2 = 21.44 * (S / c) * (1 + 0.025 * T)
        P2 = 1 - (1.37e-4) * z + (6.2e-9) * z**2
        f2 = (8.17 * 10**(8 - (1990 / (273 + T)))) / (1 + 0.0018 * (S - 35))
    
        if T <= 20:
            A3 = (4.937e-4) - (2.59e-5) * T + (9.11e-7) * T**2 - (1.5e-8) * T**3
        elif T > 20:
            A3 = (3.964e-4) - (1.146e-5) * T + (1.45e-7) * T**2 - (6.5e-8) * T**3
        P3 = 1 - (3.83e-5) * z + (4.9e-10) * (z**2)
    
        # Calculate water absorption coefficient
        alpha_w = (A1 * P1 * f1 * (f**2) / (f**2 + f1**2) + A2 * P2 * f2 * (f**2) / (f**2 + f2**2) + A3 * P3 * (f**2))
        
        # Convert absorption coefficient to dB/km
        alpha_w = (1 / 1000) * alpha_w
        
        return alpha_w
    
    
    def _scalar_sediment_absorption_coeff(self,ps, pw, d, SSC, T,S, f,z):
        '''
        Calculate sediment absorption coefficient.
    
        Parameters
        ----------
        ps : float
            Particle density in kg/m^3.
        pw : float
            Water density in kg/m^3.
        d : float
            Particle diameter in meters.
        SSC : float
            Suspended sediment concentration in kg/m^3.
        T : float
            Temperature in degrees Celsius.
        f : float
            Frequency in kHz .
    
        Returns
        -------
        float
            Sediment absorption coefficient.
        '''
        c = 1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 + (0.0134 * T) * (S - 35) + 0.016 * z # speed of sound in water
        v = (40e-6) / (20 + T)  # Kinematic viscosity (m2/s)
        B = (np.pi * f / v) * 0.5
        delt = 0.5 * (1 + 9 / (B * d))
        sig = ps / pw
        s = 9 / (2 * B * d) * (1 + (2 / (B * d)))
        k = 2 * np.pi / c  # Wave number (Assumed, as it isn't defined in the paper)
    
        alpha_s = (k**4) * (d**3) / (96 * ps) + k * ((sig - 1)**2) / (2 * ps) + \
                  (s / (s**2 + (sig + delt)**2)) * (20 / np.log(10)) * SSC
    
        return alpha_s     
        
    def calculate_ssc_from_backscatter(self, A1: float, B1: float, A2: float) -> None:
        """
        Calculate SSC from absolute backscatter using iterative alpha correction.
    
        Parameters
        ----------
        A1 : float
            Coefficient for ABS to NTU conversion.
        B1 : float
            Exponent for ABS to NTU conversion.
        A2 : float
            Coefficient for NTU to SSC conversion.
        """
        self.mask.set_mask_status(False)
    
        # ---------- Instrument + CTD data ----------
        E_r = 39
        WB = self.fixed_leaders[0].system_bandwidth_wb
        C = -139.09 if WB == 0 else -149.14
    
        k_c = {1: self.rssi_beam_1,
               2: self.rssi_beam_2,
               3: self.rssi_beam3,
               4: self.rssi_beam4}
        
        freq_str = self.fixed_leaders[0].system_configuration.frequency
        P_dbw = {"300-kHz": 14, "600-kHz": 9, "75-kHz": 27.3}[freq_str]
    
        # Sensor and geometry data
        temperature = self.get_sensor_temperature()
        bin_distances = self.get_bin_midpoints()
        pulse_lengths = self.get_sensor_transmit_pulse_length()
        bin_depths = abs(self.get_bin_midpoints_depth())
        instrument_freq = int(freq_str.split("-")[0])
    
    
    
        ## andy paused here, need to accept these as constant inputs, 
        
        # CTD data (assume self.df_ctd exists)
        df_ctd = self.df_ctd[self.name] if self.multi_source else self.df_ctd
        df_ctd = df_ctd.reindex(self.get_datetimes(), method='nearest')
        temp = df_ctd['Temperature (C)'].to_numpy()
        pressure = df_ctd['Pressure (dbar)'].to_numpy()
        salinity = df_ctd['Salinity (PSU)'].to_numpy()
        water_density = df_ctd['Density (kg/m3)'].to_numpy()
    
        # Reshape for broadcast
        nc = self.n_cells
        ne = self.n_ensembles
        temp = np.outer(temp, np.ones(nc)).T
        pressure = np.outer(pressure, np.ones(nc)).T
        salinity = np.outer(salinity, np.ones(nc)).T
        pulse_lengths = np.outer(pulse_lengths, np.ones(nc)).T
        bin_distances = np.outer(bin_distances, np.ones(ne))
        water_density = np.outer(water_density, np.ones(nc)).T
    
        if self.beam_facing == 'DOWN':
            pressure += bin_distances
        else:
            pressure -= bin_distances
    
        # Absorption from water
        alpha_w = self.processing.water_absorption_coeff(
            T=temp, S=salinity, z=pressure, f=instrument_freq, pH=7.5)
    
        # Echo intensity
        E = self.get_echo_intensity()
    
        # ---------- Init arrays ----------
        ABS = np.full_like(E, np.nan, dtype=float)
        SSC = np.full_like(E, np.nan, dtype=float)
        Alpha_s = np.zeros_like(E, dtype=float)
    
        # ---------- Iterative alpha correction ----------
        for bm in range(self.n_beams):
            for bn in range(self.n_cells):
                if bn == 0:
                    ssc = pp.ptools.NTU_to_SSC(pp.ptools.ABS_to_NTU(E[bm, bn], A=A1, B=B1), A=A2) # starting SSC from sensor 
                    for _ in range(100):
                        alpha_s = self.processing.sediment_absorption_coeff(
                            ps=1800,
                            pw=water_density[bn],
                            z=pressure[bn],
                            d=100e-6,
                            SSC=ssc,
                            T=temp[bn],
                            S=salinity[bn],
                            f=instrument_freq
                        )
                        sv, _ = self.processing.counts_to_absolute_backscatter(
                            E=E[bm, bn],
                            E_r=E_r,
                            k_c=k_c[bm + 1],
                            alpha=alpha_w[bn] + alpha_s,
                            C=C,
                            R=bin_distances[bn],
                            Tx_T=temp[bn],
                            Tx_PL=pulse_lengths[bn],
                            P_DBW=P_dbw
                        )
                        ssc_new = pp.ptools.NTU_to_SSC(pp.ptools.ABS_to_NTU(sv, A=A1, B=B1), A=A2)
                        if np.allclose(ssc_new, ssc, rtol=0, atol=1e-6, equal_nan=True):
                            break
                        ssc = ssc_new
                    ABS[bm, bn] = sv
                    SSC[bm, bn] = ssc
                    Alpha_s[bm, bn] = alpha_s
                else:
                    ssc = np.nanmean(SSC[bm, :bn], axis=0)
                    alpha_s = self.processing.sediment_absorption_coeff(
                        ps=1800,
                        pw=water_density[bn],
                        z=pressure[bn],
                        d=100e-6,
                        SSC=ssc,
                        T=temp[bn],
                        S=salinity[bn],
                        f=instrument_freq
                    )
                    sv, _ = self.processing.counts_to_absolute_backscatter(
                        E=E[bm, bn],
                        E_r=E_r,
                        k_c=k_c[bm + 1],
                        alpha=alpha_w[bn] + alpha_s,
                        C=C,
                        R=bin_distances[bn],
                        Tx_T=temp[bn],
                        Tx_PL=pulse_lengths[bn],
                        P_DBW=P_dbw
                    )
                    ABS[bm, bn] = sv
                    SSC[bm, bn] = pp.ptools.NTU_to_SSC(pp.ptools.ABS_to_NTU(sv, A=A1, B=B1), A=A2)
                    Alpha_s[bm, bn] = alpha_s
    
        # ---------- Store outputs ----------
        self.processing.append_to_ensembles(ABS, 'ABSOLUTE BACKSCATTER')
        self.processing.append_to_ensembles(SSC, 'SSC')
        self.processing.append_to_ensembles(Alpha_s, 'SEDIMENT ATTENUATION (dB/km)')
            
            

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Union
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import AutoLocator
from matplotlib.collections import LineCollection
import matplotlib as mpl

class Plotting:
    # _CMAPS = {
    #     "percent_good": plt.cm.binary,
    #     "echo_intensity": plt.cm.turbo,
    #     "filtered_echo_intensity": plt.cm.turbo,
    #     "correlation_magnitude": plt.cm.nipy_spectral,
    #     "absolute_backscatter": plt.cm.turbo,
    #     "ntu": plt.cm.turbo,
    #     "ssc": plt.cm.turbo,
    #     "signal_to_noise_ratio": plt.cm.bone_r,
    # }
    _CBAR_LABELS = {
        "u": "Eastward Velocity (m/s)",
        "v": "Northward Velocity (m/s)",
        "w": "Upward Velocity (m/s)",
        "CS": "Current Speed (m/s)",
        "error_velocity": "Error Velocity (m/s)",
    }
    def __init__(self, adcp: ADCP) -> None:
        self.adcp = adcp

    

    def flood_plot(self, variable: str, ax: Axes=None, plot_by: str="bin", beam_number: int=1, start_bin: int=None, end_bin: int=None, start_ensemble: int=None, end_ensemble: int=None, vmin: float=None, vmax: float=None, cmap: str = 'turbo_r') -> Axes:
        """
        Create a flood plot on the given axes.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        data : np.ndarray
            The data to plot.
        cmap : mpl.colors.Colormap
            The colormap to use for the plot.
        """
        variable = variable.lower().replace(" ", "_")
        start_bin = 0 if start_bin is None else start_bin
        end_bin = self.adcp.n_bins-1 if end_bin is None else end_bin
        start_ensemble = 0 if start_ensemble is None else start_ensemble
        end_ensemble = self.adcp.n_ensembles-1 if end_ensemble is None else end_ensemble
        if plot_by.lower() not in ["bin", "depth", "hab"]:
            Utils.error(
                logger=self.adcp.logger,
                msg=f"Invalid plot_by value '{plot_by}'. Must be 'Bin', 'Depth', or 'HAB'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        cmap = cmap #self._CMAPS.get(variable, cmap)
        if variable == "percent_good":
            data = self.adcp.get_percent_good()
        elif variable == "absolute_backscatter":
            data = self.adcp.get_absolute_backscatter()
        elif variable == "signal_to_noise_ratio":
            data = self.adcp.get_signal_to_noise_ratio()
        elif variable == "echo_intensity":
            data = self.adcp.get_echo_intensity()
        elif variable == "correlation_magnitude":
            data = self.adcp.get_correlation_magnitude()
        elif variable == "filtered_echo_intensity":
            data = self.adcp.get_filtered_echo_intensity()
        elif variable == "ntu":
            data = self.adcp.get_ntu()
        elif variable == "ssc":
            data = self.adcp.get_ssc()
        elif variable == 'u':
            data = self.adcp.get_velocity()[0]
        elif variable == 'v':
            data = self.adcp.get_velocity()[1]
        elif variable == 'w':
            data = self.adcp.get_velocity()[2]
        elif variable == 'cs':
            u = self.adcp.get_velocity()[0]
            v = self.adcp.get_velocity()[1]
            w = self.adcp.get_velocity()[2]
            data = np.sqrt(u**2 + v**2 + w**2)
        elif variable == 'error_velocity':
            data = self.adcp.get_velocity()[6]
        else:
            Utils.error(
                logger=self.adcp.logger,
                msg=f"Invalid variable '{variable}'. Must be 'percent_good', 'absolute_backscatter', 'signal_to_noise_ratio', 'echo_intensity', 'correlation_magnitude', 'filtered_echo_intensity', 'ntu', 'ssc', 'u', 'v', 'w', 'CS', or 'error_velocity'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        if plot_by.lower() == "bin":
            ylim = (start_bin, end_bin)
        elif plot_by.lower() == "depth":
            bin_midpoints = self.adcp.get_bin_midpoints_depth()
            ylim = (bin_midpoints[start_bin], bin_midpoints[end_bin])
        elif plot_by.lower() == "hab":
            bin_midpoints = self.adcp.get_bin_midpoints_hab()
            ylim = (bin_midpoints[start_bin], bin_midpoints[end_bin])

        datetimes = self.adcp.get_datetimes()
        if beam_number < 1 or beam_number > self.adcp.n_beams:
            Utils.error(
                logger=self.adcp.logger,
                msg=f"Invalid beam number {beam_number}. Must be between 1 and {self.adcp.n_beams}.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        if len(data.shape) == 3:
            x = data[start_ensemble:end_ensemble, start_bin:end_bin, beam_number-1]
        elif len(data.shape) == 2:
            x = data[start_ensemble:end_ensemble, start_bin:end_bin]
            data = data[:, :, np.newaxis]  # Add a new axis for compatibility
        else:
            Utils.error(
                logger=self.adcp.logger,
                msg=f"Invalid data shape {data.shape}. Expected 2D or 3D array.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        if ax is None:
            _, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3, figwidth=10.5, sharex=True, sharey=True)
        
        topax = ax.twiny()
        topax.set_xlim(start_ensemble, end_ensemble)
        if plot_by.lower() == "bin":
            ax.set_ylabel("Bin", fontsize=8)
        elif plot_by.lower() == "depth":
            ax.set_ylabel("Depth", fontsize=8)
        elif plot_by.lower() == "hab":
            ax.set_ylabel("Height Above Bed (m)", fontsize=8)

        origin = 'lower' if self.adcp.beam_facing == "up" else 'upper'
        
        vmins = {"percent_good": 0, "absolute_backscatter": -95}
        vmaxs = {"percent_good": 100, "absolute_backscatter": -10, "signal_to_noise_ratio": 50}
        vmin = vmins.get(variable, np.nanmin(data[start_ensemble:end_ensemble, start_bin:end_bin, :])) if vmin is None else vmin
        vmax = vmaxs.get(variable, np.nanmax(data[start_ensemble:end_ensemble, start_bin:end_bin, :])) if vmax is None else vmax
        
        xlim = mdates.date2num(datetimes[start_ensemble:end_ensemble])
        if self.adcp.beam_facing == "up":
            extent = (xlim[0], xlim[-1], ylim[0], ylim[-1])
        else:
            extent = (xlim[0], xlim[-1], ylim[1], ylim[0])
        ax = PlottingShell._flood_plot(
            ax=ax,
            data=x.T,
            origin=origin,
            extent=extent,
            cmap=cmap,
            aspect='auto',
            resample=False,
            vmin=vmin,
            vmax=vmax,
            cbar_label=self._CBAR_LABELS.get(variable, f"Beam {beam_number}"),
        )
        ax.xaxis.set_major_locator(mticker.FixedLocator(ax.get_xticks()))
        ax.xaxis.set_major_formatter(mdates.DateFormatter(PlottingShell._DATETIME_FORMAT))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
        ax.xaxis.tick_bottom()
        ax.xaxis.set_label_position('bottom')
        ax.yaxis.set_major_locator(AutoLocator())

        return ax
        
    def four_beam_flood_plot(self, variable: str, ax: Tuple[Axes, Axes, Axes, Axes] = None, plot_by: str = "bin",
                             start_bin: int = None, end_bin: int = None,
                             start_ensemble: int = None, end_ensemble: int = None, cmap: str = 'turbo_r') -> Tuple[Axes, Axes, Axes, Axes]:
        """
        Create a flood plot for the four beams of the ADCP data.
        Parameters
        ----------
        variable : str
            The variable to plot, must be one of 'echo_intensity', 'correlation_magnitude', or 'percent_good'.
        ax : Axes, optional
            The matplotlib Axes object to plot on. If None, a new figure and axes will be created.
        plot_by : str, optional
            The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
        start_bin : int, optional
            The starting bin index for the plot. Default is None, which means all bins will be plotted.
        end_bin : int, optional
            The ending bin index for the plot. Default is None, which means all bins will be plotted.
        start_ensemble : int, optional
            The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        end_ensemble : int, optional
            The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        Returns
        -------
        Axes
            The matplotlib Axes object with the flood plot.
        """
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=self.adcp.n_beams, ncol=1, figheight=8, figwidth=10.5, sharex=True, sharey=False)
        else:
            fig = ax[0].figure

        for i in range(self.adcp.n_beams):
            ax[i] = self.flood_plot(
                variable=variable,
                ax=ax[i],
                beam_number=i + 1,
                plot_by=plot_by,
                start_bin=start_bin,
                end_bin=end_bin,
                start_ensemble=start_ensemble,
                end_ensemble=end_ensemble,
                cmap = cmap,
            )

        return ax
    
    


    def mesh_plot(self, variable: str, ax: Axes = None, beam_number: int = 1,
                  plot_by: str = "bin", start_bin: int = None, end_bin: int = None,
                  start_ensemble: int = None, end_ensemble: int = None, vmin: float = None, vmax: float = None) -> Axes:
        """        Create a mesh plot on the given axes.
        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        variable : str
            The variable to plot.
        beam_number : int
            The beam number to plot (1 to n_beams).
        plot_by : str, optional
            The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
        start_bin : int, optional
            The starting bin index for the plot. Default is None, which means all bins will be plotted.
        end_bin : int, optional
            The ending bin index for the plot. Default is None, which means all bins will be plotted.
        start_ensemble : int, optional
            The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        end_ensemble : int, optional
            The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        Returns
        -------
        Axes
            The matplotlib Axes object with the mesh plot.
        """
        variable = variable.lower().replace(" ", "_")
        start_bin = 0 if start_bin is None else start_bin
        end_bin = self.adcp.n_bins-1 if end_bin is None else end_bin
        start_ensemble = 0 if start_ensemble is None else start_ensemble
        end_ensemble = self.adcp.n_ensembles-1 if end_ensemble is None else end_ensemble
        if plot_by.lower() not in ["bin", "depth", "hab"]:
            Utils.error(
                logger=self.adcp.logger,
                msg=f"Invalid plot_by value '{plot_by}'. Must be 'Bin', 'Depth', or 'HAB'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        cmap = self._CMAPS.get(variable, plt.cm.viridis)
        if variable == "percent_good":
            data = self.adcp.get_percent_good()
        elif variable == "absolute_backscatter":
            data = self.adcp.get_absolute_backscatter()
        elif variable == "signal_to_noise_ratio":
            data = self.adcp.get_signal_to_noise_ratio()
        elif variable == "echo_intensity":
            data = self.adcp.get_echo_intensity()
        elif variable == "correlation_magnitude":
            data = self.adcp.get_correlation_magnitude()
        elif variable == "filtered_echo_intensity":
            data = self.adcp.get_filtered_echo_intensity()
        elif variable == "ntu":
            data = self.adcp.get_ntu()
        elif variable == "ssc":
            data = self.adcp.get_ssc()
        else:
            Utils.error(
                logger=self.adcp.logger,
                msg=f"Invalid variable '{variable}'. Must be 'percent_good', 'absolute_backscatter', or 'signal_to_noise_ratio'.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        if plot_by.lower() == "bin":
            Z = self.adcp.relative_beam_midpoint_positions.z[:, :, beam_number-1]
            z_platform = (self.adcp.bin_1_distance / 100) + np.zeros(self.adcp.get_bottom_track().shape[0])
            ylim = (np.nanmin(Z), np.nanmax(Z))
        elif plot_by.lower() == "depth":
            Z = self.adcp.absolute_beam_midpoint_positions.z[:, :, beam_number-1]
            z_platform = self.adcp.position.coords.z
            ylim = (np.nanmin(Z), np.nanmax(Z))
        elif plot_by.lower() == "hab":
            Z = self.adcp.absolute_beam_midpoint_positions_hab.z[:, :, beam_number-1]
            z_platform = self.adcp.get_bottom_track()[:, beam_number-1]
            ylim = (0, 1.1*np.nanmax(z_platform))
        Z = Z[start_ensemble:(end_ensemble+1), start_bin:(end_bin+1)]
        z_platform = z_platform[start_ensemble:(end_ensemble+1)]

        datetimes = self.adcp.get_datetimes()[start_ensemble:(end_ensemble+1)]
        if beam_number < 1 or beam_number > self.adcp.n_beams:
            Utils.error(
                logger=self.adcp.logger,
                msg=f"Invalid beam number {beam_number}. Must be between 1 and {self.adcp.n_beams}.",
                exc=ValueError,
                level=self.__class__.__name__
            )
        x = data[start_ensemble:end_ensemble, start_bin:end_bin, beam_number-1]
        if ax is None:
            _, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3, figwidth=10.5, sharex=True, sharey=True)
        
        # topax = ax.twiny()
        # topax.set_xlim(start_ensemble, end_ensemble)
        # if plot_by.lower() == "bin":
        #     ax.set_ylabel("Bin", fontsize=8)
        # elif plot_by.lower() == "depth":
        #     ax.set_ylabel("Depth", fontsize=8)
        # elif plot_by.lower() == "hab":
        #     ax.set_ylabel("Height Above Bed (m)", fontsize=8)

        vmins = {"percent_good": 0, "absolute_backscatter": -95, "ntu": 0}
        vmaxs = {"percent_good": 100, "absolute_backscatter": -45, "signal_to_noise_ratio": 50}
        vmin = vmins.get(variable, np.nanmin(x)) if vmin is None else vmin
        vmax = vmaxs.get(variable, np.nanmax(x)) if vmax is None else vmax
        T = np.repeat(datetimes[:, np.newaxis], self.adcp.n_cells, axis=1)[:, start_bin:(end_bin+1)]
        ax = PlottingShell._mesh_plot(
            ax=ax,
            X = T,
            Y = Z,
            C = x,
            vmin=vmin,
            vmax=vmax,
            cmap=cmap,
            cbar_label=f"Beam {beam_number}",
            orientation="vertical",
            location="right",
            fraction=0.046,
            rotation=90,
            fontsize=8,
            T=datetimes,
            Z=z_platform,
            color="black",
            linewidth=1.0,
            alpha=0.7,
            Z_label="ROV (z)",
            ylim=ylim,
        )
        ax.xaxis.set_major_locator(mticker.FixedLocator(ax.get_xticks()))
        ax.xaxis.set_major_formatter(mdates.DateFormatter(PlottingShell._DATE_FORMAT))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
        ax.xaxis.tick_bottom()
        ax.xaxis.set_label_position('bottom')
        ax.yaxis.set_major_locator(AutoLocator())

        return ax


    def four_beam_mesh_plot(self, variable: str, ax: Tuple[Axes, Axes, Axes, Axes] = None,
                             plot_by: str = "bin", start_bin: int = None, end_bin: int = None,
                             start_ensemble: int = None, end_ensemble: int = None) -> Tuple[Axes, Axes, Axes, Axes]:
        """
        Create a mesh plot for the four beams of the ADCP data.
        Parameters
        ----------
        variable : str
            The variable to plot, must be one of 'echo_intensity', 'correlation_magnitude', or 'percent_good'.
        ax : Axes, optional
            The matplotlib Axes object to plot on. If None, a new figure and axes will be created.
        plot_by : str, optional
            The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
        start_bin : int, optional
            The starting bin index for the plot. Default is None, which means all bins will be plotted.
        end_bin : int, optional
            The ending bin index for the plot. Default is None, which means all bins will be plotted.
        start_ensemble : int, optional
            The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        end_ensemble : int, optional
            The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        Returns
        -------
        Axes
            The matplotlib Axes object with the mesh plot.
        """
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=self.adcp.n_beams, ncol=1, figheight=8, figwidth=10.5, sharex=True, sharey=True)
        else:
            fig = ax[0].figure

        for i in range(self.adcp.n_beams):
            ax[i] = self.mesh_plot(
                variable=variable,
                ax=ax[i],
                beam_number=i + 1,
                plot_by=plot_by,
                start_bin=start_bin,
                end_bin=end_bin,
                start_ensemble=start_ensemble,
                end_ensemble=end_ensemble
            )

        return ax
    
    def velocity_plot(self,ax: Tuple[Axes, Axes, Axes, Axes, Axes] = None,
                             plot_by: str = "bin", start_bin: int = None, end_bin: int = None,
                             start_ensemble: int = None, end_ensemble: int = None) -> Tuple[Axes, Axes, Axes, Axes]:
        """
        Create a flood plot for the measured velocity with 5 axes for u, v, and w components, current speed, and error velocity.
        Parameters
        ----------
        ax : Axes, optional
            The matplotlib Axes object to plot on. If None, a new figure and axes will be created.
        plot_by : str, optional
            The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
        start_bin : int, optional
            The starting bin index for the plot. Default is None, which means all bins will be plotted.
        end_bin : int, optional
            The ending bin index for the plot. Default is None, which means all bins will be plotted.
        start_ensemble : int, optional
            The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        end_ensemble : int, optional
            The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
        Returns
        -------
        Axes
            The matplotlib Axes object with the mesh plot.
        """
        if ax is None:
            fig, ax = PlottingShell.subplots(nrow=5, ncol=1, figheight=8, figwidth=10.5, sharex=True, sharey=True)
        else:
            fig = ax[0].figure
        variables = ['u', 'v', 'w', 'CS', 'error_velocity']
        for i, variable in enumerate(variables):
            ax[i] = self.flood_plot(
                variable=variable,
                ax=ax[i],
                beam_number=1,
                plot_by=plot_by,
                start_bin=start_bin,
                end_bin=end_bin,
                start_ensemble=start_ensemble,
                end_ensemble=end_ensemble
            )

        return ax