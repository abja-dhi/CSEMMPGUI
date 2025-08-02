import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from datetime import datetime

from .project import Project
from .survey import Survey
from .model import Model
from .adcp import ADCP
from .pd0 import Pd0Decoder
from .utils import Utils



def GenerateOutputXML(xml):
    result = ET.Element("Result")
    for key, value in xml.items():
        ET.SubElement(result, key).text = str(value)
    return ET.tostring(result, encoding='unicode')

def LoadPd0(filepath):
    pd0 = Pd0Decoder(filepath, cfg={})
    pd0.close()
    n_beams = pd0._n_beams
    n_ensembles = pd0._n_ensembles
    return {"NBeams": n_beams, "NEnsembles": n_ensembles}

def Extern2CSVSingle(filepath):
    result = Utils.extern_to_csv_single(filepath)
    return {"Result": result} # 1: already converted, 0: success, -1: failed
    
def Extern2CSVBatch(folderpath):
    result = Utils.extern_to_csv_batch(folderpath)
    n_success = result[0]
    n_failed = result[1]
    n_already_converted = result[2]
    return {"NSuccess": n_success, "NFailed": n_failed, "NAlreadyConverted": n_already_converted}

def GetColumnsFromCSV(filepath, header=0, sep=','):
    try:
        df = pd.read_csv(filepath, header=header, sep=sep)
        columns = df.columns.tolist()
        output = {"NColumns": len(columns)}
        for i, col in enumerate(columns):
            output[f"Column{i}"] = col
        return output
    except:
        return {"NColumns": 0}


def InstrumentSummaryADCP(filepath, task):
    """
    Generate a formatted summary report of ADCP instrument configuration and timing.

    Parameters
    ----------
    filepath : str
        Full path to the PD0 binary data file.

    Returns
    -------
    str
        Formatted plain-text summary of key ADCP parameters including timing,
        beam configuration, resolution, hardware metadata, and quality control settings.
    """
    
    # Load file
    part1 = ""
    part2 = ""
    part3 = ""
    pd0 = Pd0Decoder(filepath, cfg={})
    
    # Extract summary metadata
    fixed_leader = pd0._fixed
    #datetimes = [datetime(2000, 1, 1, 0, 0, 0), datetime(2001, 1, 1, 0, 0, 0)]
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
            'First Ensemble DateTime (UTC)': str(datetimes[0]),#.strftime("%Y-%b-%d %HH:%MM:%SS"),
            'Last Ensemble DateTime (UTC)': str(datetimes[-1]),#.strftime("%Y-%b-%d %HH:%MM:%SS"),
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

    # Format dictionary into report
    
    return {"Config": report}


def TestTask(xml):
    test = 'I will outline tasks to be implemented here'

    return {'Test':test}


def model_NTU_to_SSC(xml):
    "Use multiple OBS depth profiles and sets of water samples to estimate parameters for NTU to SSC relationship taking the linear form SSC = A * NTU + B"

    ## block where xml is parsed and data is extracted
    obs_profile_fpaths = xml.get('ObsProfiles', [])# list of OBS profile files, each file contains a single depth profile
    water_sample_fpaths = xml.get('WaterSamples', []) # only full sets of water samples are allowed

    ## load data from OBS profiles and water samples


    ## block where water samples are matched to neareset datapoint in OBS profiles 

    ## regression step 

    A,B = temp_regression(x,y)
    
    #calculate error statistics 
    residuals = y - (A * x + B) 
    mse = (residuals ** 2).mean()
    rmse = mse ** 0.5
    ssr = (residuals ** 2).sum()/ len(residuals)
    return {'A': A, 'B': B, 'RMSE': rmse, 'MSE': mse, 'SSR' : ssr}



def model_Bks_to_SSC(xml):
    'use multiple ADCP transects and water samples to estimate parameters for Bks to SSC relationship taking the LOG-linear form LOG10(SSC) = A * Bks + B'

    ## block where xml is parsed and data is extracted
    pd0_fpaths = xml.get('ADCP_Pd0_fpaths', [])  # list of ADCP transect files, each file contains a single transect
    position_Data_fpaths = xml.get('ADCP_Position_fpaths', [])  # list of position data files, each file contains a single position data corresponding to an ADCP transet. Must match order of ADCP fpaths. 
    adcp_cfg_params = xml.get('ADCP_cfgs', {})  # configuration parameters for ADCP processing, one for each input ADCP transect


    water_sample_fpaths = xml.get('WaterSample_fpaths', []) # only full sets of water samples are allowed

    ## load data from ADCP transects and water samples

    adcps = []
    for fpath in pd0_fpaths:
        adcp = ADCP(pd0, position_Data_fpaths, cfg=adcp_cfg_params)
        # Process each pd0 file as needed
        adcps.append(adcp)


    # laod water sample data 

    # construct point value pairs, matching water samples to the nearest point in the transect

    #regression step
        ## regression step 

    A,B = temp_regression(x,y)
    
    #calculate error statistics 
    residuals = y - (A * x + B) 
    mse = (residuals ** 2).mean()
    rmse = mse ** 0.5
    ssr = (residuals ** 2).sum()/ len(residuals)
    return {'A': A, 'B': B, 'RMSE': rmse, 'MSE': mse,'SSR' : ssr}



def plan_view_map(xml):
    'Function to make a map plot of the locations of ADCP transects'
    ## block where xml is parsed and data is extracted
    pd0_fpaths = xml.get('ADCP_Pd0_fpaths', [])  # list of ADCP transect files, each file contains a single transect
    pd0_position_Data_fpaths = xml.get('ADCP_Position_fpaths', [])  # list of position data files, each file contains a single position data corresponding to an ADCP transet. Must match order of ADCP fpaths. 
    adcp_cfg_params = xml.get('ADCP_cfgs', {})  # configuration parameters for ADCP processing, one for each input ADCP transect
    cmap = xml.get('cmap', 'viridis')  # colormap for the plot

    obs_profile_fpaths = xml.get('ObsProfiles', [])# list of OBS profile files, each file contains a single depth profile


    water_sample_fpaths = xml.get('WaterSamples', []) # only full sets of water samples are allowed

    ## load data from ADCP transects and associate position data

    ## load data from OBS transects and water samples
    
    ## use ADCP position data to determine location of all OBS transects by matching to nearest timestamp 

    return fig, ax 



def ADCP_floodplot(xml):

    ' create a four beam floodplot for a single Pd0 file'


    pd0_fpaths = xml.get('ADCP_Pd0_fpaths', [])  # list of ADCP transect files, each file contains a single transect
    pd0_position_Data_fpaths = xml.get('ADCP_Position_fpaths', [])  # list of position data files, each file contains a single position data corresponding to an ADCP transet. Must match order of ADCP fpaths. 
    adcp_cfg_params = xml.get('ADCP_cfgs', {})  # configuration parameters for ADCP processing, one for each input ADCP transect


    plot_params = xml.get('Plot_params',{}) # configuration parameters for the plot
    
    field = plot_params.field 
    plot_by = plot_params.plot_by
    cmap = plot_params.cmap

    depth_adjusted = plot_params.depth_adjusted # If true, generated a four beam mesh plot with depth or HAB as y-axis, if false then generic floodplot with bin number, distance from transducer, depth or HAB as options

    # plotting code

    if depth_adjusted:
        fig, ax = adcp.four_beam_floodplot(plot_params)
    else:
        fig, ax = adcp.four_beam_meshplot(plot_params)



    return fig,ax 



