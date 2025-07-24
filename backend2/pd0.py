from pathlib import Path
import numpy as np
from struct import unpack
from dataclasses import dataclass
import re
from datetime import datetime
import warnings
import os
import struct
from typing import List, Dict, Any, Tuple, Literal, Union
import numpy as np
from tqdm import tqdm

from ._pd0_fields import Pd0Formats, FieldDef
from .utils import Utils, Constants

@dataclass
class _DataCodeID:
    data_id_code: int

    def __repr__(self):
        return f"_DataCodeID(data_id_code={self.data_id_code})"

def clean_field_name(name: str) -> str:
    name = name.replace(" ", "_")
    name = re.sub(r'[^0-9a-zA-Z_]', '', name)
    if name and name[0].isdigit():
        name = "_" + name
    return name.lower()

@dataclass
class BasePd0Section:
    def __init__(self, field_defs: List[FieldDef], values_dict: Dict[str, any] = None):
        self._field_name_map = {}
        values_dict = values_dict or {}

        for field_def in field_defs:
            original_name = field_def.name
            clean_name = clean_field_name(original_name)
            self._field_name_map[clean_name] = original_name
            value = values_dict.get(original_name, np.nan)
            setattr(self, clean_name, value)

    def to_dict(self):
        """Returns a dict of clean_name → value"""
        return {attr: getattr(self, attr) for attr in self._field_name_map}

    def to_original_dict(self):
        """Returns a dict of original field name → value"""
        return {original: getattr(self, clean) for clean, original in self._field_name_map.items()}

class Header(BasePd0Section):
    def __init__(self, values_dict: Dict[str, any] = None):
        super().__init__(Pd0Formats.ensemble_header, values_dict)
        self.velocity_id: _DataCodeID = _DataCodeID(np.nan)
        self.id_code_4: _DataCodeID = _DataCodeID(np.nan)
        self.id_code_5: _DataCodeID = _DataCodeID(np.nan) 
        self.id_code_6: _DataCodeID = _DataCodeID(np.nan) 
        self.address_offset: List[int] = []

    def __repr__(self):
        text = f"Header:\n"
        for field, value in self.__dict__.items():
            if not field.startswith('_'):
                text += f"  {field}: {value}\n"
        return text

class FixedLeader(BasePd0Section):
    def __init__(self, values_dict: Dict[str, any] = None):
        super().__init__(Pd0Formats.fixed_leader, values_dict)

    def __repr__(self):
        text = f"FixedLeader:\n"
        for field, value in self.__dict__.items():
            if not field.startswith('_'):
                text += f"  {field}: {value}\n"
        return text

class VariableLeader(BasePd0Section):
    def __init__(self, values_dict: Dict[str, any] = None):
        super().__init__(Pd0Formats.variable_leader, values_dict)

    def __repr__(self):
        text = f"VariableLeader:\n"
        for field, value in self.__dict__.items():
            if not field.startswith('_'):
                text += f"  {field}: {value}\n"
        return text

class BottomTrack(BasePd0Section):
    def __init__(self, values_dict: Dict[str, any] = None):
        super().__init__(Pd0Formats.bottom_track, values_dict)

    def __repr__(self):
        text = f"BottomTrack:\n"
        for field, value in self.__dict__.items():
            if not field.startswith('_'):
                text += f"  {field}: {value}\n"
        return text

class SystemConfiguration:
    def __init__(self):
        self.beam_facing = None
        self.xdcr_hd = None
        self.sensor_config = None
        self.beam_pattern = None
        self.frequency = None
        self.janus_config = None
        self.beam_angle = None

    def __repr__(self):
        return (f"SystemConfiguration(beam_facing={self.beam_facing}, "
                f"xdcr_hd={self.xdcr_hd}, sensor_config={self.sensor_config}, "
                f"beam_pattern={self.beam_pattern}, frequency={self.frequency}, "
                f"janus_config={self.janus_config}, beam_angle={self.beam_angle})")

class ExternalFields:
    def __init__(self, values_dict: Dict[str, any] = None):
        self.leader_id = next((values_dict[k] for k in ['leader_id', 'LEADER ID'] if k in values_dict), 6241)
        self.geodetic_datum = next((values_dict[k] for k in ['geodetic_datum', 'GEODETIC DATUM'] if k in values_dict), 'NONE')
        self.vertical_datum = next((values_dict[k] for k in ['vertical_datum', 'VERTICAL DATUM'] if k in values_dict), 'SEAFLOOR')
        self.magnetic_declination = next((values_dict[k] for k in ['magnetic_declination', 'MAGNETIC DECLINATION'] if k in values_dict), 0)
        self.utc_offset = next((values_dict[k] for k in ['utc_offset', 'UTC OFFSET'] if k in values_dict), 0)
        self.crp_x = next((values_dict[k] for k in ['crp_x', 'CRP X'] if k in values_dict), 0)
        self.crp_y = next((values_dict[k] for k in ['crp_y', 'CRP Y'] if k in values_dict), 0)
        self.crp_z = next((values_dict[k] for k in ['crp_z', 'CRP Z'] if k in values_dict), 0)
        self.site_name = next((values_dict[k] for k in ['site_name', 'SITE NAME'] if k in values_dict), 'NONE')
        self.surveyor = next((values_dict[k] for k in ['surveyor', 'SURVEYOR'] if k in values_dict), 'NONE')
        self.deployment_id = next((values_dict[k] for k in ['deployment_id', 'DEPLOYMENT ID'] if k in values_dict), 'NONE')
        self.x = next((values_dict[k] for k in ['x', 'X'] if k in values_dict), 0)
        self.y = next((values_dict[k] for k in ['y', 'Y'] if k in values_dict), 0)
        self.z = next((values_dict[k] for k in ['z', 'Z'] if k in values_dict), 0)
        self.pitch = next((values_dict[k] for k in ['pitch', 'PITCH'] if k in values_dict), 0)
        self.roll = next((values_dict[k] for k in ['roll', 'ROLL'] if k in values_dict), 0)
        self.yaw = next((values_dict[k] for k in ['yaw', 'YAW'] if k in values_dict), 0)
        self.turbidity = next((values_dict[k] for k in ['turbidity', 'TURBIDITY'] if k in values_dict), 0)
        self.rssi_beam_1 = next((values_dict[k] for k in ['rssi_beam_1', 'RSSI BEAM 1'] if k in values_dict), 0.45)
        self.rssi_beam_2 = next((values_dict[k] for k in ['rssi_beam_2', 'RSSI BEAM 2'] if k in values_dict), 0.45)
        self.rssi_beam_3 = next((values_dict[k] for k in ['rssi_beam_3', 'RSSI BEAM 3'] if k in values_dict), 0.45)
        self.rssi_beam_4 = next((values_dict[k] for k in ['rssi_beam_4', 'RSSI BEAM 4'] if k in values_dict), 0.45)
        self.rssi_beam_5 = next((values_dict[k] for k in ['rssi_beam_5', 'RSSI BEAM 5'] if k in values_dict), 0.45)
        self.rssi_beam_6 = next((values_dict[k] for k in ['rssi_beam_6', 'RSSI BEAM 6'] if k in values_dict), 0.45)
        
class Ensemble:
    def __init__(self, ensemble_header: Header, fixed_leader: FixedLeader, variable_leader: VariableLeader,
                 velocity: np.ndarray, correlation_magnitude: np.ndarray, echo_intensity: np.ndarray, percent_good: np.ndarray) -> None:
        self.ensemble_header: Header = ensemble_header
        self.fixed_leader: FixedLeader = fixed_leader
        self.variable_leader: VariableLeader = variable_leader
        self.velocity: np.ndarray = velocity
        self.correlation_magnitude: np.ndarray = correlation_magnitude
        self.echo_intensity: np.ndarray = echo_intensity
        self.percent_good: np.ndarray = percent_good
        self.bottom_track: BottomTrack = None
        self.reserved_bit_data: Dict[str, Any] = {}
        self.system_configuration: SystemConfiguration = None
        self.coordinate_system: str = None
        self.checksum_passed: bool = False 
        self.external_fields: ExternalFields = None

class Pd0Decoder:
    def __init__(self, filepath: str | Path, cfg: Dict[str, Any]) -> None:
        """
        Initialize the Pd0Decoder with the path to the binary PD0 file.

        Parameters:
            file_path (str): Path to the binary PD0 file.
        """
        self.logger = Utils.get_logger()
        self.filepath = Utils._validate_file_path(filepath, Constants._PD0_SUFFIX)
        self.cfg = cfg
        self.progress_bar = self.cfg.get('progress_bar', "True").lower() in ['true', '1', 'yes']
        self._instrument_depth = float(self.cfg.get('instrument_depth', 0.0))
        self._instrument_HAB = float(self.cfg.get('instrument_HAB', 0.0))
        self.name = self.cfg.get('name', self.filepath.stem)
        self.filesize = self.filepath.stat().st_size
        self.fobject = open(self.filepath, 'rb')
        self._first_ensemble_pos = self._find_first_ensemble()
        self._header, self._fixed, self._variable = self._get_info()
        self._n_data_types = self._header.n_data_types
        self._n_bytes_in_ensemble = self._header.n_bytes_in_ensemble
        self._n_cells = self._fixed.number_of_cells_wn
        self._n_beams = self._fixed.number_of_beams
        self._n_ensembles = self.filesize // self._n_bytes_in_ensemble
        self._beam_facing = self._fixed.system_configuration.beam_facing.lower()
        self._depth_cell_length = self._fixed.depth_cell_length_ws
        self._bin_1_distance = self._fixed.bin_1_distance
        self._beam_angle = self._fixed.beam_angle
        self._approximate_n_ensembles = True
        
        


    def _find_first_ensemble(self, max_iter: int = 100) -> int:
        """
        Find the next ensemble start position in the PD0 file.
        Parameters:
        ----------
        length : int
            The number of bytes to search for a valid ensemble in it.
        max_iter : int
            The maximum number of iterations to search for a valid ensemble.
        Returns:
        -------
        int
            The start position of the next ensemble in the file.
        """
        self.fobject.seek(0)
        valid = False
        pos = 0
        iter_count = 0
        while not valid and iter_count < max_iter:
            self.fobject.seek(pos)
            try:
                header = self.decode_fields(Pd0Formats.ensemble_header, 0)
            except Exception as e:
                Utils.error(
                    logger=self.logger,
                    msg=f"Failed to decode header at position {pos}: {e}",
                    exc=ValueError,
                    level=self.__class__.__name__
                )
                
            if header is not None:
                self.fobject.seek(0)  # Reset to the beginning of the file
                return pos
            else:
                iter_count += 1
        if iter_count >= max_iter:
            Utils.error(
                logger=self.logger,
                msg=f"No valid header found in the file after {max_iter} iterations.",
                exc=ValueError,
                level=self.__class__.__name__
            )

    def _get_info(self, initial_offset=0) -> Tuple[Header, FixedLeader, VariableLeader]:
        self.fobject.seek(initial_offset)
        header = Header(self.decode_fields(Pd0Formats.ensemble_header, 0))
        n_data_types = header.n_data_types if header.n_data_types is not np.nan else 0
        address_offsets = []
        for i in range(n_data_types):
            value, _ = self._decode_field(Pd0Formats.address_offsets[0])
            address_offsets.append(value)
        header.address_offset = address_offsets        
        fixed_leader = FixedLeader(self.decode_fields(Pd0Formats.fixed_leader))
        fixed_leader.system_configuration = self.decode_system_configuration(fixed_leader.system_configuration)
        variable_leader = VariableLeader(self.decode_fields(Pd0Formats.variable_leader))
        return header, fixed_leader, variable_leader
        
    def _get_bin_midpoints(self) -> np.ndarray:
        """
        Get the midpoints of the bins.
        
        Returns:
        -------
        np.ndarray
            Midpoints of the bins with shape (n_cells,).
        """
        beam_length = self._n_cells * self._depth_cell_length
        bin_midpoints = np.linspace(
            self._bin_1_distance,
            beam_length + self._bin_1_distance,
            self._n_cells
        )
        return bin_midpoints / 100.0
    
    def _get_bin_midpoints_depth(self) -> np.ndarray:
        """
        Get the midpoints of the bins in depth.
        
        Returns:
        -------
        np.ndarray
            Midpoints of the bins in depth with shape (n_cells,).
        """
        if self._beam_facing == "up":
            bin_midpoints = self._instrument_depth - self._get_bin_midpoints()
        else:
            bin_midpoints = self._instrument_depth + self._get_bin_midpoints()
        return bin_midpoints
    
    def _get_bin_midpoints_hab(self) -> np.ndarray:
        """
        Get the midpoints of the bins in height above bed (HAB).
        
        Returns:
        -------
        np.ndarray
            Midpoints of the bins in HAB with shape (n_cells,).
        """
        if self._beam_facing == "up":
            bin_midpoints = self._instrument_HAB + self._get_bin_midpoints()
        else:
            bin_midpoints = self._instrument_HAB - self._get_bin_midpoints()
        return bin_midpoints

    def _decode_field(self, field: FieldDef) -> Tuple[Any, bytes]:
        fmtstr = f"{field.endian}{field.fmt}"
        nbytes = struct.calcsize(fmtstr)
        field_bytes = self.fobject.read(nbytes)
        if len(field_bytes) < nbytes:
            value = None
        else:
            value = struct.unpack(fmtstr, field_bytes)[0]
        if not field.decode:
            value = field_bytes
        return value, nbytes

    def decode_fields(self, fields: List[FieldDef], initial_offset: int = 0) -> Dict[str, Any]:
        """
        Decode fields from the binary file based on the provided field definitions.

        Parameters:
            fields (List[FieldDef]): List of FieldDef objects defining the fields to decode.
            initial_offset (int): Initial offset in the file to start decoding.

        Returns:
            Tuple[Dict[str, Any], int]: A dictionary of decoded field values and the total bytes read.
        """
        result = {}
        offset = initial_offset
        if offset > 0:
            self.fobject.read(offset)
        for field in fields:
            value, nbytes = self._decode_field(field)
            result[field.name] = value
            offset += nbytes
        return result

    def get_LE_bit_string(self, byte: bytes) -> str:
        """
        make a bit string from little endian byte

        Args:
            byte: a byte
        Returns:
            a string of ones and zeros, the bits in the byte
        """
        # surely there's a better way to do this!!
        bits = ""
        for i in [7, 6, 5, 4, 3, 2, 1, 0]:  # Little Endian
            if (byte >> i) & 1:
                bits += "1"
            else:
                bits += "0"
        return bits

    def decode_system_configuration(self, syscfg: str) -> SystemConfiguration:
        """
        determine the system configuration parameters from 2-byte hex

        Args:
            syscfg: 2-byte hex string 
        Returns:
            SystemConfiguration: a SystemConfiguration object with the decoded parameters
        """
        try:
            LSB = self.get_LE_bit_string(syscfg[0])
            MSB = self.get_LE_bit_string(syscfg[1])
        except:
            return SystemConfiguration()  # return empty object if decoding fails
        # determine system configuration
        # key for Beam facing
        beam_facing = {'0': 'DOWN', '1': 'UP'}

        # key for XDCR attached
        xdcr_att = {'0': 'NOT ATTACHED', '1': 'ATTACHED'}

        # key for sensor configuration
        sensor_cfg = {'00': '#1', '01': '#2', '10': '#3'}

        # key for beam pattern
        beam_pat = {'0': 'CONCAVE', '1': 'CONVEX'}

        # key for system frequencies
        sys_freq = {'000': '75-kHz', '001': '150-kHz', '010': '300-kHz', '011': '600-kHz', '100': '1200-kHz', '101': '2400-kHz'}

        # determine system configuration from MSB
        janus = {'0100': '4-BM', '0101': '5-BM (DEMOD)', '1111': '5-BM (2 DEMD)'}

        beam_angle = {'00': '15E', '01': '20E', '10': '30E', '11': 'OTHER'}

        system_configuration = SystemConfiguration()
        system_configuration.beam_facing = beam_facing[LSB[0]]
        system_configuration.xdcr_hd = xdcr_att[LSB[1]]
        system_configuration.sensor_config = sensor_cfg[LSB[2:4]]
        system_configuration.beam_pattern = beam_pat[LSB[4]]
        system_configuration.frequency = sys_freq[LSB[5:]]
        try:
            system_configuration.janus_config = janus[MSB[:4]]
        except:
            system_configuration.janus_config = 'UNKNOWN'
        system_configuration.beam_angle = beam_angle[MSB[-2:]]
        
        return system_configuration 

    def _get_fixed_leader(self) -> List[FixedLeader]:
        """
        Get the fixed leader data from the PD0 file.

        Returns:
            List[FixedLeader]: A list of FixedLeader objects for each ensemble.
        """
        self.fobject.seek(0)
        fixed_leaders = []
        for i in tqdm(range(self._n_ensembles), desc="Decoding Fixed Leaders", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + self._header.address_offset[0]
            self.fobject.seek(pos)
            try:
                fixed_leader = FixedLeader(self.decode_fields(Pd0Formats.fixed_leader))
                fixed_leader.system_configuration = self.decode_system_configuration(fixed_leader.system_configuration)
            except:
                Utils.error(
                    logger=self.logger,
                    msg=f"Failed to decode fixed leader at ensemble {i}",
                    exc=ValueError,
                    level=self.__class__.__name__
                )
            if fixed_leader.fixed_leader_id is None:
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            fixed_leaders.append(fixed_leader)
        return fixed_leaders

    def _get_variable_leader(self) -> List[VariableLeader]:
        """
        Get the variable leader data from the PD0 file.

        Returns:
            List[VariableLeader]: A list of VariableLeader objects for each ensemble.
        """
        self.fobject.seek(0)
        variable_leaders = []
        for i in tqdm(range(self._n_ensembles), desc="Decoding Variable Leaders", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + self._header.address_offset[1]
            self.fobject.seek(pos)
            try:
                variable_leader = VariableLeader(self.decode_fields(Pd0Formats.variable_leader))
            except Exception as e:
                Utils.error(
                    logger=self.logger,
                    msg=f"Failed to decode variable leader at ensemble {i}: {e}",
                    exc=ValueError,
                    level=self.__class__.__name__
                )
            if variable_leader.ensemble_number is None:
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            variable_leaders.append(variable_leader)
        return variable_leaders
    
    def _get_datetimes(self) -> List[VariableLeader]:
        """
        Get the variable leader data from the PD0 file.

        Returns:
            List[VariableLeader]: A list of VariableLeader objects for each ensemble.
        """
        self.fobject.seek(0)
        datetimes = []
        first_offset = np.sum([Pd0Formats.variable_leader[i].nbytes for i in [0, 1]])
        for i in tqdm(range(self._n_ensembles), desc="Decoding datetimes", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + self._header.address_offset[1] + first_offset
            self.fobject.seek(pos)
            try:
                data = self.decode_fields(Pd0Formats.variable_leader[2:9])
            except Exception as e:
                Utils.error(
                    logger=self.logger,
                    msg=f"Failed to decode variable leader at ensemble {i}: {e}",
                    exc=ValueError,
                    level=self.__class__.__name__
                )
            if any(d is None for d in data.values()):
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            _ = np.sum([Pd0Formats.variable_leader[i].nbytes for i in range(9,37)])
            _ = self.fobject.read(_)
            century = str(self.decode_fields([Pd0Formats.variable_leader[37]]))
            if not century in ['19','20']: century = '20'
            year = int(century + str(data["RTC YEAR {TS}"]))
            month = int(data["RTC MONTH {TS}"])
            day = int(data["RTC DAY {TS}"])
            hour = int(data["RTC HOUR {TS}"])
            minute = int(data["RTC MINUTE {TS}"])
            second = int(data["RTC SECOND {TS}"])
            hundredth = int(data["RTC HUNDREDTHS {TS}"])
            dt = datetime(year, month, day, hour, minute, second, hundredth * 10000)
            datetimes.append(dt)
        datetimes = np.array(datetimes)
        return datetimes

    def _get_velocity(self) -> np.ndarray:
        self.fobject.seek(0)
        data = []
        break_flag = False
        for i in tqdm(range(self._n_ensembles), desc="Decoding Velocity", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + self._header.address_offset[2]
            self.fobject.seek(pos)
            self._decode_field(Pd0Formats.data_ID_code[0])
            ens_data = []
            for _ in range(self._fixed.number_of_cells_wn):
                cell_data = []
                for __ in range(self._fixed.number_of_beams):
                    value, _ = self._decode_field(Pd0Formats.velocity[0])
                    if value is None:
                        break_flag = True
                        break
                    cell_data.append(value)
                ens_data.append(cell_data)
            if break_flag:
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            data.append(ens_data)
        return np.array(data)

    def _get_variable(self, name: Literal["echo_intensity", "correlation_magnitude", "percent_good"]) -> np.ndarray:
        """
        Wrapper function to get variable data from the PD0 file.
        """
        address_offsets = {
            "correlation_magnitude": self._header.address_offset[3],
            "echo_intensity": self._header.address_offset[4],
            "percent_good": self._header.address_offset[5]
        }

        labels = {
            "correlation_magnitude": "Correlation Magnitude",
            "echo_intensity": "Echo Intensity",
            "percent_good": "Percent Good"
        }

        self.fobject.seek(0)
        data = []
        break_flag = False
        for i in tqdm(range(self._n_ensembles), desc=f"Decoding {labels[name]}", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + address_offsets[name]
            self.fobject.seek(pos)
            self._decode_field(Pd0Formats.data_ID_code[0])
            ens_data = []
            for _ in range(self._fixed.number_of_cells_wn):
                cell_data = []
                for __ in range(self._fixed.number_of_beams):
                    value, _ = self._decode_field(Pd0Formats.variable[0])
                    if value is None:
                        break_flag = True
                        break
                    cell_data.append(value)
                ens_data.append(cell_data)
            if break_flag:
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            data.append(ens_data)
        return np.array(data)

    def _get_echo_intensity(self) -> np.ndarray:
        """
        Get the echo intensity data from the PD0 file.

        Returns:
            np.ndarray: A 2D array of echo intensity values for each ensemble and cell.
        """
        return self._get_variable("echo_intensity")
    
    def _get_correlation_magnitude(self) -> np.ndarray:
        """
        Get the correlation magnitude data from the PD0 file.

        Returns:
            np.ndarray: A 2D array of correlation magnitude values for each ensemble and cell.
        """
        return self._get_variable("correlation_magnitude")
    
    def _get_percent_good(self) -> np.ndarray:
        """
        Get the percent good data from the PD0 file.

        Returns:
            np.ndarray: A 2D array of percent good values for each ensemble and cell.
        """
        return self._get_variable("percent_good")

    def _get_bottom_track(self) -> List[BottomTrack]:
        """
        Get the bottom track data from the PD0 file.

        Returns:
            List[BottomTrack]: A list of BottomTrack objects for each ensemble.
        """
        if self._n_data_types < 7:
            Utils.warning(
                logger=self.logger,
                msg="No bottom track data found in the PD0 file.",
                level=self.__class__.__name__,
            )
            return []
        self.fobject.seek(0)
        bottom_tracks = []
        for i in tqdm(range(self._n_ensembles), desc="Decoding Bottom Track", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + self._header.address_offset[6]
            self.fobject.seek(pos)
            try:
                bottom_track = BottomTrack(self.decode_fields(Pd0Formats.bottom_track))
            except Exception as e:
                Utils.error(
                    logger=self.logger,
                    msg=f"Failed to decode bottom track at ensemble {i}: {e}",
                    exc=ValueError,
                    level=self.__class__.__name__
                )
            if bottom_track.bottom_track_id is None:
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            bottom_tracks.append(bottom_track)
        return bottom_tracks

    def _get_sensor_temperature(self) -> np.ndarray:
        """
        Get the sensor temperature data from the PD0 file.

        Returns:
        --------
            np.ndarray: A 1D array of sensor temperature values for each ensemble.
        """
        self.fobject.seek(0)
        data = []
        for i in tqdm(range(self._n_ensembles), desc="Decoding Sensor Temperature", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + self._header.address_offset[1] + np.sum([Pd0Formats.variable_leader[i].nbytes for i in range(17)]) - 1
            self.fobject.seek(pos)
            value, _ = self._decode_field(Pd0Formats.variable_leader[17])
            if value is None:
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            data.append(value / 100.0)
        return np.array(data)
        
    def _get_sensor_transmit_pulse_length(self) -> np.ndarray:
        """
        Get the sensor transmit pulse length data from the PD0 file.

        Returns:
        --------
            np.ndarray: A 1D array of sensor transmit pulse length values for each ensemble.
        """
        self.fobject.seek(0)
        data = []
        for i in tqdm(range(self._n_ensembles), desc="Decoding Sensor Transmit Pulse Length", unit="ensemble", disable=not self.progress_bar):
            pos = self._first_ensemble_pos + i * (self._n_bytes_in_ensemble + 2) + self._header.address_offset[0] + np.sum([Pd0Formats.fixed_leader[i].nbytes for i in range(25)])
            self.fobject.seek(pos)
            value, _ = self._decode_field(Pd0Formats.variable_leader[17])
            if value is None:
                self._n_ensembles = i
                self._approximate_n_ensembles = False
                break
            data.append(value / 100.0)
        return np.array(data)
        

    def _get_absolute_backscatter(self) -> np.ndarray:
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
        default_rssis = {1: 0.3931, 2: 0.4145, 3: 0.4160, 4: 0.4129}
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

    def __repr__(self) -> str:
        if self._approximate_n_ensembles:
            n_ensembles = "approximately " + str(self._n_ensembles)
        else:
            n_ensembles = str(self._n_ensembles)
        return f"""{self.__class__.__name__}(
        filepath='{self.filepath}',
        n_ensembles={n_ensembles},
        n_cells={self._n_cells},
        n_beams={self._n_beams})
        """
