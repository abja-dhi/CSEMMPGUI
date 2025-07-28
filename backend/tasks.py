from .project import Project
from .survey import Survey
from .model import Model
from .adcp import ADCP
from .pd0 import Pd0Decoder


def GenerateOutputXML(xml):
    result = ET.Element("Result")
    for key, value in xml.items():
        ET.SubElement(result, key).text = str(value)

def LoadPd0(filepath):
    pd0 = Pd0Decoder(filepath, cfg={})
    n_beams = pd0._n_beams
    n_ensembles = pd0._n_ensembles
    return {"NBeams": n_beams, "NEnsembles": n_ensembles}


def TestTask(xml):
    test = 'I will outline tasks to be implemented here'

    return {'Test':test}


def model_NTU_to_SSC(xml):
    'Use multiple OBS depth profiles and sets of water samples to estimate parameters for NTU to SSC relationship taking the linear form SSC = A * NTU + B"

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
    return {'A': A, 'B': B, 'RMSE': rmse, 'MSE': mse,'SSR' = ssr}}



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
    return {'A': A, 'B': B, 'RMSE': rmse, 'MSE': mse,'SSR' = ssr}}



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

    return fig,ax 



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
        fig,ax = adcp.four_beam_floodplot(plot_params)
    else:
        fig,ax = adcp.four_beam_meshplot(plot_params)



    return fig,ax 






    


    
    






