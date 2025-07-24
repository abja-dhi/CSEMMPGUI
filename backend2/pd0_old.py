from pathlib import Path
import numpy as np
from struct import unpack
import re
from datetime import datetime
import warnings

from ...utils import Utils, Constants

class Ensemble:
    velocity_format = (None, 2, '<', 'h', True)
    coor_mag_format = (None, 1, '<', 'H', True)
    echo_intensity_format = (None, 1, '<', '<H', True)
    pct_good_format = (None, 1, '<', 'H', True)
    def __init__(self) -> None:
        self.header : _EnsembleHeader = None
        self.fixed_leader : _FixedLeader = None
        self.variable_leader : _VariableLeader = None
        self.velocity : np.ndarray = None
        self.correlation_magnitude : np.ndarray = None
        self.echo_intensity : np.ndarray = None
        self.percent_good : np.ndarray = None
        self.bottom_track = None
        self.system_configuration = None
        self.coordinate_system = None

class Metadata:
    def __init__(self, filename: str | Path) -> None:
        self.filename = filename
        self.filesize = filename.stat().st_size
    def Init(self, fe: Ensemble, le: Ensemble) -> None:
        self.first_ensemble_in_file = fe.variable_leader.ensemble_number
        self.last_ensemble_in_file = le.variable_leader.ensemble_number
        self.ensemble_size = fe.header.n_bytes_in_ensemble
        self.first_date_in_file = fe.variable_leader.get_datetime()
        self.first_date_in_file = np.nan if self.first_date_in_file is None else self.first_date_in_file
        self.last_date_in_file = le.variable_leader.get_datetime()
        self.last_date_in_file = np.nan if self.last_date_in_file is None else self.last_date_in_file
        if self.first_ensemble_in_file > self.last_ensemble_in_file:
            self.n_ensemble_in_file = (Constants._ENSEMBLE_COUNT_THRESHOLD - self.first_ensemble_in_file) + self.last_ensemble_in_file
        else:
            self.n_ensemble_in_file = self.last_ensemble_in_file - self.first_ensemble_in_file + 1
        self.first_ensemble_read: int = None
        self.last_ensemble_read: int = None
  
class _EnsembleHeader:
    formats = [
        ('HEADER ID', 1, '<', 'B', True),
        ('DATA SOURCE ID', 1, '<', 'B', True),
        ('N BYTES IN ENSEMBLE', 1, '<', 'H', True),
        ('SPARE', 1, '<', 'B', True),
        ('N DATA TYPES', 1, '<', 'B', True)
        ]
    address_offsets_format = (None, 2, '<', 'H', True)
    data_ID_code_format = (None,2,'<','H',True)
    
    def __init__(self):
        self.id = None
        self.data_source_id = None
        self.n_bytes_in_ensemble = None
        self.spare = None
        self.n_data_types = None
        self.address_offsets = []
        self.velocity_id = None
        self.id_code_4 = None
        self.id_code_5 = None
        self.id_code_6 = None
        self.reserved_bit_data = None
    
class _FixedLeader:
    formats = [
        ('FIXED LEADER ID',2,'<','H',True),
        ('CPU F/W VER.',1,'<','B',True),
        ('CPU F/W REV.',1,'<','B',True),
        ('SYSTEM CONFIGURATION',2,'<','B',False),
        ('REAL/SIM FLAG',1,'<','B',True),
        ('LAG LENGTH',1,'<','B',True),
        ('NUMBER OF BEAMS',1,'<','B',True),
        ('NUMBER OF CELLS {WN}',1,'<','B',True),
        ('PINGS PER ENSEMBLE {WP}',2,'<','H',True),
        ('DEPTH CELL LENGTH {WS}',2,'<','H',True),
        ('BLANK AFTER TRANSMIT {WF}',2,'<','H',True),
        ('PROFILING MODE {WM}',1,'<','B',True),
        ('LOW CORR THRESH {WC}',1,'<','B',True),
        ('NO. CODE REPS',1,'<','B',True),
        ('%GD MINIMUM {WG}',1,'<','B',True),
        ('ERROR VELOCITY MAXIMUM {WE}',2,'<','H',True),
        ('TPP MINUTES',1,'<','B',True),
        ('TPP SECONDS',1,'<','B',True),
        ('TPP HUNDREDTHS {TP}',1,'<','B',True),
        ('COORDINATE TRANSFORM {EX}',1,'<','B',False),
        ('HEADING ALIGNMENT {EA}',2,'<','H',True),
        ('HEADING BIAS {EB}',2,'<','H',True),
        ('SENSOR SOURCE {EZ}',1,'<','B',True),
        ('SENSORS AVAILABLE',1,'<','B',True),
        ('BIN 1 DISTANCE',2,'<','H',True),
        ('XMIT PULSE LENGTH BASED ON {WT}',2,'<','H',True),
        ('starting cell WP REF LAYER AVERAGE {WL} ending cell',2,'<','B',True),
        ('FALSE TARGET THRESH {WA}',1,'<','B',True),
        ('SPARE1',1,'<','B',False),
        ('TRANSMIT LAG DISTANCE',2,'<','H',True),
        ('CPU BOARD SERIAL NUMBER',8,'<','Q',False),
        ('SYSTEM BANDWIDTH {WB}',2,'<','H',True),
        ('SYSTEM POWER {CQ}',1,'<','B',True),
        ('SPARE2',1,'<','B',False),
        ('INSTRUMENT SERIAL NUMBER',4,'<','I',True),
        ('BEAM ANGLE',1,'<','B',True)
        ]
    def __init__(self):
        self.id = None
        self.cpu_fw_ver = None
        self.cpu_fw_rev = None
        self.system_configuration = None
        self.real_sim_flag = None
        self.lag_length = None
        self.number_of_beams = None
        self.number_of_cells = None
        self.pings_per_ensemble = None
        self.depth_cell_length = None
        self.blank_after_transmit = None
        self.profiling_mode = None
        self.low_corr_thresh = None
        self.no_code_reps = None
        self.percent_good_minimum = None
        self.error_velocity_maximum = None
        self.tpp_minutes = None
        self.tpp_seconds = None
        self.tpp_hundredths = None
        self.coordinate_transform = None
        self.heading_alignment = None
        self.heading_bias = None
        self.sensor_source = None
        self.sensors_available = None
        self.bin_1_distance = None
        self.xmit_pulse_length_based_on = None
        self.starting_cell_wp_ref_layer_average = None
        self.false_target_thresh = None
        self.spare1 = None
        self.transmit_lag_distance = None
        self.cpu_board_serial_number = None
        self.system_bandwidth = None
        self.system_power = None
        self.spare2 = None
        self.instrument_serial_number = None
        self.beam_angle = None

class _VariableLeader:
    formats = [
        ('VARIABLE LEADER ID',2,'<','H',True),
        ('ENSEMBLE NUMBER',2,'<','H',True),
        ('RTC YEAR {TS}',1,'<','B',True),
        ('RTC MONTH {TS}',1,'<','B',True),
        ('RTC DAY {TS}',1,'<','B',True),
        ('RTC HOUR {TS}',1,'<','B',True),
        ('RTC MINUTE {TS}',1,'<','B',True),
        ('RTC SECOND {TS}',1,'<','B',True),
        ('RTC HUNDREDTHS {TS}',1,'<','B',True),
        ('ENSEMBLE # MSB',1,'<','B',True),
        ('BIT RESULT',2,'<','H',True),
        ('SPEED OF SOUND {EC}',2,'<','H',True),
        ('DEPTH OF TRANSDUCER {ED}',2,'<','H',True),
        ('HEADING {EH}',2,'<','H',True),
        ('PITCH TILT 1 {EP}',2,'<','h',True),
        ('ROLL TILT 2 {ER}',2,'<','h',True),
        ('SALINITY {ES}',2,'<','H',True),
        ('TEMPERATURE {ET}',2,'<','h',True),
        ('MPT MINUTES',1,'<','B',True),
        ('MPT SECONDS',1,'<','B',True),
        ('MPT HUNDREDTHS',1,'<','B',True),
        ('HDG STD DEV',1,'<','B',True),
        ('PITCH STD DEV',1,'<','B',True),
        ('ROLL STD DEV',1,'<','B',True),
        ('ADC CHANNEL 0',1,'<','B',True),
        ('ADC CHANNEL 1',1,'<','B',True),
        ('ADC CHANNEL 2',1,'<','B',True),
        ('ADC CHANNEL 3',1,'<','B',True),
        ('ADC CHANNEL 4',1,'<','B',True),
        ('ADC CHANNEL 5',1,'<','B',True),
        ('ADC CHANNEL 6',1,'<','B',True),
        ('ADC CHANNEL 7',1,'<','B',True),
        ('ERROR STATUS WORD ESW {CY}',4,'<','I',True),
        ('SPARE1',2,'<','B',False),
        ('PRESSURE',4,'<','I',True),
        ('PRESSURE SENSOR VARIANCE',4,'<','I',True),
        ('SPARE2',1,'<','B',False),
        ('RTC CENTURY',1,'<','B',True),
        ('RTC YEAR',1,'<','B',True),
        ('RTC MONTH',1,'<','B',True),
        ('RTC DAY',1,'<','B',True),
        ('RTC HOUR',1,'<','B',True),
        ('RTC MINUTE',1,'<','B',True),
        ('RTC SECOND',1,'<','B',True),
        ('RTC HUNDREDTH',1,'<','B',True),
        ]
    
    def __init__(self):
        self.id = None
        self.ensemble_number = None
        self.rtc_year = None
        self.rtc_month = None
        self.rtc_day = None
        self.rtc_hour = None
        self.rtc_minute = None
        self.rtc_second = None
        self.rtc_hundredths = None
        self.ensemble_number_msb = None
        self.bit_result = None
        self.speed_of_sound = None
        self.depth_of_transducer = None
        self.heading = None
        self.pitch_tilt_1 = None
        self.roll_tilt_2 = None
        self.salinity = None
        self.temperature = None
        self.mpt_minutes = None
        self.mpt_seconds = None
        self.mpt_hundredths = None
        self.hdg_std_dev = None
        self.pitch_std_dev = None
        self.roll_std_dev = None
        self.adc_channel_0 = None
        self.adc_channel_1 = None
        self.adc_channel_2 = None
        self.adc_channel_3 = None
        self.adc_channel_4 = None
        self.adc_channel_5 = None
        self.adc_channel_6 = None
        self.adc_channel_7 = None
        self.error_status_word = None
        self.spare1 = None
        self.pressure = None
        self.pressure_sensor_variance = None
        self.spare2 = None
        self.rtc_century = None
        self.rtc_year = None
        self.rtc_month = None
        self.rtc_day = None
        self.rtc_hour = None
        self.rtc_minute = None
        self.rtc_second = None
        self.rtc_hundredth = None

    def get_datetime(self):
        """
        Get the datetime of the ensemble.
        Returns:
        -------
        datetime
            A datetime object representing the ensemble time.
        """
        century = str(self.rtc_century)
        if not century in ['19', '20']: century = '20'
        year = int(century + str(self.rtc_year))
        month = self.rtc_month
        day = self.rtc_day
        hour = self.rtc_hour
        minute = self.rtc_minute
        second = self.rtc_second
        hundredths = self.rtc_hundredth * 1000
        try:
            return datetime(year, month, day, hour, minute, second, hundredths)
        except ValueError:
            return None

class _BottomTrack:
    formats = [
        ('BOTTOM-TRACK ID',2,'<','H',True),
        ('BT PINGS PER ENSEMBLE {BP}',2,'<','H',True),
        ('BT DELAY BEFORE RE-ACQUIRE {BD}',2,'<','H',True),
        ('BT CORR MAG MIN {BC}',1,'<','B',True),
        ('BT EVAL AMP MIN {BA}',1,'<','B',True),
        ('BT PERCENT GOOD MIN {BG}',1,'<','B',True),
        ('BT MODE {BM}',1,'<','B',True),
        ('BT ERR VEL MAX {BE}',2,'<','H',True),
        ('Reserved',4,'<','H',True),
        ('BEAM#1 BT RANGE',2,'<','H',True),
        ('BEAM#2 BT RANGE',2,'<','H',True),
        ('BEAM#3 BT RANGE',2,'<','H',True),
        ('BEAM#4 BT RANGE',2,'<','H',True),
        ('BEAM#1 BT VEL',2,'<','H',True),
        ('BEAM#2 BT VEL',2,'<','H',True),
        ('BEAM#3 BT VEL',2,'<','H',True),
        ('BEAM#4 BT VEL',2,'<','H',True),
        ('BEAM#1 BT CORR.',1,'<','H',True),
        ('BEAM#2 BT CORR.',1,'<','H',True),
        ('BEAM#3 BT CORR.',1,'<','H',True),
        ('BEAM#4 BT CORR.',1,'<','H',True),
        ('BEAM#1 EVAL AMP',1,'<','H',True),
        ('BEAM#2 EVAL AMP',1,'<','H',True),
        ('BEAM#3 EVAL AMP',1,'<','H',True),
        ('BEAM#4 EVAL AMP',1,'<','H',True),
        ('BEAM#1 BT %GOOD',1,'<','H',True),
        ('BEAM#2 BT %GOOD',1,'<','H',True),
        ('BEAM#3 BT %GOOD',1,'<','H',True),
        ('BEAM#4 BT %GOOD',1,'<','H',True),
        ('REF LAYER MIN {BL}',2,'<','H',True),
        ('REF LAYER NEAR {BL}',2,'<','H',True),
        ('REF LAYER FAR {BL}',2,'<','H',True),
        ('BEAM#1 REF LAYER VEL',2,'<','H',True),
        ('BEAM #2 REF LAYER VEL',2,'<','H',True),
        ('BEAM #3 REF LAYER VEL',2,'<','H',True),
        ('BEAM #4 REF LAYER VEL',2,'<','H',True),
        ('BM#1 REF CORR',1,'<','H',True),
        ('BM#2 REF CORR',1,'<','H',True),
        ('BM#3 REF CORR',1,'<','H',True),
        ('BM#4 REF CORR',1,'<','H',True),
        ('BM#1 REF INT',1,'<','H',True),
        ('BM#2 REF INT',1,'<','H',True),
        ('BM#3 REF INT',1,'<','H',True),
        ('BM#4 REF INT',1,'<','H',True),
        ('BM#1 REF %GOOD',1,'<','H',True),
        ('BM#2 REF %GOOD',1,'<','H',True),
        ('BM#3 REF %GOOD',1,'<','H',True),
        ('BM#4 REF %GOOD',1,'<','H',True),
        ('BT MAX. DEPTH {BX}',2,'<','H',True),
        ('BM#1 RSSI AMP',1,'<','H',True),
        ('BM#2 RSSI AMP',1,'<','H',True),
        ('BM#3 RSSI AMP',1,'<','H',True),
        ('BM#4 RSSI AMP',1,'<','H',True),
        ('GAIN',1,'<','H',True),
        ('*SEE BYTE 17',1,'<','H',True),
        ('*SEE BYTE 19',1,'<','H',True),
        ('*SEE BYTE 21',1,'<','H',True),
        ('*SEE BYTE 23',1,'<','H',True),
        ('RESERVED',4,'<','H',True),
    ]

    def __init__(self):
        self.id = None
        self.bt_pings_per_ensemble = None
        self.bt_delay_before_re_acquire = None
        self.bt_corr_mag_min = None
        self.bt_eval_amp_min = None
        self.bt_percent_good_min = None
        self.bt_mode = None
        self.bt_err_vel_max = None
        self.reserved = None
        self.beam_range_1 = None
        self.beam_range_2 = None
        self.beam_range_3 = None
        self.beam_range_4 = None
        self.beam_vel_1 = None
        self.beam_vel_2 = None
        self.beam_vel_3 = None
        self.beam_vel_4 = None
        self.beam_corr_1 = None
        self.beam_corr_2 = None
        self.beam_corr_3 = None
        self.beam_corr_4 = None
        self.beam_eval_amp_1 = None
        self.beam_eval_amp_2 = None
        self.beam_eval_amp_3 = None
        self.beam_eval_amp_4 = None
        self.beam_percent_good_1 = None
        self.beam_percent_good_2 = None
        self.beam_percent_good_3 = None
        self.beam_percent_good_4 = None
        self.ref_layer_min = None
        self.ref_layer_near = None
        self.ref_layer_far = None
        self.beam_ref_layer_vel_1 = None
        self.beam_ref_layer_vel_2 = None
        self.beam_ref_layer_vel_3 = None
        self.beam_ref_layer_vel_4 = None
        self.beam_ref_corr_1 = None
        self.beam_ref_corr_2 = None
        self.beam_ref_corr_3 = None
        self.beam_ref_corr_4 = None
        self.beam_ref_int_1 = None
        self.beam_ref_int_2 = None
        self.beam_ref_int_3 = None
        self.beam_ref_int_4 = None
        self.beam_ref_percent_good_1 = None
        self.beam_ref_percent_good_2 = None
        self.beam_ref_percent_good_3 = None
        self.beam_ref_percent_good_4 = None
        self.bt_max_depth = None
        self.beam_rssi_amp_1 = None
        self.beam_rssi_amp_2 = None
        self.beam_rssi_amp_3 = None
        self.beam_rssi_amp_4 = None
        self.gain = None
        self.see_byte_17 = None
        self.see_byte_19 = None
        self.see_byte_21 = None
        self.see_byte_23 = None
        self.Reserverd = None

class _SystemConfiguration:
    _BEAM_FACING = {'0':'DOWN', '1':'UP'}    
    _XDCR_ATT = {'0':'NOT ATTACHED', '1':'ATTACHED'}
    _SENSOR_CFG = {'00':'#1', '01':'#2', '10':'#3'}
    _BEAM_PAT = {'0':'CONCAVE', '1':'CONVEX'}
    _SYS_FREQ = {
        '000':'75-kHz',
        '001':'150-kHz',
        '010':'300-kHz',
        '011':'600-kHz',
        '100':'1200-kHz',
        '101':'2400-kHz',
        }     
    _JANUS = {
        '0100':'4-BM',
        '0101': '5-BM (DEMOD)',
        '1111': '5-BM (2 DEMD)',
        }
    _BEAM_ANGLE = {
        '00': '15E',
        '01': '20E',
        '10': '30E',
        '11': 'OTHER'
        }
    def __init__(self, cfg) -> None:
        self.cfg = cfg
        LSB = self._get_bit_string(cfg[0])
        MSB = self._get_bit_string(cfg[1])
        self.beam_facing = self._BEAM_FACING[LSB[0]]
        self.xdcr_attached = self._XDCR_ATT[LSB[1]]
        self.sensor_cfg = self._SENSOR_CFG[LSB[2:4]]
        self.beam_pattern = self._BEAM_PAT[LSB[4]]
        self.frequency = self._SYS_FREQ[LSB[5:]]
        try:
            self.janus_config = self._JANUS[MSB[:4]]
        except KeyError:
            self.janus_config = 'UNKNOWN'
        self.beam_angle = self._BEAM_ANGLE[MSB[-2:]]


    @staticmethod
    def _get_bit_string(byte: int) -> str:
        """
        Convert a byte (0-255) to an 8-character binary string (MSB to LSB).

        Parameters:
        ----------
            byte (int): A single byte value (0-255).

        Returns:
        --------
            str: A binary string, e.g., "01011001"
        """
        return format(byte, "08b")

class PD0:
    def __init__(self, filename: str | Path) -> None:
        self.fname = Utils._validate_file_path(filename, Constants._PD0_SUFFIX)
        self._checksum = []
        self.metadata = Metadata(self.fname)
        fe, le = self.__get_first_and_last_ensemble()
        self.metadata.Init(fe=fe, le=le)

    def read_ensembles(self) -> list[Ensemble]:
        """
        Read all ensembles from the PD0 file.
        Returns:
        -------
        list[Ensemble]
            A list of Ensemble objects read from the file.
        """
        self._file = open(self.fname, "rb")
        ensembles = self._read_ensembles()
        self._file.close()
        return ensembles

    def _read_ensembles(self) -> list[Ensemble]:
        """
        Read ensembles from the PD0 file between start and end ensemble numbers.
        Parameters:
        ----------
        start : int
            The starting ensemble number to read from the file.
        end : int
            The ending ensemble number to read from the file.
        Returns:
        -------
        list[Ensemble]
            A list of Ensemble objects read from the file.
        """
        en = 0
        self._n_ensembles = 0
        ensembles = []
        while en <= self.metadata.n_ensemble_in_file:
            valid = False
            try:
                ensemble = self.__read_ensemble()
                valid = self.__check_valid_ensemble(ensemble)
            except:
                pass
            if valid:
                self._n_ensembles += 1
                ensembles.append(ensemble)
                en += 1
            else:
                if self.metadata.filesize - self._file.tell() < self.metadata.ensemble_size:
                    break
                else:
                    self._file.seek(self.__find_next_ensemble())
        if len(ensembles) == 0:
            warnings.warn(
                "No valid ensembles found in the specified range.",
                RuntimeWarning,
                stacklevel=2,
            )
        else:
            self.metadata.first_ensemble_read = ensembles[0].variable_leader.ensemble_number
            self.metadata.last_ensemble_read = ensembles[-1].variable_leader.ensemble_number
            self.n_ensembles = len(ensembles)
        return ensembles    

    def __read_next_bytes(self, fmt):
        decode = fmt[4]
        raw_bytes = self._file.read(fmt[1])
        self._checksum.append(raw_bytes)
        
        if fmt[1] > 1:
            if fmt[3] == 'B':
                fmtstr = f'{fmt[2]}{fmt[1]}{fmt[3]}' 
            elif fmt[3] in ['Q','I']:
                fmtstr = f'{fmt[2]}{fmt[3]}' 
            else:
                fmtstr = f'{fmt[2]}{int(fmt[1]/2)}{fmt[3]}'
            out = unpack(fmtstr,raw_bytes)
        else:
            out = raw_bytes
            
        if decode:    
            return out[0]
        else:
            return raw_bytes

    def __get_first_and_last_ensemble(self) -> tuple[Ensemble, Ensemble]:
        """
        Get the first and last ensembles from the PD0 file.
        Returns:
        -------
        tuple[Ensemble, Ensemble]
            A tuple containing the first and last Ensemble objects.
        """
        self._file = open(self.fname,"rb")
        self._file.seek(self.__find_next_ensemble())
        first_ensemble = self.__read_ensemble()
        self._file.seek(0, 2)  # Move to the end of the file
        self._file.seek(self.__find_next_ensemble(backward=True))
        last_ensemble = self.__read_ensemble()
        self._file.close()
        return first_ensemble, last_ensemble

    def __find_next_ensemble(self, length: int = 5000, max_iter: int = 100, offset: int = 0, backward: bool = False) -> int:
        """
        Find the next ensemble start position in the PD0 file.
        Parameters:
        ----------
        length : int
            The number of bytes to search for a valid ensemble in it.
        max_iter : int
            The maximum number of iterations to search for a valid ensemble.
        offset : int
            The offset in bytes from the current position to start searching.
        backward : bool
            If True, search for the previous ensemble instead of the next one.
        Returns:
        -------
        int
            The start position of the next ensemble in the file.
        """
        if backward:
            offset = -offset
            length = -length
        current_pos = self._file.tell()
        start_pos = max(current_pos, 0) + offset
        valid = False
        iter_count = 0
        while not valid and iter_count < max_iter:
            self._file.seek(start_pos)
            headers = [i for i in re.finditer(b'\x7f\x7f', self._file.read(length), re.S)]
            for header in headers:
                pos = header.start() + start_pos
                self._file.seek(pos)
                try:
                    ensemble = self.__read_ensemble()
                    valid = self.__check_valid_ensemble(ensemble)
                except:
                    valid = False
                if valid:
                    break
            conditions = [
                iter_count > max_iter,
                self._file.tell() >= self.metadata.filesize,
            ]
            if any(conditions):
                pos = self.metadata.filesize
                warnings.warn(
                    "Failed due to termination conditions",
                    RuntimeWarning,
                    stacklevel=2,
                )
                break
            if backward:
                start_pos = max(start_pos + length, 0)
            else:
                start_pos = start_pos + length - 1
            self._file.seek(start_pos)
            iter_count += 1

        self._file.seek(current_pos)
        return pos

    def __read_ensemble(self) -> Ensemble:
        """
        Read an ensemble from the current position in the PD0 file.
        Returns:
        -------
        Ensemble
            An Ensemble object containing the data read from the file.
        """
        start_pos = self._file.tell()
        self._checksum = []
        ensemble = Ensemble()
        ensemble.header = self.__read_ensemble_header()
        self._file.seek(start_pos + self._address_offsets[0])
        ensemble.fixed_leader = self.__read_fixed_leader()
        self._file.seek(start_pos + self._address_offsets[1])
        self.variable_header = self.__read_variable_leader()
        self._file.seek(start_pos + self._address_offsets[2])
        ensemble.header.velocity_id = self.__read_next_bytes(_EnsembleHeader.data_ID_code_format)
        # Read velocity data
        data = []
        for cell in range(ensemble.fixed_leader.number_of_cells):
            cell_data = []
            for beam in range(ensemble.fixed_leader.number_of_beams):
                cell_data.append(self.__read_next_bytes(ensemble.velocity_format))
            data.append(cell_data)
        ensemble.velocity = np.array(data)
        # Read correlation magnitude data
        ensemble.header.id_code_4 = self.__read_next_bytes(_EnsembleHeader.data_ID_code_format)
        data = []
        for cell in range(ensemble.fixed_leader.number_of_cells):
            cell_data = []
            for beam in range(ensemble.fixed_leader.number_of_beams):
                cell_data.append(self.__read_next_bytes(ensemble.coor_mag_format))
            data.append(cell_data)
        ensemble.correlation_magnitude = np.array(data)
        # Read echo intensity data
        ensemble.header.id_code_5 = self.__read_next_bytes(_EnsembleHeader.data_ID_code_format)
        data = []
        for cell in range(ensemble.fixed_leader.number_of_cells):
            cell_data = []
            for beam in range(ensemble.fixed_leader.number_of_beams):
                cell_data.append(self.__read_next_bytes(ensemble.echo_intensity_format))
            data.append(cell_data)
        ensemble.echo_intensity = np.array(data)
        # Read percent good data
        ensemble.header.id_code_6 = self.__read_next_bytes(_EnsembleHeader.data_ID_code_format)
        data = []
        for cell in range(ensemble.fixed_leader.number_of_cells):
            cell_data = []
            for beam in range(ensemble.fixed_leader.number_of_beams):
                cell_data.append(self.__read_next_bytes(ensemble.pct_good_format))
            data.append(cell_data)
        ensemble.percent_good = np.array(data)
        # Read bottom track data if available
        if ensemble.header.n_data_types == 7:
            ensemble.bottom_track = self.__read_bottom_track(self)
        else:
            ensemble.bottom_track = None
        
        ensemble.header.reserved_bit_data = self.__read_next_bytes(_EnsembleHeader.data_ID_code_format)
        file_checksum = unpack('<H', self._file.read(2))[0]
        try:
            ensemble.system_configuration = _SystemConfiguration(ensemble.fixed_leader.system_configuration)
        except:
            ensemble.system_configuration = None
        ensemble.coordinate_system = self.__parse_EX_command(ensemble.fixed_leader.coordinate_transform)

        return ensemble

    def __read_ensemble_header(self) -> _EnsembleHeader:
        """
        Read the ensemble header from the current position in the PD0 file.
        Returns:
        -------
        _EnsembleHeader
            An instance of _EnsembleHeader containing the header data.
        """
        header = _EnsembleHeader()
        values = []
        for field in header.formats:
            values.append(self.__read_next_bytes(field))
        header.id = values[0]
        header.data_source_id = values[1]
        header.n_bytes_in_ensemble = values[2]
        header.spare = values[3]
        header.n_data_types = values[4]
        header.n_data_types = max(header.n_data_types, 6)
        for i in range(header.n_data_types):
            header.address_offsets.append(self.__read_next_bytes(header.address_offsets_format))
        self._address_offsets = header.address_offsets

        return header
    
    def __read_fixed_leader(self) -> _FixedLeader:
        """
        Read the fixed leader from the current position in the PD0 file.
        Returns:
        -------
        _FixedLeader
            An instance of _FixedLeader containing the fixed leader data.
        """
        fixed_leader = _FixedLeader()
        values = []
        for field in fixed_leader.formats:
            values.append(self.__read_next_bytes(field))
        fixed_leader.id = values[0]
        fixed_leader.cpu_fw_ver = values[1]
        fixed_leader.cpu_fw_rev = values[2]
        fixed_leader.system_configuration = values[3]
        fixed_leader.real_sim_flag = values[4]
        fixed_leader.lag_length = values[5]
        fixed_leader.number_of_beams = values[6]
        fixed_leader.number_of_cells = values[7]
        fixed_leader.pings_per_ensemble = values[8]
        fixed_leader.depth_cell_length = values[9]
        fixed_leader.blank_after_transmit = values[10]
        fixed_leader.profiling_mode = values[11]
        fixed_leader.low_corr_thresh = values[12]
        fixed_leader.no_code_reps = values[13]
        fixed_leader.percent_good_minimum = values[14]
        fixed_leader.error_velocity_maximum = values[15]
        fixed_leader.tpp_minutes = values[16]
        fixed_leader.tpp_seconds = values[17]
        fixed_leader.tpp_hundredths = values[18]
        fixed_leader.coordinate_transform = values[19]
        fixed_leader.heading_alignment = values[20]
        fixed_leader.heading_bias = values[21]
        fixed_leader.sensor_source = values[22]
        fixed_leader.sensors_available = values[23]
        fixed_leader.bin_1_distance = values[24]
        fixed_leader.xmit_pulse_length_based_on = values[25]
        fixed_leader.starting_cell_wp_ref_layer_average = values[26]
        fixed_leader.false_target_thresh = values[27]
        fixed_leader.spare1 = values[28]
        fixed_leader.transmit_lag_distance = values[29]
        fixed_leader.cpu_board_serial_number = values[30]
        fixed_leader.system_bandwidth = values[31]
        fixed_leader.system_power = values[32]
        fixed_leader.spare2 = values[33]
        fixed_leader.instrument_serial_number = values[34]
        fixed_leader.beam_angle = values[35]
        return fixed_leader
            
    def __read_variable_leader(self) -> _VariableLeader:
        """
        Read the variable leader from the current position in the PD0 file.
        Returns:
        -------
        _VariableLeader
            An instance of _VariableLeader containing the variable leader data.
        """
        variable_leader = _VariableLeader()
        values = []
        for field in variable_leader.formats:
            values.append(self.__read_next_bytes(field))
        variable_leader.id = values[0]
        variable_leader.ensemble_number = values[1]
        variable_leader.rtc_year = values[2]
        variable_leader.rtc_month = values[3]
        variable_leader.rtc_day = values[4]
        variable_leader.rtc_hour = values[5]
        variable_leader.rtc_minute = values[6]
        variable_leader.rtc_second = values[7]
        variable_leader.rtc_hundredths = values[8]
        variable_leader.ensemble_number_msb = values[9]
        variable_leader.bit_result = values[10]
        variable_leader.speed_of_sound = values[11]
        variable_leader.depth_of_transducer = values[12]
        variable_leader.heading = values[13]
        variable_leader.pitch_tilt_1 = values[14]
        variable_leader.roll_tilt_2 = values[15]
        variable_leader.salinity = values[16]
        variable_leader.temperature = values[17]
        variable_leader.mpt_minutes = values[18]
        variable_leader.mpt_seconds = values[19]
        variable_leader.mpt_hundredths = values[20]
        variable_leader.hdg_std_dev = values[21]
        variable_leader.pitch_std_dev = values[22]
        variable_leader.roll_std_dev = values[23]
        variable_leader.adc_channel_0 = values[24]
        variable_leader.adc_channel_1 = values[25]
        variable_leader.adc_channel_2 = values[26]
        variable_leader.adc_channel_3 = values[27]
        variable_leader.adc_channel_4 = values[28]
        variable_leader.adc_channel_5 = values[29]
        variable_leader.adc_channel_6 = values[30]
        variable_leader.adc_channel_7 = values[31]
        variable_leader.error_status_word = values[32]
        variable_leader.spare1 = values[33]
        variable_leader.pressure = values[34]
        variable_leader.pressure_sensor_variance = values[35]
        variable_leader.spare2 = values[36]
        variable_leader.rtc_century = values[37]
        variable_leader.rtc_year = values[38]
        variable_leader.rtc_month = values[39]
        variable_leader.rtc_day = values[40]
        variable_leader.rtc_hour = values[41]
        variable_leader.rtc_minute = values[42]
        variable_leader.rtc_second = values[43]
        variable_leader.rtc_hundredth = values[44]

        variable_leader.ensemble_number += variable_leader.ensemble_number_msb * 65535

        return variable_leader
    
    def __read_bottom_track(self) -> _BottomTrack:
        """
        Read the bottom track data from the current position in the PD0 file.
        Returns:
        -------
        _BottomTrack
            An instance of _BottomTrack containing the bottom track data.
        """
        bottom_track = _BottomTrack()
        values = []
        for field in bottom_track.formats:
            values.append(self.__read_next_bytes(field))
        bottom_track.id = values[0]
        bottom_track.bt_pings_per_ensemble = values[1]
        bottom_track.bt_delay_before_re_acquire = values[2]
        bottom_track.bt_corr_mag_min = values[3]
        bottom_track.bt_eval_amp_min = values[4]
        bottom_track.bt_percent_good_min = values[5]
        bottom_track.bt_mode = values[6]
        bottom_track.bt_err_vel_max = values[7]
        bottom_track.reserved = values[8]
        bottom_track.beam_range_1 = values[9]
        bottom_track.beam_range_2 = values[10]
        bottom_track.beam_range_3 = values[11]
        bottom_track.beam_range_4 = values[12]
        bottom_track.beam_vel_1 = values[13]
        bottom_track.beam_vel_2 = values[14]
        bottom_track.beam_vel_3 = values[15]
        bottom_track.beam_vel_4 = values[16]
        bottom_track.beam_corr_1 = values[17]
        bottom_track.beam_corr_2 = values[18]
        bottom_track.beam_corr_3 = values[19]
        bottom_track.beam_corr_4 = values[20]
        bottom_track.beam_eval_amp_1 = values[21]
        bottom_track.beam_eval_amp_2 = values[22]
        bottom_track.beam_eval_amp_3 = values[23]
        bottom_track.beam_eval_amp_4 = values[24]
        bottom_track.beam_percent_good_1 = values[25]
        bottom_track.beam_percent_good_2 = values[26]
        bottom_track.beam_percent_good_3 = values[27]
        bottom_track.beam_percent_good_4 = values[28]
        bottom_track.ref_layer_min = values[29]
        bottom_track.ref_layer_near = values[30]
        bottom_track.ref_layer_far = values[31]
        bottom_track.beam_ref_layer_vel_1 = values[32]
        bottom_track.beam_ref_layer_vel_2 = values[33]
        bottom_track.beam_ref_layer_vel_3 = values[34]
        bottom_track.beam_ref_layer_vel_4 = values[35]
        bottom_track.beam_ref_corr_1 = values[36]
        bottom_track.beam_ref_corr_2 = values[37]
        bottom_track.beam_ref_corr_3 = values[38]
        bottom_track.beam_ref_corr_4 = values[39]
        bottom_track.beam_ref_int_1 = values[40]
        bottom_track.beam_ref_int_2 = values[41]
        bottom_track.beam_ref_int_3 = values[42]
        bottom_track.beam_ref_int_4 = values[43]
        bottom_track.beam_ref_percent_good_1 = values[44]
        bottom_track.beam_ref_percent_good_2 = values[45]
        bottom_track.beam_ref_percent_good_3 = values[46]
        bottom_track.beam_ref_percent_good_4 = values[47]
        bottom_track.bt_max_depth = values[48]
        bottom_track.beam_rssi_amp_1 = values[49]
        bottom_track.beam_rssi_amp_2 = values[50]
        bottom_track.beam_rssi_amp_3 = values[51]
        bottom_track.beam_rssi_amp_4 = values[52]
        bottom_track.gain = values[53]
        bottom_track.see_byte_17 = values[54]
        bottom_track.see_byte_19 = values[55]
        bottom_track.see_byte_21 = values[56]
        bottom_track.see_byte_23 = values[57]
        bottom_track.Reserverd = values[58]
        return bottom_track
    
    def __parse_EX_command(self, value: bytes) -> str:
        """
        Parse the EX command value to a string.
        Parameters:
        ----------
        value : bytes
            The EX command value to parse.
        Returns:
        -------
        str
            The parsed EX command as a string.
        """
        LSB = _SystemConfiguration._get_bit_string(value)
        coord_sys = {
            '00': 'BEAM COORDINATES',
            '01': 'INSTRUMENT COORDINATES',
            '10': 'SHIP COORDINATES',
            '11': 'EARTH COORDINATES'
            }
        return coord_sys[LSB[3:5]]
    
    def __check_valid_ensemble(self, ensemble: Ensemble) -> bool:
        """
        Check if the ensemble is valid.
        Parameters:
        ----------
        ensemble : Ensemble
            The ensemble to check.
        Returns:
        -------
        bool
            True if the ensemble is valid, False otherwise.
        """
        if ensemble.header.n_data_types > 10: return False
        if ensemble.header.n_data_types < 1: return False
        if ensemble.header.id != 127: return False
        if ensemble.header.data_source_id != 127: return False
        if ensemble.variable_leader.ensemble_number == 0: return False
        if not any(ensemble.correlation_magnitude): return False
        if ensemble.variable_leader.get_datetime() is None: return False
        return True



