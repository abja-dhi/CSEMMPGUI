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
from ._adcp_position import ADCPPosition
from .plotting import PlottingShell
from pyproj import CRS, Transformer

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

        self.plot = Plotting(self)

        def get_valid(cfg, key, default):
            # helper for parsing dictionary values
            val = cfg.get(key, default)
            if val is None:
                return default
            try:
                if isinstance(val, float) and np.isnan(val):
                    return default
            except TypeError:
                pass
            return val


        @dataclass
        class ADCPCorrections:
            magnetic_declination: float = field(metadata={"desc": "Degrees CCW to rotate velocity data to account for magnetic declination"})
            utc_offset: float = field(metadata={"desc": "Hours to shift ensemble datetimes to account for UTC offset"})
            transect_shift_x: float = field(metadata={"desc": "Shifting distance of entire ADCP transect for model calibration (X axis, meters)"})
            transect_shift_y: float = field(metadata={"desc": "Shifting distance of entire ADCP transect for model calibration (Y axis, meters)"})
            transect_shift_z: float = field(metadata={"desc": "Shifting distance of entire ADCP transect for model calibration (Z axis, meters)"})
            transect_shift_t: float = field(metadata={"desc": "Shifting time of entire ADCP transect for model calibration (time axis, hours)"})
            
        self.corrections = ADCPCorrections(
            magnetic_declination=float(get_valid(self._cfg, 'magnetic_declination', 0)),
            utc_offset=float(get_valid(self._cfg, 'utc_offset', 0)),
            transect_shift_x=float(get_valid(self._cfg, 'transect_shift_x', 0)),
            transect_shift_y=float(get_valid(self._cfg, 'transect_shift_y', 0)),
            transect_shift_z=float(get_valid(self._cfg, 'transect_shift_z', 0)),
            transect_shift_t=float(get_valid(self._cfg, 'transect_shift_t', 0)),
        )
        
     
        
        
        ## Time class
        @dataclass    
        class ADCPTime:
            n_ensembles: int = field(metadata={"desc": "Number of ensembles in the dataset"})
            ensemble_datetimes: int = field(metadata={"desc": "DateTime corresponding to each ensemble in the dataset"})
            ensemble_numbers: NDArray[np.int64] = field(metadata={"desc": "Number corresponding to each ensemble in the dataset. Read directly from source file"})
          
        self.time = ADCPTime(
            n_ensembles = self._pd0._n_ensembles,
            ensemble_datetimes = self._get_datetimes(),
            ensemble_numbers = self._pd0.get_variable_leader_attr('ensemble_number')
            )
        
        @dataclass
        class ADCPAuxSensorData:
            pressure: NDArray[np.float64] = field(
                metadata={"desc": "Water pressure at the transducer head (dbar), scaled from 0.1 Pa. Range: 0–4,294,967 dbar. Requires external pressure sensor; likely manually specified if absent."}
            )
            pressure_var: NDArray[np.float64] = field(
                metadata={"desc": "Pressure variance (dbar²), scaled from 0.1 Pa². Range: 0–4,294,967 dbar². Requires external pressure sensor; likely manually specified if absent."}
            )
            depth_of_transducer: NDArray[np.float64] = field(
                metadata={"desc": "Depth of transducer below water surface (m), scaled from decimeters. Range: 0.1–999.9 m. May be set manually or computed from pressure sensor."}
            )
            temperature: NDArray[np.float64] = field(
                metadata={"desc": "Water temperature (°C), scaled from 0.01°C. Range: -5.00–40.00°C. Requires external temperature sensor; may be manually set if absent."}
            )
            salinity: NDArray[np.float64] = field(
                metadata={"desc": "Water salinity (PSU), 1:1 scaling. Range: 0–40 PSU. Requires external conductivity sensor; typically manually specified."}
            )
            speed_of_sound: NDArray[np.float64] = field(
                metadata={"desc": "Speed of sound (m/s). Range: 1400–1600 m/s. May be derived from temperature, salinity, and pressure; otherwise, manually set."}
            )
            heading: NDArray[np.float64] = field(
                metadata={"desc": "Instrument heading (°), scaled from 0.01°. Range: 0.00–359.99°. Requires internal compass or external gyro."}
            )
            pitch: NDArray[np.float64] = field(
                metadata={"desc": "Pitch angle (°), scaled from 0.01°. Range: -20.00–20.00°. Requires internal tilt sensor."}
            )
            roll: NDArray[np.float64] = field(
                metadata={"desc": "Roll angle (°), scaled from 0.01°. Range: -20.00–20.00°. Requires internal tilt sensor."}
            )
            heading_std: NDArray[np.float64] = field(
                metadata={"desc": "Heading standard deviation (°). Range: 0–180°. Requires internal or external compass."}
            )
            pitch_std: NDArray[np.float64] = field(
                metadata={"desc": "Pitch standard deviation (°), scaled from 0.1°. Range: 0.0–20.0°. Requires internal tilt sensor."}
            )
            roll_std: NDArray[np.float64] = field(
                metadata={"desc": "Roll standard deviation (°), scaled from 0.1°. Range: 0.0–20.0°. Requires internal tilt sensor."}
            )

            

        
        self.aux_sensor_data = ADCPAuxSensorData(
            pressure=self._pd0.get_variable_leader_attr("pressure") * 0.001,  # decapascal → dbar
            pressure_var=self._pd0.get_variable_leader_attr("pressure_sensor_variance") * 0.001,
            depth_of_transducer=self._pd0.get_variable_leader_attr("depth_of_transducer_ed") * 0.1,  # dm → m
            temperature=self._pd0.get_variable_leader_attr("temperature_et") * 0.01,
            salinity=self._pd0.get_variable_leader_attr("salinity_es"),
            speed_of_sound= self._pd0.get_variable_leader_attr("speed_of_sound_ec"),
            heading=self._pd0.get_variable_leader_attr("heading_eh") * 0.01,
            pitch=self._pd0.get_variable_leader_attr("pitch_tilt_1_ep") * 0.01,
            roll=self._pd0.get_variable_leader_attr("roll_tilt_2_er") * 0.01,
            heading_std=self._pd0.get_variable_leader_attr("hdg_std_dev")*.1,
            pitch_std=self._pd0.get_variable_leader_attr("pitch_std_dev") * 0.1,
            roll_std=self._pd0.get_variable_leader_attr("roll_std_dev") * 0.1,
        )
        
        
        ## Platform Position class
        self.position = ADCPPosition(self._cfg['pos_cfg'])
        

        self.position._resample_to(self.time.ensemble_datetimes)
        
        
        
        if np.all(self.position.heading ==0):
            self.position.heading = self.aux_sensor_data.heading
            
        if np.all(self.position.pitch ==0):
            self.position.pitch = self.aux_sensor_data.pitch  
            
        if np.all(self.position.roll ==0):
            self.position.roll = self.aux_sensor_data.roll
        
        @dataclass
        class ADCPGeometry:
            beam_facing: str = field(metadata={"desc": "Beam direction (Up/Down)"})
            n_bins: float = field(metadata={"desc": "Number of bins"})
            n_beams: float = field(metadata={"desc": "Number of beams"})
            beam_angle: float = field(metadata={"desc": "Beam angle in degrees from vertical"})
            bin_1_distance: float = field(metadata={"desc": "Distance to the center of the first bin (m)"})
            bin_length: float = field(metadata={"desc": "Vertical length of each measurement bin (m)"})
            bin_midpoint_distances: NDArray[np.float64] = field(metadata={"desc": "Array of distances from ADCP to bin centers (m)"})
            beam_dr: float  = field(metadata={"desc": "distance between center of transducer and center of instrument (m)"})
            crp_offset_x: float = field(metadata={"desc": "Offset of ADCP from platform CRP (X axis, meters)"})
            crp_offset_y: float = field(metadata={"desc": "Offset of ADCP from platform CRP (Y axis, meters)"})
            crp_offset_z: float = field(metadata={"desc": "Offset of ADCP from platform CRP (Z axis, meters)"})
            crp_rotation_angle: float = field(metadata={"desc": "CCW rotation of ADCP in casing (degrees)"})
            relative_beam_origin: NDArray[np.float64] = field (metadata = {"desc": "Relative XYZ position of the beams with respect to CRP"})
            relative_beam_midpoint_positions: NDArray[np.float64] = field(metadata={"desc": "XYZ position of each beam/bin/ensemble pair relative to centroid of transducer faces (meters, pos above, neg below)"})
            geographic_beam_midpoint_positions: NDArray[np.float64] = field(metadata={"desc": f"geographic XYZ position of each beam/bin/ensemble pair (meters) , EPSG {self.position.epsg}"})
                    
                
        
        #vh_list = self._pd0._get_variable_leader()  
        
        self.geometry = ADCPGeometry(
            beam_facing=self._pd0.fixed_leaders[0].system_configuration.beam_facing.lower(),
            n_bins=self._pd0.fixed_leaders[0].number_of_cells_wn,
            n_beams=self._pd0.fixed_leaders[0].number_of_beams,
            beam_angle=self._pd0.fixed_leaders[0].beam_angle,
            bin_1_distance=self._pd0.fixed_leaders[0].bin_1_distance / 100,
            bin_length=self._pd0.fixed_leaders[0].depth_cell_length_ws / 100,
            bin_midpoint_distances=None,
            beam_dr =float(get_valid(self._cfg, 'beam_dr', 0.1)),
            crp_offset_x=float(get_valid(self._cfg, 'crp_offset_x', 0)),
            crp_offset_y=float(get_valid(self._cfg, 'crp_offset_y', 0)),
            crp_offset_z=float(get_valid(self._cfg, 'crp_offset_z', 0)),
            crp_rotation_angle=float(get_valid(self._cfg, 'crp_rotation_angle',0)),
            relative_beam_origin = None,
            relative_beam_midpoint_positions=None,
            geographic_beam_midpoint_positions=None,
        )

        self.geometry.bin_midpoint_distances=self._get_bin_midpoints()

        relative_org, relative_bmp, geographic_bmp = self._calculate_beam_geometry()
        self.geometry.relative_beam_midpoint_positions = relative_bmp
        self.geometry.geographic_beam_midpoint_positions = geographic_bmp
        self.geometry.relative_beam_origin  = relative_org  
            
        @dataclass
        class ADCPBeamData:
            echo_intensity: np.ndarray = field(metadata={"desc": "Raw echo intensity from each beam. Unitless ADC counts representing backscatter strength."})
            correlation_magnitude: np.ndarray = field(metadata={"desc": "Correlation magnitude from each beam, used as a data quality metric."})
            percent_good: np.ndarray = field(metadata={"desc": "Percentage of good data for each beam and cell, based on instrument quality control logic."})
            absolute_backscatter: np.ndarray = field(default=None, metadata={"desc": "Calibrated absolute backscatter in dB, derived from raw echo intensity using beam-specific corrections."})
            signal_to_noise_ratio: np.ndarray = field(default=None, metadata={"desc": "SNR in dB, calculated as the difference between backscatter and instrument noise floor."})
            suspended_solids_concentration: np.ndarray = field(default=None, metadata={"desc": "Estimated suspended solids concentration (e.g., mg/L) derived from absolute backscatter using calibration coefficients."})
            sediment_attenuation: np.ndarray = field(default=None, metadata={"desc": "Estimated acoustic power attenuation due to suspended sediments in water (dB/km)"})

        self.beam_data = ADCPBeamData(
            echo_intensity=self._pd0.get_echo_intensity().astype(float),
            correlation_magnitude=self._pd0.get_correlation_magnitude().astype(float),
            percent_good=self._pd0.get_percent_good().astype(float),
            absolute_backscatter = None,  # placeholder until compute
            suspended_solids_concentration=None,  # placeholder until compute 
            signal_to_noise_ratio = None, # placeholder until compute
            sediment_attenuation = None,  # placeholder until compute
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
                    
        bt_list = self._pd0.get_bottom_track()

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
    
    




                 
        ## water properties class
        @dataclass
        class WaterProperties:
            density: NDArray[np.float64] = field(metadata={"desc": "Water density (kg/m³)."})
            salinity: NDArray[np.float64] = field(metadata={"desc": "Water salinity (PSU)."})
            temperature: NDArray[np.float64] = field(metadata={"desc": "Water temperature (°C)."})
            pH: NDArray[np.float64] = field(metadata={"desc": "Water pH (unitless)."})
            pressure: Optional[NDArray[np.float64]] = field(default=None, metadata={"desc": "Water pressure array (deci-bar, )"})
            
        # default typical Singapore coastal values:
        # Density: ~1023 kg/m³, Salinity: ~30 PSU, Temp: ~28°C, pH: ~8.1
        wp_cfg = self._cfg.get('water_properties', {}) # get water rproperties dictionary
        # approximate water pressure based on bin distances. 
        bin_distances = self.geometry.bin_midpoint_distances
        pressure = self.aux_sensor_data.pressure
        pressure = np.outer(pressure, np.ones(self.geometry.n_bins))
        if self.geometry.beam_facing.lower() == 'down':
            pressure += bin_distances * 0.981
        else:
            pressure -= bin_distances * 0.981
           
        # get sensor temperature

        temperature = np.array(get_valid(wp_cfg,'temperature', None))
        if not temperature:
            temperature = self.aux_sensor_data.temperature # if not manual entry, use sensor data
        else:
            temperature = temperature*np.ones(self.time.n_ensembles)# else cast input variable to correct dimension 
        temperature = np.outer(temperature, np.ones(self.geometry.n_bins)) # cast to correct dimensions                      

        self.water_properties = WaterProperties(
            density=np.array(get_valid(wp_cfg, 'density', [1023.0]), dtype=np.float64),
            salinity=np.array(get_valid(wp_cfg, 'salinity', [30.0]), dtype=np.float64),
            temperature=temperature,
            pressure=pressure,
            pH=np.array(get_valid(wp_cfg, 'pH', [8.1]), dtype=np.float64),
        )
                    
        
        ## Sediment properties class
        @dataclass
        class SedimentProperties:
            particle_diameter: NDArray[np.float64] = field(metadata={"desc": "Median particle diameter (µm)."})
            particle_density: NDArray[np.float64] = field(metadata={"desc": "Particle density (kg/m³)."})
        
        # Default: 30 µm diameter (fine silt), 2650 kg/m³ (quartz)
        sed_cfg = self._cfg.get('sediment_properties', {})
        self.sediment_properties = SedimentProperties(
            particle_diameter=np.array(sed_cfg.get('particle_diameter', [30.0]), dtype=np.float64),
            particle_density=np.array(sed_cfg.get('particle_density', [2650.0]), dtype=np.float64),
        )   

        @dataclass
        class SSCParams:
            A: float = field(metadata={"desc": "Parameter A in SSC = A * 10^(B * ABS)"})
            B: float = field(metadata={"desc": "Parameter B in SSC = A * 10^(B * ABS)"})
        
        sscpar_cfg = self._cfg.get('ssc_params', {})
        
        self.ssc_params = SSCParams(
            A=get_valid(sscpar_cfg,'A', 0.05),
            B=get_valid(sscpar_cfg,'B', 5)
        )
                
        
        
        ## absolute backscatter params class
        abs_cfg = self._cfg.get('abs_params', {})
        @dataclass
        class AbsoluteBackscatterParams:
            """Parameters used in calculating absolute backscatter from echo intensity."""
            E_r: float = field(default=39.0, metadata={"desc": "Noise floor (counts)"})
            C: float = field(default=None, metadata={"desc": "System-specific calibration constant (dB)"})
            alpha_s: Optional[NDArray[np.float64]] = field(default=None, metadata={"desc": "Sediment Attenuation coefficient array (dB/m)"})
            alpha_w: Optional[NDArray[np.float64]] = field(default=None, metadata={"desc": "Water Attenuation coefficient array (dB/m)"})
            P_dbw: float = field(default=None, metadata={"desc": "Transmit power (dBW)"})
            WB: float =  field(default=None, metadata={"desc": "System Bandwidth (dBW)"}) 
            rssi: Dict[int, float] = field(default_factory=lambda: {1: 0.41, 2: 0.41, 3: 0.41, 4: 0.41},metadata={"desc": "RSSI scaling factors (counts to decibals) per beam"}),
            frequency: float = field(default=None, metadata={"desc": "System frequency"})
            tx_pulse_length: float = field(default=None, metadata={"desc": "Transmit pule length (m)"})
            
            
        
        # set default Absolute Backscatter params 
        n_beams = self.geometry.n_beams
        n_bins = self.geometry.n_bins
        n_ens = self.time.n_ensembles
        
        # Determine system-specific default C based on bandwidth
        bandwidth = self._pd0.fixed_leaders[0].system_bandwidth_wb
        C = -139.09 if bandwidth == 0 else -149.14
    
        # set default sediment attenuation coefficient  (all zeros)
        alpha_s = np.zeros((n_ens,n_bins,n_beams), dtype = float)
        

        # compute water attenuation coefficient
        pulse_lengths = self._pd0.get_fixed_leader_attr('xmit_pulse_length_based_on_wt')*.01#_get_sensor_transmit_pulse_length()
        bin_depths = abs(self.geometry.geographic_beam_midpoint_positions.z)
        freq = self._pd0.fixed_leaders[0].system_configuration.frequency
        freq = float(freq.split('-')[0])
        
        temperature = self.water_properties.temperature
        
        salinity = self.water_properties.salinity
        density = self.water_properties.density
        pH = self.water_properties.pH
        
        #temp = temperature * np.ones((n_ens, n_bins,n_beams))

        #salinity = salinity * np.ones((n_ens, n_bins,n_beams))
        water_density = density * np.ones((n_ens, n_bins, n_beams))
        
        #pulse_lengths = np.outer(pulse_lengths, np.ones(n_bins))
        bin_distances = np.outer(bin_distances, np.ones(n_ens)).T
        
        alpha_w = self._water_absorption_coeff(
                          T = self.water_properties.temperature,
                          S = self.water_properties.salinity,
                          z = pressure, 
                          f = freq, 
                          pH = pH)
        
        # Default P_dbw based on frequency
        freq_defaults = {
            75:  27.3,
            300: 14.0,
            600:  9.0}
        
        P_dbw = freq_defaults.get(freq, 9)
        
        # Override with config if provided
        C = abs_cfg.get("C", C)
        #alpha = self._cfg.get("absolute_backscatter_alpha", default_alpha)
        P_dbw = abs_cfg.get("P_dbw", P_dbw)
        E_r = abs_cfg.get("E_r", 39.0)
    
        # Beam-specific RSSI from rssi dataclass
        rssi ={1:float(get_valid(abs_cfg,'rssi_beam1', 0.41)),
               2:float(get_valid(abs_cfg,'rssi_beam2', 0.41)),
               3:float(get_valid(abs_cfg,'rssi_beam3', 0.41)),
               4:float(get_valid(abs_cfg,'rssi_beam4', 0.41))}
        
        self.abs_params = AbsoluteBackscatterParams(
                            E_r=E_r,
                            C=C,
                            alpha_s = alpha_s,
                            alpha_w = alpha_w,
                            P_dbw=P_dbw,
                            rssi=rssi,
                            frequency = freq,
                            tx_pulse_length = pulse_lengths,
                            WB = bandwidth)
        
        #calculate absolute backscatter
        ABS,StN = self._calculate_absolute_backscatter()
        self.beam_data.absolute_backscatter = ABS
        self.beam_data.signal_to_noise_ratio = StN
        

        #self.abs_params = self._gen_abs_backscatter_params_from_adcp()
        
        

        
        ## masking attributres class
        @dataclass
        class MaskParams:
            pg_min: float = field(metadata={"desc": "Minimum 'percent good' threshold below which data is masked. Reflects the combined percentage of viable 3 and 4 beam velocity solutions PG1 + PG3. Applies to masks for velocity data only."})
            cormag_min: int = field(metadata={"desc": "Minimum correlation magnitude accepted. Applies to masks for beam data only."})
            cormag_max: int = field(metadata={"desc": "Maximum correlation magnitude accepted. Applies to masks for beam data only."})
            echo_min: int = field(metadata={"desc": "Minimum echo intensity threshold accepted. Applies to masks for beam data only."})
            echo_max: int = field(metadata={"desc": "Maximum echo intensity threshold accepted. Applies to masks for beam data only."})
            abs_min: int = field(metadata={"desc": "Minimum absolute backscatter intensity threshold accepted. Applies to masks for beam data only."})
            abs_max: int = field(metadata={"desc": "Maximum absolute backscatter intensity threshold accepted. Applies to masks for beam data only."})
            vel_min: float = field(metadata={"desc": "Minimum accepted velocity magnitude (m/s). Applies to masks for velocity data only."})
            vel_max: float = field(metadata={"desc": "Maximum accepted velocity magnitude (m/s). Applies to masks for velocity data only."})
            err_vel_max: float = field(metadata={"desc": "Maximum accepted error velocity (m/s). Applies to masks for velocity data only." })
            start_datetime: datetime = field(metadata={"desc": "Start time for valid ensemble masking window. Applies to masks for velocity and beam data."})
            end_datetime: datetime = field(metadata={"desc": "End time for valid ensemble masking window. Applies to masks for velocity and beam data."})
            first_good_ensemble: int = field(metadata={"desc": "Index of first ensemble to retain. Zero based index. Applies to masks for velocity and beam data."})
            last_good_ensemble: int = field(metadata={"desc": "Index of last ensemble to retain. Zero based index. Applies to masks for velocity and beam data."})
            beam_data_mask: NDArray[np.float64] = field(metadata={"desc": "(calculated) Boolean array (n_ens,n_bin,n_beam) contaning composite mask for all beam data variables"})
            vel_data_mask: NDArray[np.float64] = field(metadata={"desc": "(calculated) Boolean array (n_ens,n_bin) contaning composite mask for all velocity data variables"})

            
        self.masking = MaskParams(
            pg_min=float(get_valid(self._cfg, 'pg_min', 0)),
            cormag_min=int(get_valid(self._cfg, 'cormag_min', 0)),
            cormag_max=int(get_valid(self._cfg, 'cormag_max', 255)),
            echo_min=int(get_valid(self._cfg, 'echo_min', 0)),
            echo_max=int(get_valid(self._cfg, 'echo_max', 255)),
            abs_min=int(get_valid(self._cfg, 'abs_min', 0)),
            abs_max=int(get_valid(self._cfg, 'abs_max', Constants._LOW_NUMBER)),
            vel_min=float(get_valid(self._cfg, 'vel_min', Constants._LOW_NUMBER)),
            vel_max=float(get_valid(self._cfg, 'vel_max', Constants._HIGH_NUMBER)),
            err_vel_max=float(get_valid(self._cfg, 'err_vel_max', Constants._HIGH_NUMBER)),
            start_datetime=parser.parse(get_valid(self._cfg, 'start_datetime', Constants._FAR_PAST_DATETIME)),
            end_datetime=parser.parse(get_valid(self._cfg, 'end_datetime', Constants._FAR_FUTURE_DATETIME)),
            first_good_ensemble=int(get_valid(self._cfg, 'first_good_ensemble', 1)),
            last_good_ensemble=int(get_valid(self._cfg, 'last_good_ensemble', self.time.n_ensembles +1)),
            beam_data_mask=None,
            vel_data_mask=None,
        )

        
        
        
        
        #% create bottom track mask 
        #self._generate_bottom_track_mask()
        
        ## TO-DO 
        # Apply masking to beam data and velocity data separately
        # apply bottom track masking 
        # apply bottom track current velocity corrections
        # SSC estimation, with ability to handle Nan values
        # accept SSC conversion parameters A and B
        # add the instrument configuration summary as a method 
        #
    

        
        self._generate_beam_data_masks()
        
        # ABS,SSC,Alpha_s = self._calculate_ssc()
        # self.beam_data.absolute_backscatter = ABS
        # self.beam_data.suspended_sediments_concentration = SSC
        # self.beam_data.sediment_attenuation = Alpha_s

        
        # self.plot = Plotting(self)
        
        # fig,ax = PlottingShell.subplots()
        
        # ax.imshow(self.beam_data.suspended_sediments_concentration[0])
        # plt.imshow(self.beam_data.suspended_sediments_concentration[0], cmap = 'turbo_r')

    def _get_bin_midpoints(self) -> np.ndarray:
        """
        Get the midpoints of the bins as function of distance from the transducer. 
        
        Returns:
        -------
        np.ndarray
            Midpoints of the bins with shape (n_cells,).
        """
        beam_length = self.geometry.n_bins * self.geometry.bin_length
        bin_midpoints = np.linspace(
            self.geometry.bin_1_distance,
            beam_length + self.geometry.bin_1_distance,
            self.geometry.n_bins
        )
        return bin_midpoints 

    def get_beam_data(self, field_name: str, mask: bool = True) -> np.ndarray:
        """
        Retrieve a specific beam data field, optionally masked.
    
        Parameters
        ----------
        field_name : str
            Name of the beam data field to retrieve (e.g., 'echo_intensity', 'correlation_magnitude').
        mask : bool, optional
            If True, returns masked data. If False, returns raw unmasked data.
    
        Returns
        -------
        np.ndarray
            The requested beam data array.
        """
        field_name = field_name.lower().strip()
    
        # Validate field name
        valid_fields = ['echo_intensity', 'correlation_magnitude', 'percent_good',
                        'absolute_backscatter', 'signal_to_noise_ratio',
                        'suspended_solids_concentration', 'sediment_attenuation']
        if field_name not in valid_fields:
            raise ValueError(f"Invalid field name '{field_name}'. Must be one of: {valid_fields}")
    
        data = getattr(self.beam_data, field_name)
       
        if mask:
            data[self.masking.beam_data_mask] = np.nan
        
        return data
        
                       
                       
    def _generate_beam_data_masks(self) -> None:
        
        # Create masks: True = valid , False = invalid 
        
        
        # correlation magnitude
        cmag = self.beam_data.correlation_magnitude
        cmag_mask = (cmag > self.masking.cormag_max) | (cmag < self.masking.cormag_min)
        
        # echo intensity
        echo = self.beam_data.echo_intensity
        echo_mask = (echo > self.masking.echo_max) | (echo < self.masking.echo_min)
        
        # absolute backscatter
        sv = self.beam_data.absolute_backscatter
        sv_mask = (sv > self.masking.abs_max) | (sv < self.masking.abs_min)
        
        # first/last good ensemble 
        ens = np.arange(start = 1, stop = self.time.n_ensembles + 1)
        ens_mask = (ens > self.masking.last_good_ensemble) | (ens < self.masking.first_good_ensemble)
        ens_mask = ens_mask[:, np.newaxis, np.newaxis]
        ens_mask = np.broadcast_to(ens_mask, (self.time.n_ensembles, self.geometry.n_bins, self.geometry.n_beams))

        #start/end dates 
        dt = self.time.ensemble_datetimes
        dt_mask = (dt > self.masking.end_datetime) | (dt < self.masking.start_datetime)
        dt_mask = dt_mask[:, np.newaxis, np.newaxis]
        dt_mask = np.broadcast_to(dt_mask, (self.time.n_ensembles, self.geometry.n_bins, self.geometry.n_beams))

        # print(f"cmag_mask has unmasked values: {np.any(~cmag_mask)}")
        # print(f"echo_mask has unmasked values: {np.any(~echo_mask)}")
        # print(f"sv_mask has unmasked values: {np.any(~sv_mask)}")
        # print(f"ens_mask has unmasked values: {np.any(~ens_mask)}")
        # print(f"dt_mask has unmasked values: {np.any(~dt_mask)}")
        bt_mask = self._generate_bottom_track_mask()

        master_mask = bt_mask
        
        master_mask = np.logical_or.reduce([cmag_mask, echo_mask, sv_mask, ens_mask, dt_mask, ~bt_mask])
        #master_mask = np.logical_or.reduce([sv_mask])
        
        self.masking.beam_data_mask = master_mask
        
 
        
        
        

    def _generate_bottom_track_mask(self, cell_offset: int = 0) -> None:
        """
        Masks beam data below the seabed based on bottom track range.
    
        Parameters
        ----------
        cell_offset : int, optional
            Number of bins to offset the mask above (+) or below (-) the bottom track cell.
            Default is 0, which masks the bottom track cell itself.
        """
        # Get bottom track range (in meters)
        bt_range = self.bottom_track.range_to_seabed  # shape: (n_beams, n_ensembles)
    
        # Expand bottom track range to match beam data shape: (n_beams, n_bins, n_ensembles)
        bt_range_expanded = np.repeat(bt_range[:, np.newaxis, :], self.geometry.n_bins, axis=1)
    
        # Get bin center distances (in meters)
        bin_centers = np.outer(self.geometry.bin_midpoint_distances, np.ones(self.time.n_ensembles))
        bin_centers = np.repeat(bin_centers[np.newaxis, :, :], self.geometry.n_beams, axis=0)
    
        # Apply offset (positive = mask above bottom, negative = below)
        bin_centers += cell_offset * self.geometry.bin_length
    
        # Create mask: True = valid (above bottom), False = invalid (below bottom)
        mask = bin_centers < bt_range_expanded
        mask = mask.T
        
        
        # # Apply mask to beam data fields
        # for attr in ['echo_intensity', 'correlation_magnitude', 'percent_good']:
        #     data = getattr(self.beam_data, attr)
        #     masked_data = np.where(mask, data, np.nan)
        #     setattr(self.beam_data, attr, masked_data)
    
        return mask
        
        
        

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
        datetimes = self._pd0.get_datetimes()
        if apply_corrections:
            delta = timedelta(hours=float(self.corrections.utc_offset)) + \
                    timedelta(hours=float(self.corrections.transect_shift_t))
            datetimes = [dt + delta for dt in datetimes]
        return np.array(datetimes)
    
        
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
        data = self._pd0.get_velocity()
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
        

    # def _calculate_beam_geometry(self) -> XYZ:
    #     """Calculate relative and geoaphic positions of each beam/bin/ensemble pair"""
        
        
    #     theta = self.geometry.crp_rotation_angle
    #     offset_x = self.geometry.crp_offset_x
    #     offset_y = self.geometry.crp_offset_y
    #     offset_z = self.geometry.crp_offset_z
    #     dr = self.geometry.beam_dr
    #     R = Utils.gen_rot_z(theta)
    
    #     if self.geometry.beam_facing == "down":
    #         rel_orig = np.array([(dr, 0, 0), (-dr, 0, 0), (0, dr, 0), (0, -dr, 0)])
    #     else:
    #         rel_orig = np.array([(-dr, 0, 0), (dr, 0, 0), (0, dr, 0), (0, -dr, 0)])
            
    #     rel_orig = rel_orig.dot(R) 
       
    #     rel_orig = np.array([-offset_x, offset_y, offset_z]) + rel_orig
        
    #     rel_orig = rel_orig.T
        
    
    #     n_beams, n_cells, n_ensembles, = self.geometry.n_beams, self.geometry.n_bins, self.time.n_ensembles
    #     beam_angle = self.geometry.beam_angle
    #     rel = np.zeros((3, n_beams, n_cells, n_ensembles))
    
    #     bin_mids = self.geometry.bin_midpoint_distances
    #     if self.geometry.beam_facing == "down":
    #         z_offsets = -bin_mids
    #     else:
    #         z_offsets = bin_mids
    
    #     for b in range(n_beams):
    #         if b in [0, 1]:
    #             R_beam = Utils.gen_rot_y((-1 if b == 0 else 1) * beam_angle)
    #         else:
    #             R_beam = Utils.gen_rot_x((1 if b == 3 else -1) * beam_angle)
    
    #         for e in range(n_ensembles):
    #             midpoints = np.zeros((3, n_cells))
    #             midpoints[2, :] = z_offsets
    #             rel[:, b, :, e] = R_beam @ midpoints
    
    #             yaw = self.position.heading if isinstance(self.position.heading, float) else self.position.heading[e]
    #             pitch = self.position.pitch if isinstance(self.position.pitch, float) else self.position.pitch[e]
    #             roll = self.position.roll if isinstance(self.position.roll, float) else self.position.roll[e]
                
                
    #             R_att = Utils.gen_rot_x(roll) @ Utils.gen_rot_z(yaw) @ Utils.gen_rot_y(pitch)
    #             rel[:, b, :, e] = (rel[:, b, :, e].T @ R_att).T
    

    #     # Absolute positions
    #     if isinstance(self.position.x, float):
    #         xx = np.full(n_ensembles, self.position.x)
    #     else:
    #         xx = self.position.x
    #     if isinstance(self.position.y, float):
    #         yy = np.full(n_ensembles, self.position.y)
    #     else:
    #         yy = self.position.y
    #     if isinstance(self.position.z, float):
    #         zz = np.full(n_ensembles, self.position.z)
    #     else:
    #         zz = self.position.z
    
    #     X_base = np.stack([xx, yy, zz])[:, None, :]
    #     X_base = np.repeat(X_base, n_cells, axis=1)  # shape (3, n_cells, n_ensembles)
    #     X_base = np.repeat(X_base[None, :, :, :], n_beams, axis=0)  # (n_beams, 3, n_cells, n_ensembles)
       
    #     abs_pos = rel + np.transpose(X_base, (1, 0, 2, 3))  # shape (3, n_beams, n_cells, n_ensembles)
    #     abs_pos = abs_pos.transpose(0, 3, 2, 1)  # to (3, ens, cell, beam)
    
    #     relative_beam_midpoint_positions = XYZ(
    #             x=rel[0].transpose(1, 2, 0),
    #             y=rel[1].transpose(1, 2, 0),
    #             z=rel[2].transpose(1, 2, 0),
    #         )
    
    #     geographic_beam_midpoint_positions = XYZ(x=abs_pos[0], y=abs_pos[1], z=abs_pos[2])
        
    #     return rel_orig,relative_beam_midpoint_positions, geographic_beam_midpoint_positions


        
    

    def _calculate_beam_geometry(self):
        
        
        crp_theta = self.geometry.crp_rotation_angle
        off = np.array([self.geometry.crp_offset_x,
                        self.geometry.crp_offset_y,
                        self.geometry.crp_offset_z])
        dr = self.geometry.beam_dr
        R_crp = Utils.gen_rot_z(crp_theta)
    
        # beam bases in body frame (about instrument origin)
        bases = np.array([[ dr, -dr,  0,   0],
                          [  0,   0, dr, -dr],
                          [  0,   0,  0,   0]], dtype=float)

        # CRP rotation + CRP offsets (still body frame)
        rel_orig = (R_crp @ bases) #+ off[:, None]        # (3, n_beams)
    
        n_beams = self.geometry.n_beams
        n_cells = self.geometry.n_bins
        ne = self.time.n_ensembles
        beam_angle = self.geometry.beam_angle
        rel = np.zeros((3, n_beams, n_cells, ne))
    
        bin_mids = self.geometry.bin_midpoint_distances
        z_off = -bin_mids if self.geometry.beam_facing == "down" else bin_mids
    
        # build per-beam tilt matrices in body frame
        for b in range(n_beams):
            if b in (0, 1):
                Rb = Utils.gen_rot_y((-1 if b == 0 else 1) * beam_angle)
            else:
                Rb = Utils.gen_rot_x((1 if b == 3 else -1) * beam_angle)
            # mids = np.zeros((3, n_cells))
            # mids[2, :] = z_off
            # rel[:, b, :, :] = Rb @ mids
            mids = np.zeros((3, n_cells))
            mids[2, :] = z_off
        
            base = Rb @ mids                 # (3, n_cells)
            rel[:, b, :, :] = base[:, :, None]   # -> (3, n_cells, ne)
        # apply attitude and add CRP-offset beam origins (now earth frame, meters)
        for e in range(ne):
            yaw = -(self.position.heading if isinstance(self.position.heading, float) else self.position.heading[e] + crp_theta)
            pitch = self.position.pitch if isinstance(self.position.pitch, float) else self.position.pitch[e]
            roll = self.position.roll if isinstance(self.position.roll, float) else self.position.roll[e]
            R_att = Utils.gen_rot_z(yaw) @ Utils.gen_rot_y(pitch) @ Utils.gen_rot_x(roll)
            for b in range(n_beams):
                #rel[:, b, :, e] = R_att @ rel[:, b, :, e] + (R_att @ rel_orig[:, b])[:, None]
                rel[:, b, :, e] = (
                R_att @ rel[:, b, :, e]
                + (R_att @ rel_orig[:, b])[:, None]
                + (R_att @ (R_crp @ off))[:, None]   # apply offsets after CRP + attitude
            )
    
        # #% update offsets 
        # rel_orig = rel_orig + off[:, None]
        # rel = rel + off[:, None]
        
        # platform positions
        xx = np.full(ne, self.position.x) if isinstance(self.position.x, float) else np.asarray(self.position.x)
        yy = np.full(ne, self.position.y) if isinstance(self.position.y, float) else np.asarray(self.position.y)
        zz = np.full(ne, self.position.z) if isinstance(self.position.z, float) else np.asarray(self.position.z)
    
        src = CRS.from_user_input(self.position.epsg)
        gx = np.empty((ne, n_cells, n_beams))
        gy = np.empty((ne, n_cells, n_beams))
        gz = np.empty((ne, n_cells, n_beams))
    
        for e in range(ne):
            if src.is_geographic:
                lat0, lon0 = float(yy[e]), float(xx[e])
                aeqd = CRS.from_proj4(f"+proj=aeqd +lat_0={lat0} +lon_0={lon0} +ellps=WGS84 +units=m +no_defs")
                fwd = Transformer.from_crs(src, aeqd, always_xy=True)
                inv = Transformer.from_crs(aeqd, src, always_xy=True)
                x0, y0 = fwd.transform(lon0, lat0)
                Xm = x0 + rel[0, :, :, e]     # east (m)
                Ym = y0 + rel[1, :, :, e]     # north (m)
                lon, lat = inv.transform(Xm, Ym)
                gx[e] = lon.T
                gy[e] = lat.T
                gz[e] = (zz[e] + rel[2, :, :, e]).T
            else:
                gx[e] = (xx[e] + rel[0, :, :, e]).T
                gy[e] = (yy[e] + rel[1, :, :, e]).T
                gz[e] = (zz[e] + rel[2, :, :, e]).T
    
        relative_beam_midpoint_positions = XYZ(
            x=rel[0].transpose(2, 1, 0),
            y=rel[1].transpose(2, 1, 0),
            z=rel[2].transpose(2, 1, 0),
        )
        
        rel_orig += off[:, None]  
        geographic_beam_midpoint_positions = XYZ(x=gx, y=gy, z=gz)
    
        return rel_orig, relative_beam_midpoint_positions, geographic_beam_midpoint_positions





    def _counts_to_absolute_backscatter(self, E,E_r, k_c, alpha, C, R, Tx_T, Tx_PL, P_dbw):
        """
        Absolute Backscatter Equation from Deines (Updated - Mullison 2017 TRDI Application Note FSA031)
    
        Parameters
        ----------
        E : ndarray
            Measured echo intensity, in counts.
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
            
        alpha_w : float
            Acoustic absorption of water (dB/m), array of same shape as E.
            
        alpha_s : float
            Acoustic absorption of sediment (dB/m), array of same shape as E.
                    
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
        
        
        E_db = k_c * E / 10
        E_r_db = k_c * E_r / 10
        
    

        # Prevent division by zero and negative log input
        with np.errstate(divide='ignore', invalid='ignore'):
            delta_power = np.maximum(10 ** (0.1 * k_c * (E - E_r)) - 1, 1e-10)
            Sv = (
                C
                + np.log10(np.maximum((Tx_T + 273.16) * (R ** 2), 1e-10)) * 10
                - np.log10(np.maximum(Tx_PL, 1e-10)) * 10
                - P_dbw
                + 2 * alpha * R
                + np.log10(delta_power) * 10
            )
    
            StN = (10 ** E_db - 10 ** E_r_db) / np.maximum(10 ** E_r_db, 1e-10)
    
        Sv = np.where(np.isfinite(Sv), Sv, np.nan)
        StN = np.where(np.isfinite(StN), StN, np.nan)
    
        return Sv, StN
         

    def _calculate_absolute_backscatter(self) -> np.ndarray:
        """
        Convert echo intensity to absolute backscatter.

        Returns:
        --------
            np.ndarray: A 2D array of absolute backscatter values for each ensemble and cell.
        """
        echo_intensity = self._pd0.get_echo_intensity()
        E_r = self.abs_params.E_r
        WB = self.abs_params.WB
        C = self.abs_params.C
        k_c = self.abs_params.rssi
        alpha_w = self.abs_params.alpha_w # water attenuation coefficient 
        alpha_s = self.abs_params.alpha_s # sediment attenuation coefficient 
        P_dbw = self.abs_params.P_dbw
        temperature = self.water_properties.temperature #np.outer(self._pd0._get_sensor_temperature(), np.ones(self.geometry.n_bins))
        bin_distances = np.outer(self.geometry.bin_midpoint_distances, np.ones(self.time.n_ensembles)).T
        transmit_pulse_length = np.outer(self.abs_params.tx_pulse_length, np.ones(self.geometry.n_bins))
    
        # print(f"""
        # echo_intensity mean: {np.mean(echo_intensity)}
        # E_r: {E_r}
        # WB: {WB}
        # C: {C}
        # k_c: {k_c}
        # alpha_w mean: {np.mean(alpha_w)}
        # alpha_s mean: {np.mean(alpha_s)}
        # P_dbw: {P_dbw}
        # temperature mean: {np.mean(temperature)}
        # bin_distances mean: {np.mean(bin_distances)}
        # transmit_pulse_length mean: {np.mean(transmit_pulse_length)}
        # """)


        X = []
        StN = []
        for i in range(self.geometry.n_beams):
            E = echo_intensity[:, :, i]
            alpha = alpha_w + alpha_s[:,:,i]
            sv, stn = self._counts_to_absolute_backscatter(E, E_r, float(k_c[i+1]), alpha, C, bin_distances, temperature, transmit_pulse_length, P_dbw)
            X.append(sv)
            StN.append(stn)
        X = np.array(X).transpose(1, 2, 0).astype(int).astype(float)  # Shape: (n_ensembles, n_cells, n_beams) Absolute backscatter
        StN = np.array(StN).transpose(1, 2, 0).astype(int).astype(float)  # Shape: (n_ensembles, n_cells, n_beams) Signal to noise ratio
        
        return X, StN

 
 
    # def _water_absorption_coeff(self,T, S, z, f, pH):
        
    #     print(f"""
    #     T mean: {np.mean(T)}
    #     S mean: {np.mean(S)}
    #     z mean: {np.mean(z)}
    #     f mean: {np.mean(f)}
    #     pH mean: {np.mean(pH)}
    #     """)
        
    #     c = 1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 + (0.0134 * T) * (S - 35) + 0.016 * z
    
    #     A1 = (8.68 / c) * 10**(0.78 * pH - 5)
    #     P1 = 1
    #     f1 = 2.8 * np.sqrt(S / 35) * 10**(4 - (1245 / (273 + T)))
    
    #     A2 = 21.44 * (S / c) * (1 + 0.025 * T)
    #     P2 = 1 - 1.37e-4 * z + 6.2e-9 * z**2
    #     f2 = (8.17 * 10**(8 - (1990 / (273 + T)))) / (1 + 0.0018 * (S - 35))
    
    #     A3 = np.where(
    #         T <= 20,
    #         4.937e-4 - 2.59e-5 * T + 9.11e-7 * T**2 - 1.5e-8 * T**3,
    #         3.964e-4 - 1.146e-5 * T + 1.45e-7 * T**2 - 6.5e-8 * T**3,
    #     )
    #     P3 = 1 - 3.83e-5 * z + 4.9e-10 * z**2
    
    #     alpha_w = (
    #         A1 * P1 * f1 * f**2 / (f**2 + f1**2) +
    #         A2 * P2 * f2 * f**2 / (f**2 + f2**2) +
    #         A3 * P3 * f**2
    #     )
        
    #     print(f"A3 mean: {np.mean(A3)}, min: {np.min(A3)}")
    #     print(f"P3 mean: {np.mean(P3)}")
    #     print(f"Contribution 3 mean: {np.mean(A3 * P3 * f**2)}")
                
    #     return alpha_w / 1000  # dB/m
    
    def _water_absorption_coeff(self, T, S, z, f, pH):
        """
        Compute acoustic absorption in seawater using the Francois & Garrison (1982) model.
    
        Parameters
        ----------
        T : array_like
            Temperature in °C.
        S : array_like
            Salinity in PSU.
        z : array_like
            Depth in meters.
        f : array_like
            Frequency in kHz.
        pH : array_like
            Seawater pH (unitless).
    
        Returns
        -------
        alpha_w : array_like
            Sound absorption in dB/m.
        """
        T_K = 273 + T  # Temperature in Kelvin
    
        # Sound speed approximation (c in m/s)
        c = 1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 + (0.0134 * T) * (S - 35) + 0.016 * z
    
        # Boric acid contribution
        A1 = (8.686 / c) * 10**(0.78 * pH - 5)
        f1 = 2.8 * np.sqrt(S / 35) * 10**(4 - (1245 / T_K))
    
        # MgSO4 contribution
        A2 = (21.44 * S / c) * (1 + 0.025 * T)
        f2 = (8.17 * 10**(8 - (1990 / T_K))) / (1 + 0.0018 * (S - 35))
    
        # Pure water contribution (temperature-dependent polynomial)
        A3 = np.where(
            T <= 20,
            4.937e-4 - 2.59e-5 * T + 9.11e-7 * T**2 - 1.5e-8 * T**3,
            3.964e-4 - 1.146e-5 * T + 1.45e-7 * T**2 - 6.5e-8 * T**3,
        )
        A3 = np.clip(A3, 0, None)
    
        # Optional pressure corrections (empirical, not in original F&G 1982)
        P2 = 1 - 1.37e-4 * z + 6.2e-9 * z**2
        P3 = 1 - 3.83e-5 * z + 4.9e-10 * z**2
    
        # Total absorption in dB/km
        alpha_dBkm = (
            A1 * (f**2 / (f1**2 + f**2)) +
            A2 * P2 * (f**2 / (f2**2 + f**2)) +
            A3 * P3 * f**2
        )
    
        # Convert to dB/m
        return alpha_dBkm / 1000

    def _sediment_absorption_coeff(self,ps, pw, d, SSC, T, S, f, z):

        c = 1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 + (0.0134 * T) * (S - 35) + 0.016 * z
        v = (40e-6) / (20 + T)
        B = (np.pi * f / v) * 0.5
        delt = 0.5 * (1 + 9 / (B * d))
        sig = ps / pw
        s = 9 / (2 * B * d) * (1 + 2 / (B * d))
        k = 2 * np.pi / c
    
        term1 = k**4 * d**3 / (96 * ps)
        term2 = k * (sig - 1)**2 / (2 * ps)
        term3 = (s / (s**2 + (sig + delt)**2)) * (20 / np.log(10)) * SSC
    
        return term1 + term2 + term3
        
    # def _sediment_absorption_coeff(self, ps, pw, d, SSC, T, S, f, z):
    #     """
    #     Calculate sediment-induced acoustic attenuation (alpha_s) [dB/m] using
    #     visco-inertial absorption and scattering theory for spherical particles.
        
    #     Parameters
    #     ----------
    #     ps : float
    #         Particle density [kg/m³]
    #     pw : array_like
    #         Water density [kg/m³]
    #     d : float
    #         Particle diameter [m]
    #     SSC : array_like
    #         Suspended sediment concentration [mg/L]
    #     T : array_like
    #         Temperature [°C]
    #     S : array_like
    #         Salinity [PSU]
    #     f : float
    #         Acoustic frequency [Hz]
    #     z : array_like
    #         Depth [m]
        
    #     Returns
    #     -------
    #     alpha_s : array_like
    #         Sediment-induced attenuation coefficient [dB/m]
    #     """
    #     import numpy as np
    
    #     # Convert SSC from mg/L to g/L
    #     SSC_gL = SSC #/ 1000.0
    
    #     # Speed of sound [m/s] — Mackenzie (1981) approximation
    #     c = (1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 +
    #          (0.0134 * T) * (S - 35) + 0.016 * z)
    
    #     # Kinematic viscosity [m²/s]
    #     nu = (40e-6) / (20 + T)
    
    #     # Wave number [rad/m]
    #     k = 2 * np.pi * f / c
    
    #     # Inertial term
    #     B = 0.5 * np.pi * f / nu
    #     delta = 0.5 * (1 + 9 / (B * d))
    #     sigma = ps / pw
    #     s = (9 / (2 * B * d)) * (1 + 2 / (B * d))
    
    #     # Scattering and inertial damping terms
    #     term1 = (k**4 * d**3) / (96 * ps)                        # Scattering loss
    #     term2 = (k * (sigma - 1)**2) / (2 * ps)                  # Inertial loss
    
    #     # Viscous absorption term
    #     viscous_term = (s / (s**2 + (sigma + delta)**2))
    #     term3 = viscous_term * (20 / np.log(10)) * SSC_gL       # dB/m

    #     return term1 + term2 + term3
        
 
    def _backscatter_to_ssc(self,backscatter):
        return 10**(self.ssc_params.A + backscatter*self.ssc_params.B)
    
    

   
    def _calculate_ssc(self):
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
        #self.mask.set_mask_status(False)

        # ---------- Instrument + CTD data ----------
        E_r = self.abs_params.E_r
        WB = self._pd0._fixed.system_bandwidth_wb
        C = self.abs_params.C
        
        k_c = {
            1: self.abs_params.rssi[1],
            2: self.abs_params.rssi[2],
            3: self.abs_params.rssi[3],
            4: self.abs_params.rssi[4]
        }
        
        P_dbw = self.abs_params.P_dbw
        
        bin_distances = self.geometry.bin_midpoint_distances
        pulse_lengths = self._pd0._get_sensor_transmit_pulse_length()
        bin_depths = abs(self.geometry.geographic_beam_midpoint_positions.z)
        instrument_freq = self.abs_params.frequency*1000 # in hZ
        
        temperature = self.water_properties.temperature
        pressure = self.aux_sensor_data.pressure
        salinity = self.water_properties.salinity
        density = self.water_properties.density
        
        nc = self.geometry.n_bins
        ne = self.time.n_ensembles
        
        temp = temperature * np.ones((ne, nc)).T
        pressure = np.outer(pressure, np.ones(nc)).T
        salinity = salinity * np.ones((ne, nc)).T
        water_density = density * np.ones((ne, nc)).T
        
        pulse_lengths = np.outer(pulse_lengths, np.ones(nc)).T
        bin_distances = np.outer(bin_distances, np.ones(ne))
        
        print(f"temp shape: {temp.shape}")
        print(f"pressure shape: {pressure.shape}")
        print(f"salinity shape: {salinity.shape}")
        print(f"water_density shape: {water_density.shape}")
        print(f"pulse_lengths shape: {pulse_lengths.shape}")
        print(f"bin_distances shape: {bin_distances.shape}")
        
        if self.geometry.beam_facing.lower() == 'down':
            pressure += bin_distances * 0.98
        else:
            pressure -= bin_distances * 0.98
        
        alpha_w = self._water_absorption_coeff(
            T=temp, S=salinity, z=pressure, f=instrument_freq, pH=7.5)
        
        E = self.beam_data.echo_intensity.T
        
        ABS = self.beam_data.absolute_backscatter.T
        SSC = np.full_like(E, np.nan, dtype=float)
        Alpha_s = np.zeros_like(E, dtype=float)
        
        print(f"echo shape {E.shape}")
        
        for bm in range(self.geometry.n_beams):
            for bn in range(self.geometry.n_bins):
                if bn == 0:
                    ssc_beam_bin = self._backscatter_to_SSC(ABS)[bm, bn]
        
                    for _ in range(100):
                        alpha_s = self._sediment_absorption_coeff(
                            ps=self.sediment_properties.particle_density,
                            pw=water_density[bn],
                            z=pressure[bn],
                            d=self.sediment_properties.particle_diameter,
                            SSC=ssc_beam_bin,
                            T=temp[bn],
                            S=salinity[bn],
                            f=instrument_freq
                        )
                        sv, _ = self._counts_to_absolute_backscatter(
                            E=E[bm, bn],
                            E_r=E_r,
                            k_c=k_c[bm + 1],
                            alpha=alpha_w[bn] + alpha_s,
                            C=C,
                            R=bin_distances[bn],
                            Tx_T=temp[bn],
                            Tx_PL=pulse_lengths[bn],
                            P_dbw=P_dbw
                        )
                        ssc_new = self._backscatter_to_SSC(sv)
                        if np.allclose(ssc_new, ssc_beam_bin, rtol=0, atol=1e-6, equal_nan=True):
                            print('broken')
                            break
                        ssc_beam_bin = ssc_new
        
                    ABS[bm, bn] = sv
                    SSC[bm, bn] = ssc_beam_bin
                    Alpha_s[bm, bn] = alpha_s
        
                else:
                    ssc_beam_bin = np.nanmean(SSC[bm, :bn], axis=0)
                    alpha_s = self._sediment_absorption_coeff(
                        ps=self.sediment_properties.particle_density,
                        pw=water_density[bn],
                        z=pressure[bn],
                        d=self.sediment_properties.particle_diameter,
                        SSC=ssc_beam_bin,
                        T=temp[bn],
                        S=salinity[bn],
                        f=instrument_freq
                    )
                    sv, _ = self._counts_to_absolute_backscatter(
                        E=E[bm, bn],
                        E_r=E_r,
                        k_c=k_c[bm + 1],
                        alpha=alpha_w[bn] + alpha_s,
                        C=C,
                        R=bin_distances[bn],
                        Tx_T=temp[bn],
                        Tx_PL=pulse_lengths[bn],
                        P_dbw=P_dbw
                    )
                    ABS[bm, bn] = sv
                    SSC[bm, bn] = self._backscatter_to_SSC(sv)
                    Alpha_s[bm, bn] = alpha_s
        
                
        return ABS,SSC,Alpha_s
    

            
           
            
           
            
           
            
           
            
           
            
           
            
           
            
           
            
           
            
           
            
           
            
           
#%%

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Union
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import AutoLocator
from matplotlib.collections import LineCollection
import matplotlib as mpl

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors
from matplotlib.ticker import ScalarFormatter
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
    
    
    # _CBAR_LABELS = {
    #     "u": "Eastward Velocity (m/s)",
    #     "v": "Northward Velocity (m/s)",
    #     "w": "Upward Velocity (m/s)",
    #     "CS": "Current Speed (m/s)",
    #     "error_velocity": "Error Velocity (m/s)",
    # }
    
    def __init__(self, adcp: ADCP) -> None:
        self._adcp = adcp

    
    def platform_orientation(self):
        pos = self._adcp.geometry.relative_beam_origin
        
        
        fig, (ax, ax2) = PlottingShell.subplots(
            figheight=6, figwidth=4, nrow=2, height_ratios = [3,1]
        )
        
        # Temporary limit calc for scaling label offsets
        x_span = max(abs(pos[0, :])) or 1
        y_span = max(abs(pos[1, :])) or 1
        r_offset = 0.05 * max(x_span, y_span)
        
        # Metadata dictionary
        meta = {
            'Δx': self._adcp.geometry.crp_offset_x,
            'Δy': self._adcp.geometry.crp_offset_y,
            'Δz': self._adcp.geometry.crp_offset_z,
            'Rotation (° CW)': self._adcp.geometry.crp_rotation_angle,
        }
        
        # --- Top plot: beam geometry ---
        for b in range(self._adcp.geometry.n_beams):
            x = pos[0, b]
            y = pos[1, b]

            ax.scatter(x, y, s=25, c='black', zorder=3, marker = rf'${str(b+1)}$')
        
            # if x != 0 or y != 0:
            #     norm = np.hypot(x, y)
            #     dx = (x / norm) * r_offset
            #     dy = (y / norm) * r_offset
            # else:
            # dx, dy = 0, 0
        
            # ax.annotate(f"{b+1}", (x + dx, y + dy),
            #             ha='center', va='center', fontsize=8,
            #             bbox=dict(boxstyle="round,pad=0.2", fc="none", ec="none", alpha=0.6))
        
        limit = max(max(map(abs, ax.get_xlim())), max(map(abs, ax.get_ylim()))) * 1.2
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal', adjustable='box')
        
        arrow_length = limit * 0.2
        ax.arrow(0, 0, 0, arrow_length,
                 head_width=arrow_length * 0.08, head_length=arrow_length * 0.12,
                 fc='blue', ec='blue', length_includes_head=True, linewidth=1)
        ax.text(0, arrow_length + r_offset, "Vessel direction",
                ha='center', va='bottom', fontsize=8, color='blue')
        
        ax.scatter(0, 0, s=20, marker='s', color='red')
        ax.annotate("Vessel CRP", (0, -r_offset),
                    ha='center', va='top', fontsize=8, color='red',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.6))
        
        mean_x = np.mean(pos[0, :])
        mean_y = np.mean(pos[1, :])
        meta_text = "\n".join(
            f"{k}: {v:.3f}" if isinstance(v, (int, float)) else f"{k}: {v}"
            for k, v in meta.items()
        )
        pad_factor = 0.80
        if abs(mean_x) >= abs(mean_y):
            text_x = -np.sign(mean_x) * limit * pad_factor if mean_x != 0 else -limit * pad_factor
            text_y = 0
        else:
            text_x = 0
            text_y = -np.sign(mean_y) * limit * pad_factor if mean_y != 0 else -limit * pad_factor
        ax.text(text_x, text_y, meta_text,
                ha='center', va='center', fontsize=8,
                bbox=dict(fc="white", ec="none", alpha=0.3))
        
        ax.set_xlabel('Δx (m)')
        ax.set_ylabel('Δy (m)')
        ax.set_title(f'{self._adcp.name} Platform Orientation')
        
        # --- Bottom plot: Z-offset relative to CRP ---
        y = np.mean(pos[1,:])
        z = np.mean(pos[2,:])
        
        ax2.scatter(0, 0, c='red', marker='s', s=10)
        ax2.scatter(y, z, c='black', s=10)
        
        # Determine plot limits for bottom plot
        limit2 = max(max(map(abs, ax2.get_xlim())), max(map(abs, ax2.get_ylim()))) * 1.2
        ax2.set_xlim(-limit2, limit2)
        ax2.set_ylim(-limit2, limit2)
        ax2.set_aspect('equal', adjustable='datalim')
        
        # Water line arrow spanning full x-axis extent
        ax2.arrow(-limit2, 0, 2 * limit2, 0,
                  fc='blue', ec='blue', linestyle='--', alpha=0.5,
                  length_includes_head=True, linewidth=1)
        ax2.text(limit2, 0, "Water line",
                 ha='right', va='bottom', fontsize=8, color='blue', alpha=0.7)
        
        ax2.set_ylabel("Δz (m)")
        ax2.set_xlabel("Δy (m)")
        
        fig.tight_layout()
        plt.show()

    


    
    def transect_animation(
        self,
        figheight: float = 5,
        figwidth: float = 5,
        cmap: str | plt.Colormap = 'viridis',
        vmin: float | None = None,
        vmax: float | None = None,
        show_pos_trail: bool = True,
        show_beam_trail: bool = True,
        pos_trail_len: int | None = None,
        beam_trail_len: int | None = None,
        interval_ms: int = 50,
        cax_label: str = 'Absolute backscatter',
        save_gif: bool = False,
        gif_name: str | None = None
    ) -> FuncAnimation:
        
        
        adcp = self._adcp
        
        t = np.asarray(adcp.time.ensemble_datetimes)
        ens = np.asarray(adcp.time.ensemble_numbers)
        x = np.asarray(adcp.position.x, dtype=float)
        y = np.asarray(adcp.position.y, dtype=float)
        beam_x = np.asarray(adcp.geometry.geographic_beam_midpoint_positions.x, dtype=float)
        beam_y = np.asarray(adcp.geometry.geographic_beam_midpoint_positions.y, dtype=float)
        beam_bs = np.asarray(adcp.get_beam_data(field_name='absolute_backscatter', mask=True), dtype=float)

        mask = np.isfinite(x) & np.isfinite(y)
        if mask.sum() < 2:
            raise ValueError('Not enough finite (x,y) pairs to animate.')
        t, ens, x, y = t[mask], ens[mask], x[mask], y[mask]
        beam_x, beam_y, beam_bs = beam_x[mask], beam_y[mask], beam_bs[mask]
        n_beams = int(beam_x.shape[2])

        fig, ax = PlottingShell.subplots(figheight=figheight, figwidth=figwidth)
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title(f'{adcp.name} vessel track')
        ax.set_aspect('equal', adjustable='datalim')
        # Force plain numeric formatting without scientific notation
        ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        ax.ticklabel_format(style='plain', axis='both')

        
        pad = 0.05
        xmin = np.nanmin([np.nanmin(x), np.nanmin(beam_x)])
        xmax = np.nanmax([np.nanmax(x), np.nanmax(beam_x)])
        ymin = np.nanmin([np.nanmin(y), np.nanmin(beam_y)])
        ymax = np.nanmax([np.nanmax(y), np.nanmax(beam_y)])
        xc, yc = 0.5 * (xmin + xmax), 0.5 * (ymin + ymax)
        r = (1 + pad) * max(max((xmax - xmin) * 0.5, 1e-9), max((ymax - ymin) * 0.5, 1e-9))
        ax.set_xlim(xc - r, xc + r)
        ax.set_ylim(yc - r, yc + r)


        (point,) = ax.plot([], [], 'o', ms=3, zorder=3)
        (trail_line,) = ax.plot([], [], '-', lw=1, alpha=0.85, zorder=2)
        ts_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, ha='left', va='top', fontsize=9)

        if isinstance(cmap, str):
            cmap = plt.get_cmap(cmap).copy()
        else:
            cmap = cmap.copy()
        cmap.set_bad('white')

        if vmin is None or vmax is None:
            finite_bs = beam_bs[np.isfinite(beam_bs)]
            if finite_bs.size == 0:
                vmin_calc, vmax_calc = 0.0, 1.0
            else:
                vmin_calc, vmax_calc = np.nanpercentile(finite_bs, [2, 98])
                if not np.isfinite(vmin_calc) or not np.isfinite(vmax_calc) or vmin_calc == vmax_calc:
                    vmin_calc, vmax_calc = np.nanmin(finite_bs), np.nanmax(finite_bs)
            vmin = vmin if vmin is not None else float(vmin_calc)
            vmax = vmax if vmax is not None else float(vmax_calc)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

        beam_lcs = [LineCollection([], cmap=cmap, norm=norm, linewidths=2, zorder=1) for _ in range(n_beams)]
        for lc in beam_lcs:
            ax.add_collection(lc)

        sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.02, fraction=0.06)
        cbar.set_label(cax_label)

        def _make_segments_for_beam(bx_b, by_b, bs_b):
            x0, x1 = bx_b[:-1], bx_b[1:]
            y0, y1 = by_b[:-1], by_b[1:]
            c0, c1 = bs_b[:-1], bs_b[1:]
            coord_ok = np.isfinite(x0) & np.isfinite(y0) & np.isfinite(x1) & np.isfinite(y1)
            if not np.any(coord_ok):
                return np.empty((0, 2, 2)), np.empty((0,))
            segs = np.stack([np.stack([x0[coord_ok], y0[coord_ok]], axis=1), np.stack([x1[coord_ok], y1[coord_ok]], axis=1)], axis=1)
            colors = 0.5 * (c0 + c1)[coord_ok]
            return segs, colors

        def _accumulate_segments(i, j0, b):
            segs_list, cols_list = [], []
            for k in range(j0, i + 1):
                segs_k, cols_k = _make_segments_for_beam(beam_x[k, :, b], beam_y[k, :, b], beam_bs[k, :, b])
                if segs_k.size:
                    segs_list.append(segs_k)
                    cols_list.append(cols_k)
            if not segs_list:
                return np.empty((0, 2, 2)), np.empty((0,))
            return np.vstack(segs_list), np.concatenate(cols_list)

        def init():
            point.set_data([], [])
            trail_line.set_data([], [])
            for lc in beam_lcs:
                lc.set_segments([])
                lc.set_array(np.array([]))
            ts_text.set_text('')
            return (point, trail_line, *beam_lcs, ts_text)

        def update(i):
            if show_pos_trail:
                j0_pos = 0 if pos_trail_len is None else max(0, i - pos_trail_len)
                trail_line.set_data(x[j0_pos:i+1], y[j0_pos:i+1])
            else:
                trail_line.set_data([], [])
            point.set_data([x[i]], [y[i]])
            j0_beam = i if not show_beam_trail else (0 if beam_trail_len is None else max(0, i - beam_trail_len))
            for b, lc in enumerate(beam_lcs):
                segs, colors = (_accumulate_segments(i, j0_beam, b) if show_beam_trail else _make_segments_for_beam(beam_x[i, :, b], beam_y[i, :, b], beam_bs[i, :, b]))
                lc.set_segments(segs)
                lc.set_array(np.ma.array(colors, mask=np.isnan(colors)))
            ts = mdates.num2date(mdates.date2num(t[i])).strftime('%Y-%m-%d %H:%M:%S')
            ts_text.set_text(f'{ts} (ens #:{int(ens[i])})')
            return (point, trail_line, *beam_lcs, ts_text)

        ani = FuncAnimation(fig, update, frames=len(t), init_func=init, interval=interval_ms, blit=False)

        if save_gif:
            if gif_name is None:
                gif_name = f"{adcp.name} transect animation.gif"
            ani.save(gif_name, dpi=120, fps=1000/interval_ms)
        return ani


 

    def beam_geometry_animation(self, figheight: float = 6,
                                figwidth: float = 7,
                                interval: int = 50,
                                blit: bool = False,
                                show: bool = True,
                                export_gif: bool = False,
                                gif_path: str = None,
                                show_heading: bool = True,
                                heading_length_scale: float = 0.9):
        """
        Animate relative beam geometry in 3D across ensembles.

        Parameters
        ----------
        figheight : float, default 6
            Figure height in inches.
        figwidth : float, default 7
            Figure width in inches.
        interval : int, default 50
            Delay between frames in milliseconds.
        blit : bool, default False
            Whether to use blitting.
        show : bool, default True
            If True, calls ``plt.show()`` at the end.
        export_gif : bool, default False
            If True, exports the animation as a GIF.
        gif_path : str, optional
            Path for saving the GIF. Defaults to "{adcp.name} beam geometry animation.gif".
        show_heading : bool, default True
            If True, draws an arrow at the origin pointing along vessel heading each frame.
        heading_length_scale : float, default 0.9
            Fraction of the global axis limit used for arrow length.

        Returns
        -------
        ani : matplotlib.animation.FuncAnimation
            The animation object.
        ax : matplotlib.axes._subplots.Axes3DSubplot
            The 3D axes used for plotting.
        """
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation, PillowWriter
        from matplotlib import dates as mdates
        from matplotlib.lines import Line2D

        adcp = self._adcp

        # --- Data ---
        t = np.asarray(adcp.time.ensemble_datetimes)
        ens = np.asarray(adcp.time.ensemble_numbers)

        bx = np.asarray(adcp.geometry.relative_beam_midpoint_positions.x, dtype=float)
        by = np.asarray(adcp.geometry.relative_beam_midpoint_positions.y, dtype=float)
        bz = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, dtype=float)

        if bx.ndim != 3 or by.ndim != 3 or bz.ndim != 3:
            raise ValueError("relative_beam_midpoint_positions must be shaped (time, bins, beams)")

        n_t, n_bins, n_beams = bx.shape

        # Heading from adcp.position.heading
        heading_deg = np.mod(np.asarray(adcp.position.heading, dtype=float).reshape(-1), 360.0)

        # --- Figure/Axes ---
        fig, ax = PlottingShell.subplots3d(figheight=figheight, figwidth=figwidth)
        ax.set_title(f"{adcp.name} — Relative Beam Geometry (3D)")
        ax.set_xlabel('Δx (m)')
        ax.set_ylabel('Δy (m)')
        ax.set_zlabel('Δz (m)')
        ax.set_box_aspect((1, 1, 1))

        # --- Global limits ---
        finite = np.isfinite(bx) & np.isfinite(by) & np.isfinite(bz)
        if not np.any(finite):
            raise ValueError("No finite beam midpoint coordinates to animate.")
        maxabs = max(np.nanmax(np.abs(bx[finite])),
                     np.nanmax(np.abs(by[finite])),
                     np.nanmax(np.abs(bz[finite])),
                     1e-9)
        L = 1.1 * maxabs
        ax.set_xlim(-L, L)
        ax.set_ylim(-L, L)
        ax.set_zlim(-L, L)

        # --- Artists ---
        colors = plt.rcParams['axes.prop_cycle'].by_key().get('color', ['C0', 'C1', 'C2', 'C3', 'C4', 'C5'])
        beam_lines, head_markers = [], []
        for b in range(n_beams):
            (ln,) = ax.plot([], [], [], '-', lw=2, color=colors[b % len(colors)], label=f'Beam {b + 1}')
            (mk,) = ax.plot([], [], [], 'o', ms=4, color=colors[b % len(colors)])
            beam_lines.append(ln)
            head_markers.append(mk)

        label = ax.text2D(0.02, 0.98, '', transform=ax.transAxes, ha='left', va='top', fontsize=9)

        heading_quiver = None
        if show_heading:
            heading_proxy = Line2D([0], [0], color='k', lw=2)
            handles, texts = ax.get_legend_handles_labels()
            handles.append(heading_proxy)
            texts.append('Vessel heading')
            ax.legend(handles=handles, labels=texts, loc='upper right', fontsize=8)
        else:
            ax.legend(loc='upper right', fontsize=8)

        # --- Helpers ---
        def _format_ts(ts):
            try:
                return ts.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                return mdates.num2date(mdates.date2num(ts)).strftime('%Y-%m-%d %H:%M:%S')

        def _draw_heading(i):
            nonlocal heading_quiver
            if not show_heading:
                return
            theta = np.deg2rad(float(heading_deg[i]))
            ux = np.sin(theta)
            uy = np.cos(theta)
            if heading_quiver is not None:
                try:
                    heading_quiver.remove()
                except Exception:
                    pass
            heading_quiver = ax.quiver(0.0, 0.0, 0.0,
                                       ux, uy, 0.0,
                                       length=L * heading_length_scale,
                                       normalize=True,
                                       linewidth=2.0,
                                       color='k')

        # --- Animation callbacks ---
        def init():
            for ln, mk in zip(beam_lines, head_markers):
                ln.set_data_3d([], [], [])
                mk.set_data_3d([], [], [])
            label.set_text('')
            _draw_heading(0)
            if heading_quiver is None:
                return (*beam_lines, *head_markers, label)
            return (*beam_lines, *head_markers, label, heading_quiver)

        def update(i):
            for b, (ln, mk) in enumerate(zip(beam_lines, head_markers)):
                xb = bx[i, :, b]
                yb = by[i, :, b]
                zb = bz[i, :, b]
                m = np.isfinite(xb) & np.isfinite(yb) & np.isfinite(zb)
                if np.any(m):
                    ln.set_data_3d(xb[m], yb[m], zb[m])
                    first_idx = np.argmax(m)
                    mk.set_data_3d([xb[first_idx]], [yb[first_idx]], [zb[first_idx]])
                else:
                    ln.set_data_3d([], [], [])
                    mk.set_data_3d([], [], [])
            _draw_heading(i)
            label.set_text(f"{_format_ts(t[i])}  (#{int(ens[i])})")
            if heading_quiver is None:
                return (*beam_lines, *head_markers, label)
            return (*beam_lines, *head_markers, label, heading_quiver)

        # --- Build animation ---
        ani = FuncAnimation(fig, update, frames=n_t, init_func=init, interval=interval, blit=blit)

        # --- Export GIF ---
        if export_gif:
            if gif_path is None:
                gif_path = f"{adcp.name} beam geometry animation.gif"
            ani.save(gif_path, writer=PillowWriter(fps=max(1, 1000 // interval)))

        if show:
            plt.show()

        return ani, ax


    # def flood_plot(self, variable: str, ax: Axes=None, plot_by: str="bin", beam_number: int=1, start_bin: int=None, end_bin: int=None, start_ensemble: int=None, end_ensemble: int=None, vmin: float=None, vmax: float=None, cmap: str = 'turbo_r') -> Axes:
    #     """
    #     Create a flood plot on the given axes.

    #     Parameters
    #     ----------
    #     ax : Axes
    #         The matplotlib Axes object to plot on.
    #     data : np.ndarray
    #         The data to plot.
    #     cmap : mpl.colors.Colormap
    #         The colormap to use for the plot.
    #     """
    #     variable = variable.lower().replace(" ", "_")
    #     start_bin = 0 if start_bin is None else start_bin
    #     end_bin = self.adcp.n_bins-1 if end_bin is None else end_bin
    #     start_ensemble = 0 if start_ensemble is None else start_ensemble
    #     end_ensemble = self.adcp.n_ensembles-1 if end_ensemble is None else end_ensemble
    #     if plot_by.lower() not in ["bin", "depth", "hab"]:
    #         Utils.error(
    #             logger=self.adcp.logger,
    #             msg=f"Invalid plot_by value '{plot_by}'. Must be 'Bin', 'Depth', or 'HAB'.",
    #             exc=ValueError,
    #             level=self.__class__.__name__
    #         )
    #     cmap = cmap #self._CMAPS.get(variable, cmap)
    #     if variable == "percent_good":
    #         data = self.adcp.get_percent_good()
    #     elif variable == "absolute_backscatter":
    #         data = self.adcp.get_absolute_backscatter()
    #     elif variable == "signal_to_noise_ratio":
    #         data = self.adcp.get_signal_to_noise_ratio()
    #     elif variable == "echo_intensity":
    #         data = self.adcp.get_echo_intensity()
    #     elif variable == "correlation_magnitude":
    #         data = self.adcp.get_correlation_magnitude()
    #     elif variable == "filtered_echo_intensity":
    #         data = self.adcp.get_filtered_echo_intensity()
    #     elif variable == "ntu":
    #         data = self.adcp.get_ntu()
    #     elif variable == "ssc":
    #         data = self.adcp.get_ssc()
    #     elif variable == 'u':
    #         data = self.adcp.get_velocity()[0]
    #     elif variable == 'v':
    #         data = self.adcp.get_velocity()[1]
    #     elif variable == 'w':
    #         data = self.adcp.get_velocity()[2]
    #     elif variable == 'cs':
    #         u = self.adcp.get_velocity()[0]
    #         v = self.adcp.get_velocity()[1]
    #         w = self.adcp.get_velocity()[2]
    #         data = np.sqrt(u**2 + v**2 + w**2)
    #     elif variable == 'error_velocity':
    #         data = self.adcp.get_velocity()[6]
    #     else:
    #         Utils.error(
    #             logger=self.adcp.logger,
    #             msg=f"Invalid variable '{variable}'. Must be 'percent_good', 'absolute_backscatter', 'signal_to_noise_ratio', 'echo_intensity', 'correlation_magnitude', 'filtered_echo_intensity', 'ntu', 'ssc', 'u', 'v', 'w', 'CS', or 'error_velocity'.",
    #             exc=ValueError,
    #             level=self.__class__.__name__
    #         )
    #     if plot_by.lower() == "bin":
    #         ylim = (start_bin, end_bin)
    #     elif plot_by.lower() == "depth":
    #         bin_midpoints = self.adcp.get_bin_midpoints_depth()
    #         ylim = (bin_midpoints[start_bin], bin_midpoints[end_bin])
    #     elif plot_by.lower() == "hab":
    #         bin_midpoints = self.adcp.get_bin_midpoints_hab()
    #         ylim = (bin_midpoints[start_bin], bin_midpoints[end_bin])

    #     datetimes = self.adcp.get_datetimes()
    #     if beam_number < 1 or beam_number > self.adcp.n_beams:
    #         Utils.error(
    #             logger=self.adcp.logger,
    #             msg=f"Invalid beam number {beam_number}. Must be between 1 and {self.adcp.n_beams}.",
    #             exc=ValueError,
    #             level=self.__class__.__name__
    #         )
    #     if len(data.shape) == 3:
    #         x = data[start_ensemble:end_ensemble, start_bin:end_bin, beam_number-1]
    #     elif len(data.shape) == 2:
    #         x = data[start_ensemble:end_ensemble, start_bin:end_bin]
    #         data = data[:, :, np.newaxis]  # Add a new axis for compatibility
    #     else:
    #         Utils.error(
    #             logger=self.adcp.logger,
    #             msg=f"Invalid data shape {data.shape}. Expected 2D or 3D array.",
    #             exc=ValueError,
    #             level=self.__class__.__name__
    #         )
    #     if ax is None:
    #         _, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3, figwidth=10.5, sharex=True, sharey=True)
        
    #     topax = ax.twiny()
    #     topax.set_xlim(start_ensemble, end_ensemble)
    #     if plot_by.lower() == "bin":
    #         ax.set_ylabel("Bin", fontsize=8)
    #     elif plot_by.lower() == "depth":
    #         ax.set_ylabel("Depth", fontsize=8)
    #     elif plot_by.lower() == "hab":
    #         ax.set_ylabel("Height Above Bed (m)", fontsize=8)

    #     origin = 'lower' if self.adcp.beam_facing == "up" else 'upper'
        
    #     vmins = {"percent_good": 0, "absolute_backscatter": -95}
    #     vmaxs = {"percent_good": 100, "absolute_backscatter": -10, "signal_to_noise_ratio": 50}
    #     vmin = vmins.get(variable, np.nanmin(data[start_ensemble:end_ensemble, start_bin:end_bin, :])) if vmin is None else vmin
    #     vmax = vmaxs.get(variable, np.nanmax(data[start_ensemble:end_ensemble, start_bin:end_bin, :])) if vmax is None else vmax
        
    #     xlim = mdates.date2num(datetimes[start_ensemble:end_ensemble])
    #     if self.adcp.beam_facing == "up":
    #         extent = (xlim[0], xlim[-1], ylim[0], ylim[-1])
    #     else:
    #         extent = (xlim[0], xlim[-1], ylim[1], ylim[0])
    #     ax = PlottingShell._flood_plot(
    #         ax=ax,
    #         data=x.T,
    #         origin=origin,
    #         extent=extent,
    #         cmap=cmap,
    #         aspect='auto',
    #         resample=False,
    #         vmin=vmin,
    #         vmax=vmax,
    #         cbar_label=self._CBAR_LABELS.get(variable, f"Beam {beam_number}"),
    #     )
    #     ax.xaxis.set_major_locator(mticker.FixedLocator(ax.get_xticks()))
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter(PlottingShell._DATETIME_FORMAT))
    #     ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
    #     ax.xaxis.tick_bottom()
    #     ax.xaxis.set_label_position('bottom')
    #     ax.yaxis.set_major_locator(AutoLocator())

    #     return ax
        
    # def four_beam_flood_plot(self, variable: str, ax: Tuple[Axes, Axes, Axes, Axes] = None, plot_by: str = "bin",
    #                          start_bin: int = None, end_bin: int = None,
    #                          start_ensemble: int = None, end_ensemble: int = None, cmap: str = 'turbo_r') -> Tuple[Axes, Axes, Axes, Axes]:
    #     """
    #     Create a flood plot for the four beams of the ADCP data.
    #     Parameters
    #     ----------
    #     variable : str
    #         The variable to plot, must be one of 'echo_intensity', 'correlation_magnitude', or 'percent_good'.
    #     ax : Axes, optional
    #         The matplotlib Axes object to plot on. If None, a new figure and axes will be created.
    #     plot_by : str, optional
    #         The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
    #     start_bin : int, optional
    #         The starting bin index for the plot. Default is None, which means all bins will be plotted.
    #     end_bin : int, optional
    #         The ending bin index for the plot. Default is None, which means all bins will be plotted.
    #     start_ensemble : int, optional
    #         The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     end_ensemble : int, optional
    #         The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     Returns
    #     -------
    #     Axes
    #         The matplotlib Axes object with the flood plot.
    #     """
    #     if ax is None:
    #         fig, ax = PlottingShell.subplots(nrow=self.adcp.n_beams, ncol=1, figheight=5, figwidth=7, sharex=True, sharey=False)
    #     else:
    #         fig = ax[0].figure

    #     for i in range(self.adcp.n_beams):
    #         ax[i] = self.flood_plot(
    #             variable=variable,
    #             ax=ax[i],
    #             beam_number=i + 1,
    #             plot_by=plot_by,
    #             start_bin=start_bin,
    #             end_bin=end_bin,
    #             start_ensemble=start_ensemble,
    #             end_ensemble=end_ensemble,
    #             cmap = cmap,
    #         )

    #     return ax
    
    


    # def mesh_plot(self, variable: str, ax: Axes = None, beam_number: int = 1,
    #               plot_by: str = "bin", start_bin: int = None, end_bin: int = None,
    #               start_ensemble: int = None, end_ensemble: int = None, vmin: float = None, vmax: float = None) -> Axes:
    #     """        Create a mesh plot on the given axes.
    #     Parameters
    #     ----------
    #     ax : Axes
    #         The matplotlib Axes object to plot on.
    #     variable : str
    #         The variable to plot.
    #     beam_number : int
    #         The beam number to plot (1 to n_beams).
    #     plot_by : str, optional
    #         The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
    #     start_bin : int, optional
    #         The starting bin index for the plot. Default is None, which means all bins will be plotted.
    #     end_bin : int, optional
    #         The ending bin index for the plot. Default is None, which means all bins will be plotted.
    #     start_ensemble : int, optional
    #         The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     end_ensemble : int, optional
    #         The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     Returns
    #     -------
    #     Axes
    #         The matplotlib Axes object with the mesh plot.
    #     """
    #     variable = variable.lower().replace(" ", "_")
    #     start_bin = 0 if start_bin is None else start_bin
    #     end_bin = self.adcp.n_bins-1 if end_bin is None else end_bin
    #     start_ensemble = 0 if start_ensemble is None else start_ensemble
    #     end_ensemble = self.adcp.n_ensembles-1 if end_ensemble is None else end_ensemble
    #     if plot_by.lower() not in ["bin", "depth", "hab"]:
    #         Utils.error(
    #             logger=self.adcp.logger,
    #             msg=f"Invalid plot_by value '{plot_by}'. Must be 'Bin', 'Depth', or 'HAB'.",
    #             exc=ValueError,
    #             level=self.__class__.__name__
    #         )
    #     cmap = self._CMAPS.get(variable, plt.cm.viridis)
    #     if variable == "percent_good":
    #         data = self.adcp.get_percent_good()
    #     elif variable == "absolute_backscatter":
    #         data = self.adcp.get_absolute_backscatter()
    #     elif variable == "signal_to_noise_ratio":
    #         data = self.adcp.get_signal_to_noise_ratio()
    #     elif variable == "echo_intensity":
    #         data = self.adcp.get_echo_intensity()
    #     elif variable == "correlation_magnitude":
    #         data = self.adcp.get_correlation_magnitude()
    #     elif variable == "filtered_echo_intensity":
    #         data = self.adcp.get_filtered_echo_intensity()
    #     elif variable == "ntu":
    #         data = self.adcp.get_ntu()
    #     elif variable == "ssc":
    #         data = self.adcp.get_ssc()
    #     else:
    #         Utils.error(
    #             logger=self.adcp.logger,
    #             msg=f"Invalid variable '{variable}'. Must be 'percent_good', 'absolute_backscatter', or 'signal_to_noise_ratio'.",
    #             exc=ValueError,
    #             level=self.__class__.__name__
    #         )
    #     if plot_by.lower() == "bin":
    #         Z = self.adcp.relative_beam_midpoint_positions.z[:, :, beam_number-1]
    #         z_platform = (self.adcp.bin_1_distance / 100) + np.zeros(self.adcp.get_bottom_track().shape[0])
    #         ylim = (np.nanmin(Z), np.nanmax(Z))
    #     elif plot_by.lower() == "depth":
    #         Z = self.adcp.absolute_beam_midpoint_positions.z[:, :, beam_number-1]
    #         z_platform = self.adcp.position.coords.z
    #         ylim = (np.nanmin(Z), np.nanmax(Z))
    #     elif plot_by.lower() == "hab":
    #         Z = self.adcp.absolute_beam_midpoint_positions_hab.z[:, :, beam_number-1]
    #         z_platform = self.adcp.get_bottom_track()[:, beam_number-1]
    #         ylim = (0, 1.1*np.nanmax(z_platform))
    #     Z = Z[start_ensemble:(end_ensemble+1), start_bin:(end_bin+1)]
    #     z_platform = z_platform[start_ensemble:(end_ensemble+1)]

    #     datetimes = self.adcp.get_datetimes()[start_ensemble:(end_ensemble+1)]
    #     if beam_number < 1 or beam_number > self.adcp.n_beams:
    #         Utils.error(
    #             logger=self.adcp.logger,
    #             msg=f"Invalid beam number {beam_number}. Must be between 1 and {self.adcp.n_beams}.",
    #             exc=ValueError,
    #             level=self.__class__.__name__
    #         )
    #     x = data[start_ensemble:end_ensemble, start_bin:end_bin, beam_number-1]
    #     if ax is None:
    #         _, ax = PlottingShell.subplots(nrow=1, ncol=1, figheight=3, figwidth=10.5, sharex=True, sharey=True)
        
    #     # topax = ax.twiny()
    #     # topax.set_xlim(start_ensemble, end_ensemble)
    #     # if plot_by.lower() == "bin":
    #     #     ax.set_ylabel("Bin", fontsize=8)
    #     # elif plot_by.lower() == "depth":
    #     #     ax.set_ylabel("Depth", fontsize=8)
    #     # elif plot_by.lower() == "hab":
    #     #     ax.set_ylabel("Height Above Bed (m)", fontsize=8)

    #     vmins = {"percent_good": 0, "absolute_backscatter": -95, "ntu": 0}
    #     vmaxs = {"percent_good": 100, "absolute_backscatter": -45, "signal_to_noise_ratio": 50}
    #     vmin = vmins.get(variable, np.nanmin(x)) if vmin is None else vmin
    #     vmax = vmaxs.get(variable, np.nanmax(x)) if vmax is None else vmax
    #     T = np.repeat(datetimes[:, np.newaxis], self.adcp.n_cells, axis=1)[:, start_bin:(end_bin+1)]
    #     ax = PlottingShell._mesh_plot(
    #         ax=ax,
    #         X = T,
    #         Y = Z,
    #         C = x,
    #         vmin=vmin,
    #         vmax=vmax,
    #         cmap=cmap,
    #         cbar_label=f"Beam {beam_number}",
    #         orientation="vertical",
    #         location="right",
    #         fraction=0.046,
    #         rotation=90,
    #         fontsize=8,
    #         T=datetimes,
    #         Z=z_platform,
    #         color="black",
    #         linewidth=1.0,
    #         alpha=0.7,
    #         Z_label="ROV (z)",
    #         ylim=ylim,
    #     )
    #     ax.xaxis.set_major_locator(mticker.FixedLocator(ax.get_xticks()))
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter(PlottingShell._DATE_FORMAT))
    #     ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
    #     ax.xaxis.tick_bottom()
    #     ax.xaxis.set_label_position('bottom')
    #     ax.yaxis.set_major_locator(AutoLocator())

    #     return ax


    # def four_beam_mesh_plot(self, variable: str, ax: Tuple[Axes, Axes, Axes, Axes] = None,
    #                          plot_by: str = "bin", start_bin: int = None, end_bin: int = None,
    #                          start_ensemble: int = None, end_ensemble: int = None) -> Tuple[Axes, Axes, Axes, Axes]:
    #     """
    #     Create a mesh plot for the four beams of the ADCP data.
    #     Parameters
    #     ----------
    #     variable : str
    #         The variable to plot, must be one of 'echo_intensity', 'correlation_magnitude', or 'percent_good'.
    #     ax : Axes, optional
    #         The matplotlib Axes object to plot on. If None, a new figure and axes will be created.
    #     plot_by : str, optional
    #         The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
    #     start_bin : int, optional
    #         The starting bin index for the plot. Default is None, which means all bins will be plotted.
    #     end_bin : int, optional
    #         The ending bin index for the plot. Default is None, which means all bins will be plotted.
    #     start_ensemble : int, optional
    #         The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     end_ensemble : int, optional
    #         The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     Returns
    #     -------
    #     Axes
    #         The matplotlib Axes object with the mesh plot.
    #     """
    #     if ax is None:
    #         fig, ax = PlottingShell.subplots(nrow=self.adcp.n_beams, ncol=1, figheight=8, figwidth=10.5, sharex=True, sharey=True)
    #     else:
    #         fig = ax[0].figure

    #     for i in range(self.adcp.n_beams):
    #         ax[i] = self.mesh_plot(
    #             variable=variable,
    #             ax=ax[i],
    #             beam_number=i + 1,
    #             plot_by=plot_by,
    #             start_bin=start_bin,
    #             end_bin=end_bin,
    #             start_ensemble=start_ensemble,
    #             end_ensemble=end_ensemble
    #         )

    #     return ax
    
    # def velocity_plot(self,ax: Tuple[Axes, Axes, Axes, Axes, Axes] = None,
    #                          plot_by: str = "bin", start_bin: int = None, end_bin: int = None,
    #                          start_ensemble: int = None, end_ensemble: int = None) -> Tuple[Axes, Axes, Axes, Axes]:
    #     """
    #     Create a flood plot for the measured velocity with 5 axes for u, v, and w components, current speed, and error velocity.
    #     Parameters
    #     ----------
    #     ax : Axes, optional
    #         The matplotlib Axes object to plot on. If None, a new figure and axes will be created.
    #     plot_by : str, optional
    #         The dimension to plot by, either 'bin', 'depth', or 'HAB'. Default is 'bin'.
    #     start_bin : int, optional
    #         The starting bin index for the plot. Default is None, which means all bins will be plotted.
    #     end_bin : int, optional
    #         The ending bin index for the plot. Default is None, which means all bins will be plotted.
    #     start_ensemble : int, optional
    #         The starting ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     end_ensemble : int, optional
    #         The ending ensemble index for the plot. Default is None, which means all ensembles will be plotted.
    #     Returns
    #     -------
    #     Axes
    #         The matplotlib Axes object with the mesh plot.
    #     """
    #     if ax is None:
    #         fig, ax = PlottingShell.subplots(nrow=5, ncol=1, figheight=8, figwidth=10.5, sharex=True, sharey=True)
    #     else:
    #         fig = ax[0].figure
    #     variables = ['u', 'v', 'w', 'CS', 'error_velocity']
    #     for i, variable in enumerate(variables):
    #         ax[i] = self.flood_plot(
    #             variable=variable,
    #             ax=ax[i],
    #             beam_number=1,
    #             plot_by=plot_by,
    #             start_bin=start_bin,
    #             end_bin=end_bin,
    #             start_ensemble=start_ensemble,
    #             end_ensemble=end_ensemble
    #         )

    #     return ax
    
    
    
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