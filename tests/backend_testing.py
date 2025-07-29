
import sys
import os

# Add the project root (one level up from /tests/) to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import backend
from backend.pd0 import Pd0Decoder


    
if __name__ == "__main__":

    pd0_fpath = r'\\SGSIN1-STOR\Projects\61801596\Working Documents\Data and Calculations\10_Field Survey\Sediment Flux\2022\10. Oct\20221003-TF(F)-Exp2\RawDataRT\20221003-TF(F)-001r.000'
    
    
    
    cfg = {
    "progress_bar": "True",
    "instrument_depth": 12.5,          # meters
    "instrument_HAB": 2.0,             # height above bed, meters
    "name": "ADCP_20221003_TF(F)",
    "noise_floor": 39,
    "absolute_backscatter_C": -149.14,
    "absolute_backscatter_alpha": 0.178,
    "absolute_backscatter_P_dbw": 9,
    "rssi_beam_1": 0.3931,
    "rssi_beam_2": 0.4145,
    "rssi_beam_3": 0.4160,
    "rssi_beam_4": 0.4129,
    }
    
    
    import numpy as np
    pd0 = Pd0Decoder(pd0_fpath, cfg = cfg)

    fixed_leader = pd0._get_fixed_leader()[0]#.to_dict()

    datetimes = pd0._get_datetimes()
    dt_diffs = np.diff(datetimes)
    duration = datetimes[-1] - datetimes[0]
    total_seconds = int(duration.total_seconds())
    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    
    out = {
        "Ensemble Timing and General Metadata": {
            'Number of Ensembles': pd0._n_ensembles,
            'First Ensemble DateTime (UTC)': datetimes[0],
            'Last Ensemble DateTime (UTC)': datetimes[-1],
            'Duration (d:h:m:s)': f"{days}:{hours:02}:{minutes:02}:{seconds:02}",
            'Mean Ensemble Duration (s)': round(np.nanmean(dt_diffs).total_seconds(), 3),
            'Median Ensemble Duration (s)': round(np.nanmedian(dt_diffs).total_seconds(), 3),
            'Minimum Ensemble Duration (s)': round(np.nanmin(dt_diffs).total_seconds(), 3),
            'Maximum Ensemble Duration (s)': round(np.nanmax(dt_diffs).total_seconds(), 3),
        },
    
    
        "Beam Configuration and System Geometry": {
            'Beam Facing': fixed_leader.system_configuration.beam_facing,
            'Beam Pattern': fixed_leader.system_configuration.beam_pattern,
            'Beam Angle (°)': fixed_leader.system_configuration.beam_angle,
            'Beam Angle (Redundant °)': fixed_leader.beam_angle,
            'Janus Config': fixed_leader.system_configuration.janus_config,
            'Frequency': fixed_leader.system_configuration.frequency,
        },
    
        "Measurement Configuration and Resolution": {
            'Number of Beams': fixed_leader.number_of_beams,
            'Number of Cells': fixed_leader.number_of_cells_wn,
            'Pings per Ensemble': fixed_leader.pings_per_ensemble_wp,
            'Cell Size (cm)': fixed_leader.depth_cell_length_ws,
            'Blank After Transmit (cm)': fixed_leader.blank_after_transmit_wf,
            'Bin 1 Distance (cm)': fixed_leader.bin_1_distance,
            'Lag Length': fixed_leader.lag_length,
            'Transmit Lag Distance (cm)': fixed_leader.transmit_lag_distance,
            'Transmit Pulse Length Based on Water Track': fixed_leader.xmit_pulse_length_based_on_wt,
            'Ref Layer Start/End Cell': fixed_leader.starting_cell_wp_ref_layer_average_wl_ending_cell,
        },
    
        "Timing Parameters": {
            'TPP Minutes': fixed_leader.tpp_minutes,
            'TPP Seconds': fixed_leader.tpp_seconds,
            'TPP Hundredths': fixed_leader.tpp_hundredths_tp,
        },
    
        "Quality Control and Filtering Thresholds": {
            'Low Correlation Threshold': fixed_leader.low_corr_thresh_wc,
            'Number of Code Repetitions': fixed_leader.no_code_reps,
            'Minimum Good Data (%)': fixed_leader.gd_minimum_wg,
            'Max Error Velocity Threshold (mm/s)': fixed_leader.error_velocity_maximum_we,
            'False Target Threshold (dB)': fixed_leader.false_target_thresh_wa,
        },
    
        "Coordinate Transforms and Orientation": {
            'Coordinate Transform Flags': fixed_leader.coordinate_transform_ex,
            'Heading Alignment (°)': fixed_leader.heading_alignment_ea,
            'Heading Bias (°)': fixed_leader.heading_bias_eb,
        },
    
        "Sensor and Source Configuration": {
            'Sensor Source Flags': fixed_leader.sensor_source_ez,
            'Sensors Available Flags': fixed_leader.sensors_available,
        },
    
        "Firmware and Hardware Metadata": {
            'CPU Firmware Version': fixed_leader.cpu_fw_ver,
            'CPU Firmware Revision': fixed_leader.cpu_fw_rev,
            'CPU Board Serial Number': fixed_leader.cpu_board_serial_number,
            'Instrument Serial Number': fixed_leader.instrument_serial_number,
            'System Bandwidth (kHz)': fixed_leader.system_bandwidth_wb,
            'System Power (W)': fixed_leader.system_power_cq,
        },
    
        "Flags and Placeholders": {
            'Realsim Flag': fixed_leader.realsim_flag,
            'Spare1': fixed_leader.spare1,
            'Spare2': fixed_leader.spare2,
        }
    }

    lines = []
    for section, items in out.items():
        lines.append(section.upper())
        lines.append("=" * len(section))
    
        max_key_len = max(len(key) for key in items)
        for key, value in items.items():
            padding = " " * 2
            key_str = key.ljust(max_key_len + 4)
            lines.append(f"{padding}{key_str}: {value}")
    
        lines.append("")  # Blank line between sections
    
    report = "\n".join(lines)
 
    # with open("adcp_summary.txt", "w", encoding="utf-8") as f:
    #     f.write(report)
    
