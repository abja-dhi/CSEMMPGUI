from pathlib import Path
from typing import List, Tuple, Dict, Optional
import warnings
import numpy as np
from numpy.typing import NDArray
from datetime import datetime, timedelta
from dateutil import parser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from dataclasses import dataclass, field
from datetime import datetime

from .utils import Utils, Constants, XYZ
from .pd0 import Pd0Decoder, FixedLeader, VariableLeader
from ._adcp_position import ADCPPosition, PositionSetupGUI
from .plotting import PlottingShell


class ADCP():
    def __init__(self, cfg: str | Path, name: str) -> None:

        self._cfg = cfg #Utils._parse_kv_file(self._config_path)
        self._pd0_path = self._cfg.get("filename", None)
        self.name = self._cfg.get("name", 'MyADCP') #self._cfg.get("name", self._config_path.stem)
        

        if self._pd0_path is not None:
            self._pd0_path = Utils._validate_file_path(self._pd0_path, Constants._PD0_SUFFIX)
        else:
            Utils.error(
                logger=self.logger,
                msg=f"Configuration for {self.name} must contain key 'filename' corresponding to a valid path to a PD0 (.000) file.",
                exc=ValueError,
                level=self.__class__.__name__
            )
            
        self._pd0 = Pd0Decoder(self._pd0_path, self._cfg)

        ## grab masking attributes
        @dataclass
        class MaskParams:
            pg_min: float = field(metadata={"desc": "Minimum 'percent good' threshold below which data is masked. Reflects the combined percentage of viable 3 and 4 beam velocity solutions PG1 + PG3. Applies to masks for velocity data only."})
            cormag_min: int = field(metadata={"desc": "Minimum correlation magnitude accepted. Applies to masks for beam data only."})
            cormag_max: int = field(metadata={"desc": "Maximum correlation magnitude accepted. Applies to masks for beam data only."})
            echo_min: int = field(metadata={"desc": "Minimum echo intensity threshold accepted. Applies to masks for beam data only."})
            echo_max: int = field(metadata={"desc": "Maximum echo intensity threshold accepted. Applies to masks for beam data only."})
            vel_min: float = field(metadata={"desc": "Minimum accepted velocity magnitude (m/s). Applies to masks for velocity data only."})
            vel_max: float = field(metadata={"desc": "Maximum accepted velocity magnitude (m/s). Applies to masks for velocity data only."})
            err_vel_max: float = field(metadata={"desc": "Maximum accepted error velocity (m/s). Applies to masks for velocity data only." })
            start_datetime: datetime = field(metadata={"desc": "Start time for valid ensemble masking window. Applies to masks for velocity and beam data."})
            end_datetime: datetime = field(metadata={"desc": "End time for valid ensemble masking window. Applies to masks for velocity and beam data."})
            first_good_ensemble: int = field(metadata={"desc": "Index of first ensemble to retain. Zero based index. Applies to masks for velocity and beam data."})
            last_good_ensemble: int = field(metadata={"desc": "Index of last ensemble to retain. Zero based index. Applies to masks for velocity and beam data."})

            
        self.masking = MaskParams(
            pg_min=float(self._cfg.get('pg_min', Constants._LOW_NUMBER)),
            cormag_min=int(self._cfg.get('cormag_min', Constants._LOW_NUMBER)),
            cormag_max=int(self._cfg.get('cormag_max', Constants._HIGH_NUMBER)),
            echo_min=int(self._cfg.get('echo_min', Constants._LOW_NUMBER)),
            echo_max=int(self._cfg.get('echo_max', Constants._HIGH_NUMBER)),
            vel_min=float(self._cfg.get('vel_min', Constants._LOW_NUMBER)),
            vel_max=float(self._cfg.get('vel_max', Constants._HIGH_NUMBER)),
            err_vel_max=float(self._cfg.get('err_vel_max', Constants._HIGH_NUMBER)),
            start_datetime=parser.parse(self._cfg.get('start_datetime', Constants._FAR_PAST_DATETIME)),
            end_datetime=parser.parse(self._cfg.get('end_datetime', Constants._FAR_FUTURE_DATETIME)),
            first_good_ensemble=int(self._cfg.get('first_good_ensemble', 1)),
            last_good_ensemble=int(self._cfg.get('last_good_ensemble', 1))
            )
        

        @dataclass
        class ADCPGeometry:
            beam_facing: str = field(metadata={"desc": "Beam direction (Up/Down)"})
            n_bins: float = field(metadata={"desc": "Number of bins"})
            n_beams: float = field(metadata={"desc": "Number of beams"})
            beam_angle: float = field(metadata={"desc": "Beam angle in degrees from vertical"})
            bin_1_distance: float = field(metadata={"desc": "Distance to the center of the first bin (m)"})
            bin_length: float = field(metadata={"desc": "Vertical length of each measurement bin (m)"})
            bin_midpoint_distances: NDArray[np.float64] = field(metadata={"desc": "Array of distances from ADCP to bin centers (m)"})
            crp_offset_x: float = field(metadata={"desc": "Offset of ADCP from platform CRP (X axis, meters)"})
            crp_offset_y: float = field(metadata={"desc": "Offset of ADCP from platform CRP(Y axis, meters)"})
            crp_offset_z: float = field(metadata={"desc": "Offset of ADCP from platform CRP (Z axis, meters)"})
            crp_rotation_angle: float = field(metadata={"desc": "CCW rotation of ADCP in casing (degrees)"})
            
                
        self.geometry = ADCPGeometry(
            beam_facing = self._pd0._beam_facing,
            n_bins = self._pd0._n_cells,
            n_beams = self._pd0._fixed.number_of_beams,
            beam_angle=self._pd0._fixed.beam_angle, 
            bin_1_distance=self._pd0._fixed.bin_1_distance/100,  
            bin_length= self._pd0._fixed.depth_cell_length_ws/100,  
            bin_midpoint_distances =  self._pd0._get_bin_midpoints(),
            crp_offset_x=float(self._cfg.get('crp_offset_x', Constants._LOW_NUMBER)),
            crp_offset_y=float(self._cfg.get('crp_offset_y', Constants._LOW_NUMBER)),
            crp_offset_z=float(self._cfg.get('crp_offset_z', Constants._LOW_NUMBER)),
            crp_rotation_angle=float(self._cfg.get('crp_rotation_angle', Constants._LOW_NUMBER))
            )

        # @dataclass
        # class RSSICoefficients:
        #     beam1: float = field(metadata={"desc": "RSSI coefficient for beam 1, from P3 test on TRDI instrument"})
        #     beam2: float = field(metadata={"desc": "RSSI coefficient for beam 2, from P3 test on TRDI instrument"})
        #     beam3: float = field(metadata={"desc": "RSSI coefficient for beam 3, from P3 test on TRDI instrument"})
        #     beam4: float = field(metadata={"desc": "RSSI coefficient for beam 4, from P3 test on TRDI instrument"})
                    
        # self.rssi = RSSICoefficients(
        #     beam1=float(self._cfg.get('rssi_beam1', 0.41)),
        #     beam2=float(self._cfg.get('rssi_beam2', 0.41)),
        #     beam3=float(self._cfg.get('rssi_beam3', 0.41)),
        #     beam4=float(self._cfg.get('rssi_beam4', 0.41))
        #     )
        
        @dataclass
        class ADCPCorrections:
            magnetic_declination: float = field(metadata={"desc": "Degrees CCW to rotate velocity data to account for magnetic declination"})
            utc_offset: float = field(metadata={"desc": "Hours to shift ensemble datetimes to account for UTC offset"})
            transect_shift_x: float = field(metadata={"desc": "Shifting distance of entire ADCP transect for model calibration (X axis, meters)"})
            transect_shift_y: float = field(metadata={"desc": "Shifting distance of entire ADCP transect for model calibration (Y axis, meters)"})
            transect_shift_z: float = field(metadata={"desc": "Shifting distance of entire ADCP transect for model calibration (Z axis, meters)"})
            transect_shift_t: float = field(metadata={"desc": "Shifting time of entire ADCP transect for model calibration (time axis, hours)"})
            
        self.corrections = ADCPCorrections(
            magnetic_declination= float(self._cfg.get('magnetic_declination', Constants._LOW_NUMBER)),
            utc_offset= float(self._cfg.get('utc_offset', Constants._LOW_NUMBER)),
            transect_shift_x= float(self._cfg.get('transect_shift_x', Constants._LOW_NUMBER)),
            transect_shift_y= float(self._cfg.get('transect_shift_y', Constants._LOW_NUMBER)),
            transect_shift_z= float(self._cfg.get('transect_shift_z', Constants._LOW_NUMBER)),
            transect_shift_t= float(self._cfg.get('transect_shift_t', Constants._LOW_NUMBER)),
            )
        
        @dataclass    
        class ADCPTime:
            n_ensembles: int = field(metadata={"desc": "Number of ensembles in the dataset"})
            ensemble_datetimes: int = field(metadata={"desc": "DateTime corresponding to each ensemble in the dataset"})
            ensemble_numbers: NDArray[np.int64] = field(metadata={"desc": "Number corresponding to each ensemble in the dataset. Read directly from source file"})
          
        self.time = ADCPTime(
            n_ensembles = self._pd0._n_ensembles,
            ensemble_datetimes = self._get_datetimes(),
            ensemble_numbers = np.array([i.ensemble_number for i in self._pd0._get_variable_leader()])
            )
        

        @dataclass
        class ADCPBeamData:
            echo_intensity: np.ndarray = field(metadata={"desc": "Raw echo intensity from each beam. Unitless ADC counts representing backscatter strength."})
            correlation_magnitude: np.ndarray = field(metadata={"desc": "Correlation magnitude from each beam, used as a data quality metric."})
            percent_good: np.ndarray = field(metadata={"desc": "Percentage of good data for each beam and cell, based on instrument quality control logic."})
            absolute_backscatter: np.ndarray = field(metadata={"desc": "Calibrated absolute backscatter in dB, derived from raw echo intensity using beam-specific corrections."})
            suspended_solids_concentration: np.ndarray = field(metadata={"desc": "Estimated suspended solids concentration (e.g., mg/L) derived from absolute backscatter using calibration coefficients."})
            signal_to_noise_ratio: np.ndarray = field(metadata={"desc": "SNR in dB, calculated as the difference between backscatter and instrument noise floor."})


        self.beam_data = ADCPBeamData(
            echo_intensity=self._pd0._get_echo_intensity(),
            correlation_magnitude=self._pd0._get_correlation_magnitude(),
            percent_good=self._pd0._get_percent_good(),
            absolute_backscatter = None,  # optional if calculated later
            suspended_solids_concentration=None,  # placeholder until compute 
            signal_to_noise_ratio = None
            )
        
        @dataclass
        class ADCPVelocityData:
            """
            Container for ADCP velocity-derived quantities in Earth coordinates.
            """
            u: np.ndarray = field(default=None, metadata={"desc": "Eastward (u) velocity component [m/s]"})
            v: np.ndarray = field(default=None, metadata={"desc": "Northward (v) velocity component [m/s]"})
            z: np.ndarray = field(default=None, metadata={"desc": "Vertical (z/upward) velocity component [m/s]"})
            speed: np.ndarray = field(default=None, metadata={"desc": "Horizontal current speed [m/s] = sqrt(u^2 + v^2)"})
            direction: np.ndarray = field(default=None, metadata={"desc": "Current direction in degrees from North (0°–360°)"})
            error_velocity: np.ndarray = field(default=None, metadata={"desc": "Error velocity component from ADCP [m/s]"})
            
        u,v,z,ev = self._get_velocity()
        speed = np.sqrt(u**2 + v**2)
        direction = (np.degrees(np.arctan2(u, v)) + 360) % 360
        
        self.velocity_data = ADCPVelocityData(
            u=u,
            v=v,
            z=z,
            speed=speed,  # Can be calculated later as sqrt(u^2 + v^2)
            direction=direction,  # Can be calculated later with arctan2(v, u)
            error_velocity=ev
        )
               
        @dataclass
        class ADCPBottomTrack:
            eval_amp: np.ndarray = field(metadata={"desc": "Bottom-track evaluation amplitude for each beam (counts)"})
            correlation_magnitude: np.ndarray = field(metadata={"desc": "Bottom-track correlation magnitude for each beam (counts)"})
            percent_good: np.ndarray = field(metadata={"desc": "Bottom-track percent-good per beam (0–100%)"})
            range_to_seabed: np.ndarray = field(metadata={"desc": "Vertical range to seabed per beam (meters)"})
            velocity: np.ndarray = field(metadata={"desc": "Bottom-track velocity vectors for each beam (m/s)"})
            ref_layer_velocity: np.ndarray = field(metadata={"desc": "Reference layer velocity for each beam (m/s)"})
            ref_correlation_magnitude: np.ndarray = field(metadata={"desc": "Correlation magnitude in reference layer (counts)"})
            ref_echo_intensity: np.ndarray = field(metadata={"desc": "Echo intensity in reference layer (counts)"})
            ref_percent_good: np.ndarray = field(metadata={"desc": "Percent-good in reference layer (0–100%)"})
            rssi_amp: np.ndarray = field(metadata={"desc": "Receiver Signal Strength Indicator amplitude in bottom echo (counts)"})
        
            # Configuration and metadata fields
            fid: int = field(metadata={"desc": "Bottom-track data ID (constant 0x0600)"})
            corr_mag_min_bc: int = field(metadata={"desc": "Minimum correlation magnitude (BC command)"})
            delay_before_reacquire_bd: int = field(metadata={"desc": "Ensembles to wait before reacquiring bottom (BD command)"})
            error_velocity_max_be: int = field(metadata={"desc": "Maximum error velocity (mm/s) (BE command)"})
            eval_amp_min_ba: int = field(metadata={"desc": "Minimum evaluation amplitude (BA command)"})
            max_depth_bx: int = field(metadata={"desc": "Maximum tracking depth (decimeters) (BX command)"})
            mode_bm: int = field(metadata={"desc": "Bottom-tracking mode (BM command)"})
            percent_good_min_bg: int = field(metadata={"desc": "Minimum percent-good required per ensemble (BG command)"})
            pings_per_ensemble_bp: int = field(metadata={"desc": "Bottom-track pings per ensemble (BP command)"})
            gain: int = field(metadata={"desc": "Gain level for shallow water bottom tracking"})
        
            # Reference layer bounds (BL command)
            ref_layer_far_bl: int = field(metadata={"desc": "Reference layer far boundary (dm)"})
            ref_layer_min_bl: int = field(metadata={"desc": "Reference layer minimum size (dm)"})
            ref_layer_near_bl: int = field(metadata={"desc": "Reference layer near boundary (dm)"})
                    
        bt_list = self._pd0._get_bottom_track()

        self.bottom_track = ADCPBottomTrack(
            eval_amp = np.array([[getattr(bt_list[e], f"beam{b}_eval_amp") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)]).T,
            correlation_magnitude = np.array([[getattr(bt_list[e], f"beam{b}_bt_corr") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)]).T,
            percent_good = np.array([[getattr(bt_list[e], f"beam{b}_bt_pgood") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)]).T,
            range_to_seabed = np.array([[getattr(bt_list[e], f"beam{b}_bt_range") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)], dtype = np.float64).T/100,
            velocity = np.array([[getattr(bt_list[e], f"beam{b}_bt_vel") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)], dtype = np.float64).T/100,
            ref_layer_velocity = np.array([[getattr(bt_list[e], f"beam_{b}_ref_layer_vel") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)], dtype = np.float64).T/100,
            ref_correlation_magnitude = np.array([[getattr(bt_list[e], f"bm{b}_ref_corr") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)]).T,
            ref_echo_intensity = np.array([[getattr(bt_list[e], f"bm{b}_ref_int") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)]).T,
            ref_percent_good = np.array([[getattr(bt_list[e], f"bm{b}_ref_pgood") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)]).T,
            rssi_amp = np.array([[getattr(bt_list[e], f"bm{b}_rssi_amp") for b in range(1, self.geometry.n_beams+1)] for e in range(self.time.n_ensembles)]).T,
            fid = np.array([bt.bottom_track_id for bt in bt_list]),
            corr_mag_min_bc = np.array([bt.bt_corr_mag_min_bc for bt in bt_list]),
            delay_before_reacquire_bd = np.array([bt.bt_delay_before_reacquire_bd for bt in bt_list]),
            error_velocity_max_be = np.array([bt.bt_err_vel_max_be for bt in bt_list]),
            eval_amp_min_ba = np.array([bt.bt_eval_amp_min_ba for bt in bt_list]),
            max_depth_bx = np.array([bt.bt_max_depth_bx for bt in bt_list]),
            mode_bm = np.array([bt.bt_mode_bm for bt in bt_list]),
            percent_good_min_bg = np.array([bt.bt_percent_good_min_bg for bt in bt_list]),
            pings_per_ensemble_bp = np.array([bt.bt_pings_per_ensemble_bp for bt in bt_list]),
            gain = np.array([bt.gain for bt in bt_list]),
            ref_layer_far_bl = np.array([bt.ref_layer_far_bl for bt in bt_list]),
            ref_layer_min_bl = np.array([bt.ref_layer_min_bl for bt in bt_list]),
            ref_layer_near_bl = np.array([bt.ref_layer_near_bl for bt in bt_list]),
        )
    
        @dataclass
        class AbsoluteBackscatterParams:
            """Parameters used in calculating absolute backscatter from echo intensity."""
            E_r: float = field(default=39.0, metadata={"desc": "Noise floor (counts)"})
            C: Optional[float] = field(default=None, metadata={"desc": "System-specific calibration constant (dB)"})
            alpha: Optional[float] = field(default=None, metadata={"desc": "Attenuation coefficient (dB/m)"})
            P_dbw: Optional[float] = field(default=None, metadata={"desc": "Transmit power (dBW)"})
            rssi: Dict[int, float] = field(
                default_factory=lambda: {1: 0.41, 2: 0.41, 3: 0.41, 4: 0.41},
                metadata={"desc": "RSSI scaling factors per beam"}
            )
            
        def gen_abs_backscatter_params_from_adcp(adcp: ADCP) -> AbsoluteBackscatterParams:
            """Derive absolute backscatter parameters from an ADCP instance."""
        
            # Determine system-specific default C based on bandwidth
            bandwidth = adcp._pd0._fixed.system_bandwidth_wb
            default_C = -139.09 if bandwidth == 0 else -149.14
        
            # Default alpha and P_dbw based on frequency
            freq = adcp._pd0._fixed.system_configuration.frequency
            freq_defaults = {
                "75-kHz": (0.027, 27.3),
                "300-kHz": (0.068, 14.0),
                "600-kHz": (0.178, 9.0)
            }
            default_alpha, default_P_dbw = freq_defaults.get(freq, (0.5, 8.3))
        
            # Override with config if provided
            C = adcp._cfg.get("absolute_backscatter_C", default_C)
            alpha = adcp._cfg.get("absolute_backscatter_alpha", default_alpha)
            P_dbw = adcp._cfg.get("absolute_backscatter_P_dbw", default_P_dbw)
            E_r = adcp._cfg.get("noise_floor", 39.0)
        
            # Beam-specific RSSI from rssi dataclass
            rssi ={
                1:float(self._cfg.get('rssi_beam1', 0.41)),
                2:float(self._cfg.get('rssi_beam2', 0.41)),
                3:float(self._cfg.get('rssi_beam3', 0.41)),
                4:float(self._cfg.get('rssi_beam4', 0.41))
                }
            
            return AbsoluteBackscatterParams(
                E_r=E_r,
                C=C,
                alpha=alpha,
                P_dbw=P_dbw,
                rssi=rssi
            )
        
        self.abs_params = gen_abs_backscatter_params_from_adcp(self)
        
        
        #self.bottom_track = build_bottom_track_data()
        # class ADCPModelParams:
        #     A,B,Water density, etc. 
        # # self.time = ADCPTime(
        # #     n_ensembles = )
        

        
        #self.position: ADCPPosition | None = ADCPPosition(self._cfg['pos_cfg'])
        #self.position.resample_to(self.time.ensemble_datetimes)
        
        #class BeamData:
            
        # self.get_datetimes()
        # self.plot = Plotting(self)
        # #self.calculate_beam_geometry()
        
        
        # if hasattr(self.position, "x"):
        #     print("Position has attribute 'x'")
        
        

        #self.print_info()

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}(\n"
            f"config_path='{self._config_path}'\n)"
        )

    # def _print_info(self) -> None:
    #     """
    #     Print information about the model.
    #     """
    #     self._print_info(msg=f"ADCP '{self.name}' configuration loaded successfully.")
    #     self._print_info(msg=f"ADCP '{self.name}' number of ensembles: {self.n_ensembles}")
    #     self._print_info(msg=f"ADCP '{self.name}' number of beams: {self.n_beams}")
    #     self._print_info(msg=f"ADCP '{self.name}' number of cells: {self.n_cells}")
    #     self._print_info(msg=f"ADCP '{self.name}' beam facing direction: {self.beam_facing}.")
    #     self._print_info(msg=f"ADCP '{self.name}' depth cell length: {self.depth_cell_length} m.")
    #     self._print_info(msg=f"ADCP '{self.name}' bin 1 distance: {self.bin_1_distance} m.")
    #     self._print_info(msg=f"ADCP '{self.name}' beam angle: {self.beam_angle} degrees.")
    #     self._print_info(msg=f"ADCP '{self.name}' instrument depth: {self.instrument_depth} m.")
    #     self._print_info(msg=f"ADCP '{self.name}' first ensemble datetime: {self.datetimes[0]}")
    #     self._print_info(msg=f"ADCP '{self.name}' last ensemble datetime: {self.datetimes[-1]}")

        


    def _get_datetimes(self, apply_corrections: bool = True) -> List[datetime]:
        """
        Get the datetimes for each ensemble in the PD0 file.
    
        If enabled, applies UTC offset and transect time shift corrections.
    
        Parameters
        ----------
        apply_corrections : bool, optional
            Whether to apply time corrections (default is True).
    
        Returns
        -------
        List[datetime]
            A list of datetime objects corresponding to each ensemble.
        """
        datetimes = self._pd0._get_datetimes()
        if apply_corrections:
            delta = timedelta(hours=float(self.corrections.utc_offset)) + \
                    timedelta(hours=float(self.corrections.transect_shift_t))
            datetimes = [dt + delta for dt in datetimes]
        return datetimes
    
        
    def _get_velocity(self,apply_corrections: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Get the velocity data from the PD0 file.
    
        Parameters
        ----------
        apply_corrections : bool, optional
            Whether to apply magnetic declination correction, by default True.
    
        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
            Tuple containing u, v, w, and error velocity arrays.
        """
        data = self._pd0._get_velocity()
        u = data[:,0] 
        v = data[:,1]  
        w = data[:,2]  
        ev = data[:,3] 
    
        if apply_corrections and self.corrections.magnetic_declination != 0.0:
            X = np.stack((u, v), axis=-1)  # Shape (n_ensembles, n_cells, 2)
            rot = Utils.gen_rot_z(self.corrections.magnetic_declination)[:2, :2]
            X_rot = np.einsum('ij,klj->kli', rot, X)
            u, v = X_rot[:, :, 0], X_rot[:, :, 1]
    
        return u, v, w, ev
        



    # def _get_sensor_temperature(self) -> np.ndarray:
    #     """
    #     Get the sensor temperature data from the PD0 file.
        
    #     Returns:
    #     -------
    #     np.ndarray
    #         Sensor temperature data with shape (n_ensembles,).
    #     """
    #     if self.sensor_temperature is None:
    #         self.sensor_temperature = self._pd0._get_sensor_temperature()

    #     self.sensor_temperature = self.sensor_temperature
    #     return self.sensor_temperature
    
    # def _get_sensor_transmit_pulse_length(self) -> np.ndarray:
    #     """
    #     Get the sensor transmit pulse length data from the PD0 file.
        
    #     Returns:
    #     -------
    #     np.ndarray
    #         Sensor transmit pulse length data with shape (n_ensembles,).
    #     """
    #     if self.sensor_transmit_pulse_length is None:
    #         self.sensor_transmit_pulse_length = self._pd0._get_sensor_transmit_pulse_length()

            

    #     self.sensor_transmit_pulse_length = self.sensor_transmit_pulse_length#

    # def _get_absolute_backscatter(self) -> np.ndarray:
    #     """
    #     Get the absolute backscatter data from the PD0 file.
        
    #     Returns:
    #     -------
    #     np.ndarray
    #         Absolute backscatter data with shape (n_ensembles, n_cells, n_beams).
    #     """
    #     if self.absolute_backscatter is None:
    #         self.absolute_backscatter = self._pd0._get_absolute_backscatter()[0]

    #     self.absolute_backscatter = self.absolute_backscatte
    #     return self.absolute_backscatter
    
    # def _get_signal_to_noise_ratio(self) -> np.ndarray:
    #     """
    #     Get the signal to noise ratio data from the PD0 file.
        
    #     Returns:
    #     -------
    #     np.ndarray
    #         Signal to noise ratio data with shape (n_ensembles, n_cells, n_beams).
    #     """
    #     if self.signal_to_noise_ratio is None:
    #         self.signal_to_noise_ratio = self._pd0._get_absolute_backscatter()[1]

            
    #     self.signal_to_noise_ratio = self.signal_to_noise_ratio
    #     return self.signal_to_noise_ratio

    # def _get_bin_midpoints(self) -> np.ndarray:
    #     """
    #     Get the midpoints of the bins.
        
    #     Returns:
    #     -------
    #     np.ndarray
    #         Midpoints of the bins with shape (n_cells,).
    #     """
    #     return self.pd0._get_bin_midpoints()

    # def _get_bin_midpoints_depth(self) -> np.ndarray:
    #     """
    #     Get the midpoints of the bins in depth.
        
    #     Returns:
    #     -------
    #     np.ndarray
    #         Midpoints of the bins in depth with shape (n_cells,).
    #     """
    #     return self.pd0._get_bin_midpoints_depth()

    # def get_bin_midpoints_hab(self) -> np.ndarray:
    #     """
    #     Get the midpoints of the bins in height above bed (HAB).
        
    #     Returns:
    #     -------
    #     np.ndarray
    #         Midpoints of the bins in HAB with shape (n_cells,).
    #     """
    #     return self.pd0._get_bin_midpoints_hab()

    def _calculate_beam_geometry(self) -> XYZ:
        """Calculate relative and geoaphic positions of each beam/bin/ensemble pair"""
        
        
        theta = self.crp_rotation_angle
        offset_x = self.crp_
        offset_y = float(self._cfg.get('offset_y', 0.0))
        offset_z = float(self._cfg.get('offset_z', 0.0))
        dr = float(self._cfg.get('radial_distance', 0.1))
        R = Utils.gen_rot_z(theta)
    
        if self.beam_facing == "down":
            rel_orig = np.array([(dr, 0, 0), (-dr, 0, 0), (0, dr, 0), (0, -dr, 0)])
        else:
            rel_orig = np.array([(-dr, 0, 0), (dr, 0, 0), (0, dr, 0), (0, -dr, 0)])
        rel_orig = np.array([offset_x, offset_y, offset_z]) + rel_orig
        rel_orig = rel_orig.dot(R).T
    
        n_beams, n_cells, n_ensembles = self.n_beams, self.n_cells, self.n_ensembles
        rel = np.zeros((3, n_beams, n_cells, n_ensembles))
    
        bin_mids = self.get_bin_midpoints()
        if self.beam_facing == "down":
            z_offsets = -bin_mids
        else:
            z_offsets = bin_mids
    
        for b in range(n_beams):
            if b in [0, 1]:
                R_beam = Utils.gen_rot_y((-1 if b == 0 else 1) * self.beam_angle)
            else:
                R_beam = Utils.gen_rot_x((1 if b == 3 else -1) * self.beam_angle)
    
            for e in range(n_ensembles):
                midpoints = np.zeros((3, n_cells))
                midpoints[2, :] = z_offsets
                rel[:, b, :, e] = R_beam @ midpoints
    
                yaw = self.position.heading if isinstance(self.position.heading, float) else self.position.heading[e]
                pitch = self.position.pitch if isinstance(self.position.pitch, float) else self.position.pitch[e]
                roll = self.position.roll if isinstance(self.position.roll, float) else self.position.roll[e]
                R_att = Utils.gen_rot_x(roll) @ Utils.gen_rot_z(yaw) @ Utils.gen_rot_y(pitch)
                rel[:, b, :, e] = (rel[:, b, :, e].T @ R_att).T
    
        self.relative_beam_midpoint_positions = XYZ(
            x=rel[0].transpose(1, 2, 0),
            y=rel[1].transpose(1, 2, 0),
            z=rel[2].transpose(1, 2, 0),
        )
    
        # Absolute positions
        if isinstance(self.position.x, float):
            xx = np.full(n_ensembles, self.position.x)
        else:
            xx = self.position.x
        if isinstance(self.position.y, float):
            yy = np.full(n_ensembles, self.position.y)
        else:
            yy = self.position.y
        if isinstance(self.position.z, float):
            zz = np.full(n_ensembles, self.position.z)
        else:
            zz = self.position.z
    
        X_base = np.stack([xx, yy, zz])[:, None, :]
        X_base = np.repeat(X_base, n_cells, axis=1)  # shape (3, n_cells, n_ensembles)
        X_base = np.repeat(X_base[None, :, :, :], n_beams, axis=0)  # (n_beams, 3, n_cells, n_ensembles)
    
        abs_pos = rel + np.transpose(X_base, (1, 0, 2, 3))  # shape (3, n_beams, n_cells, n_ensembles)
        abs_pos = abs_pos.transpose(0, 3, 2, 1)  # to (3, ens, cell, beam)
    
    
        return XYZ(x=abs_pos[0], y=abs_pos[1], z=abs_pos[2])

    
    # def calculate_beam_geometry_OLD(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    #     #TODO: Check the logic and update the function to 1. work with the correct shapes instead of transposing outputs, 2. use vectorized operations where possible
    #     """
    #     Calculate the beam geometry coordinates.
    #     Returns:
    #         Tuple[np.ndarray, np.ndarray, np.ndarray]: Arrays of x, y, z coordinates for the beams.
    #     """
    #     theta    = float(self._cfg.get('rotation_angle', 0.0))
    #     offset_x = float(self._cfg.get('offset_x', 0.0))
    #     offset_y = float(self._cfg.get('offset_y', 0.0))
    #     offset_z = float(self._cfg.get('offset_z', 0.0))
    #     dr       = float(self._cfg.get('radial_distance', 0.1))
    #     bt_range = self._get_bottom_track().T
    #     R = Utils.gen_rot_z(theta)
    #     if self.beam_facing == "down":
    #         relative_beam_origin = np.array([(dr, 0, 0),
    #                                          (-dr, 0, 0),
    #                                          (0, dr, 0),
    #                                          (0, -dr, 0)])
    #     else:
    #         relative_beam_origin = np.array([(-dr, 0, 0),
    #                                          (dr, 0, 0),
    #                                          (0, dr, 0),
    #                                          (0, -dr, 0)])
            
    #     relative_beam_origin = np.array([offset_x, offset_y, offset_z]) + relative_beam_origin
    #     relative_beam_origin = relative_beam_origin.dot(R).T
    #     relative_beam_midpoint_positions = np.full((3, self.n_beams, self.n_cells, self.n_ensembles), 0, dtype=float)
        
    #     if isinstance(self.position.x, float):
    #         xx = np.ones(self.n_ensembles) * self.position.x
    #     else:
    #         xx = self.position.x
    #     if isinstance(self.position.y, float):
    #         yy = np.ones(self.n_ensembles) * self.position.y
    #     else:
    #         yy = self.position.y
    #     if isinstance(self.position.z, float):
    #         zz = np.ones(self.n_ensembles) * self.position.z
    #     else:
    #         zz = self.position.z
    #     X = np.repeat(np.stack([xx, yy, zz])[:, np.newaxis, :], self.n_cells, axis=1)
    #     X = np.repeat(X[:, np.newaxis, :, :], self.n_beams, axis=1)
    #     X_hab = X.copy()
    #     bt_vec = np.full((3, self.n_beams, self.n_ensembles), 0, dtype=float)
        
    #     if any(~np.isnan(bt_range).flatten()):
    #         bt_vec[2] = -bt_range
    #     for b in range(self.n_beams):
    #         beam_midpoints = np.repeat(np.outer((0, 0, 0), np.ones(self.n_cells))[:, :, np.newaxis], self.n_ensembles, axis=2)
    #         if self.beam_facing == "down":
    #             beam_midpoints[2] += -np.repeat(self.get_bin_midpoints()[:, np.newaxis], self.n_ensembles, axis=1)
    #         else:
    #             beam_midpoints[2] += np.repeat(self.get_bin_midpoints()[:, np.newaxis], self.n_ensembles, axis=1)
    #         theta_beam = self.beam_angle
    #         Ry_cw = Utils.gen_rot_y(-theta_beam)
    #         Rx_cw = Utils.gen_rot_x(-theta_beam)
    #         Ry_ccw = Utils.gen_rot_y(theta_beam)
    #         Rx_ccw = Utils.gen_rot_x(theta_beam)

    #         for e in range(self.n_ensembles):
    #             if b == 0:
    #                 relative_beam_midpoint_positions[:, 0, :, e] = Ry_cw.dot(beam_midpoints[:, :, e])
    #                 bt_vec[:, b, e] = Ry_cw.dot(bt_vec[:, b, e])
    #             elif b == 1:
    #                 relative_beam_midpoint_positions[:, 1, :, e] = Ry_ccw.dot(beam_midpoints[:, :, e])
    #                 bt_vec[:, b, e] = Ry_ccw.dot(bt_vec[:, b, e])
    #             elif b == 2:
    #                 relative_beam_midpoint_positions[:, 2, :, e] = Rx_ccw.dot(beam_midpoints[:, :, e])
    #                 bt_vec[:, b, e] = Rx_ccw.dot(bt_vec[:, b, e])
    #             elif b == 3:
    #                 relative_beam_midpoint_positions[:, 3, :, e] = Rx_cw.dot(beam_midpoints[:, :, e])
    #                 bt_vec[:, b, e] = Rx_cw.dot(bt_vec[:, b, e])
                
    #             if isinstance(self.position.heading, float):
    #                 yaw = self.position.heading
    #             else:
    #                 yaw = self.position.heading[e]
    #             if isinstance(self.position.pitch, float):
    #                 pitch = self.position.pitch
    #             else:
    #                 pitch = self.position.pitch[e]
    #             if isinstance(self.position.roll, float):
    #                 roll = self.position.roll
    #             else:
    #                 roll = self.position.roll[e]
                
    #             R = np.dot(Utils.gen_rot_x(roll), Utils.gen_rot_z(yaw).dot(Utils.gen_rot_y(pitch)))
    #             relative_beam_midpoint_positions[:, b, :, e] = relative_beam_midpoint_positions[:, b, :, e].T.dot(R).T
    #             bt_vec[:, b, e] = bt_vec[:, b, e].dot(R).T

    #             X[:, b, :, e] += relative_beam_midpoint_positions[:, b, :, e]
    #             X_hab[:, b, :, e] += relative_beam_midpoint_positions[:, b, :, e]
    #             X_hab[2, b, :, e] = relative_beam_midpoint_positions[2, b, :, e] - bt_vec[2, b, e]
        
    #     self.bottom_track = np.abs(bt_vec[2, :, :])
    #     instrument_range = (self.bin_1_distance + self.depth_cell_length * self.n_cells) / 100
        
    #     relative_beam_midpoint_positions = relative_beam_midpoint_positions.transpose(0, 3, 2, 1)
    #     self.bottom_track[self.bottom_track > instrument_range] = bt_range[self.bottom_track > instrument_range]
    #     absolute_beam_midpoint_positions = X.copy().transpose(0, 3, 2, 1)
    #     absolute_beam_midpoint_positions_hab = X_hab.copy().transpose(0, 3, 2, 1)
    #     self.absolute_beam_midpoint_positions_hab = absolute_beam_midpoint_positions_hab

    #     self.relative_beam_midpoint_positions = XYZ(x=relative_beam_midpoint_positions[0, :, :, :],
    #                                                y=relative_beam_midpoint_positions[1, :, :, :],
    #                                                z=relative_beam_midpoint_positions[2, :, :, :])
    #     self.bottom_track = self.bottom_track.T
    #     self.absolute_beam_midpoint_positions = XYZ(x=absolute_beam_midpoint_positions[0, :, :, :],
    #                                                 y=absolute_beam_midpoint_positions[1, :, :, :],
    #                                                 z=absolute_beam_midpoint_positions[2, :, :, :])
    #     self.absolute_beam_midpoint_positions_hab = XYZ(x=absolute_beam_midpoint_positions_hab[0, :, :, :],
    #                                                     y=absolute_beam_midpoint_positions_hab[1, :, :, :],
    #                                                     z=absolute_beam_midpoint_positions_hab[2, :, :, :])
        



    @classmethod
    def _calculate_absolute_backscatter(self) -> np.ndarray:
        """
        Convert echo intensity to absolute backscatter.

        Returns:
        --------
            np.ndarray: A 2D array of absolute backscatter values for each ensemble and cell.
        """
        echo_intensity = self._get_echo_intensity()
        if echo_intensity is None:
            return None
        E_r = self.cfg.get('noise_floor', 39)
        WB = self._fixed.system_bandwidth_wb
        if WB == 0:
            C = -139.09
        else:
            C = -149.14
        C = self.cfg.get('absolute_backscatter_C', C)
        default_rssis = {1: 0.41, 2: 0.41, 3: 0.41, 4: 0.41}
        k_c = {}
        for i in range(self._fixed.number_of_beams):
            if f'rssi_beam_{i+1}' in self.cfg.keys():
                k_c[i+1] = self.cfg[f'rssi_beam_{i+1}']
            else:
                k_c[i+1] = default_rssis.get(i+1, 0.45)
                Utils.warning(
                    logger=self.logger,
                    msg=f"Using default RSSI value {k_c[i+1]} for beam {i+1}.",
                    level=self.__class__.__name__
                )
        alpha = 0.5
        P_dbw = 8.3
        if self._fixed.system_configuration.frequency == '75-kHz':
            alpha = 0.027
            P_dbw = 27.3
        elif self._fixed.system_configuration.frequency == '300-kHz':
            alpha = 0.068
            P_dbw = 14    
        elif self._fixed.system_configuration.frequency == '600-kHz':
            alpha = 0.178
            P_dbw = 9
            

        alpha = self.cfg.get('absolute_backscatter_alpha', alpha)
        P_dbw = self.cfg.get('absolute_backscatter_P_dbw', P_dbw)

        temperature = np.outer(self._get_sensor_temperature(), np.ones(self._n_cells))
        bin_distances = np.outer(self._get_bin_midpoints(), np.ones(self._n_ensembles)).T
        transmit_pulse_length = np.outer(self._get_sensor_transmit_pulse_length(), np.ones(self._n_cells))
        X = []
        StN = []
        for i in range(self._n_beams):
            E = echo_intensity[:, :, i]
            sv, stn = self._scalar_counts_to_absolute_backscatter(E, E_r, float(k_c[i+1]), alpha, C, bin_distances, temperature, transmit_pulse_length, P_dbw)
            # print(k_c[i+1])
            # quit()
            X.append(sv)
            StN.append(stn)
        X = np.array(X).transpose(1, 2, 0).astype(int).astype(float)  # Shape: (n_ensembles, n_cells, n_beams) Absolute backscatter
        StN = np.array(StN).transpose(1, 2, 0).astype(int).astype(float)  # Shape: (n_ensembles, n_cells, n_beams) Signal to noise ratio
        return X, StN

    @staticmethod
    def _scalar_counts_to_absolute_backscatter(E, E_r, k_c, alpha, C, R, Tx_T, Tx_PL, P_DBW):
        """
        Vectorized Absolute Backscatter Equation from Deines (Updated - Mullison 2017 TRDI Application Note FSA031)
        
        Parameters
        ----------
        E : ndarray
            Measured Returned Signal Strength Indicator (RSSI) amplitude, in counts.
        R : ndarray
            Along-beam range to the measurement in meters.
        Tx_T : ndarray
            Transducer temperature in deg C.
        Tx_PL : ndarray
            Transmit pulse length in dBm.
        E_r : float
            Measured RSSI amplitude in absence of signal (noise), in counts.
        k_c : float
            Factor to convert amplitude counts to decibels (dB).
        alpha : float
            Acoustic absorption (dB/m).
        C : float
            Constant combining several parameters specific to the instrument.
        P_DBW : float
            Transmit pulse power in dBW.
        
        Returns
        -------
        Sv : ndarray
            Apparent volume scattering strength.
        StN : ndarray
            True signal to noise ratio.
        """
        
        # Signal to noise ratio (true)
        E_db = k_c * E / 10
        E_r_db = k_c * E_r / 10
        
        StN = (10 ** E_db - 10 ** E_r_db) / (10 ** E_r_db)
        
        # L_DBM: Transmit pulse length in dBm
        L_DBM = 10 * np.log10(Tx_PL)
        
        Sv = (
            C
            + 10 * np.log10((Tx_T + 273.16) * (R ** 2))
            - L_DBM
            - P_DBW
            + 2 * alpha * R
            + 10 * np.log10(10 ** (0.1 * k_c * (E - E_r)) - 1)
        )
        
        return Sv, StN        

    @classmethod    
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
    
    @classmethod
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
    
    @classmethod    
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
            fig, ax = PlottingShell.subplots(nrow=self.adcp.n_beams, ncol=1, figheight=5, figwidth=7, sharex=True, sharey=False)
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