# from tasks import CreateADCPDict

import xml.etree.ElementTree as ET
from pathlib import Path
class Constants:
    """Global constants for the pyEMMP package."""
    _CFG_SUFFIX = ".cfg"
    _PD0_SUFFIX = [".pd0", ".000"]
    _TABLE_SUFFIX = [".csv", ".xlsx"]
    _SSC_PAR_SUFFIX = ".sscpar"
    _VALID_ENSEMBLE_NAMES = ('ECHO INTENSITY', 'PERCENT GOOD', 'CORRELATION MAGNITUDE', 'SIGNAL TO NOISE RATIO', 'ABSOLUTE BACKSCATTER')
    _ENSEMBLE_COUNT_THRESHOLD = 65536
    _DFSU_SUFFIX = [".dfsu"]
    _DFS0_SUFFIX = [".dfs0"]
    _LOW_NUMBER = -9.0e99
    _HIGH_NUMBER = 9.0e99
    _FAR_PAST_DATETIME = "1950-01-01T00:00:00"
    _FAR_FUTURE_DATETIME = "2100-01-01T00:00:00"

inst = r"""
<VesselMountedADCP id="2" type="VesselMountedADCP" name="New Vessel Mounted ADCP 1">
      <Pd0>
        <Path>C:\Users\abja\OneDrive - DHI\61803553-05 EMMP Support Group\github\CSEMMPGUI\tests\20241002_F3(E)\RawDataPP\20241002_F3(E)_002r.000</Path>
        <SSCModel>
        </SSCModel>
        <Configuration>
          <MagneticDeclination>0.0</MagneticDeclination>
          <UTCOffset>0.0</UTCOffset>
          <RotationAngle>0.0</RotationAngle>
          <CRPOffset>
            <X>0.0</X>
            <Y>0.0</Y>
            <Z>0.0</Z>
          </CRPOffset>
          <RSSICoefficients>
            <Beam1>0.41</Beam1>
            <Beam2>0.41</Beam2>
            <Beam3>0.41</Beam3>
            <Beam4>0.41</Beam4>
          </RSSICoefficients>
          <TransectShift>
            <X>0.0</X>
            <Y>0.0</Y>
            <Z>0.0</Z>
            <T>0.0</T>
          </TransectShift>
          <C>-139.0</C>
          <Pdbw>9</Pdbw>
          <Er>39</Er>
        </Configuration>
        <Masking>
          <FirstEnsemble Enabled="false">1</FirstEnsemble>
          <LastEnsemble Enabled="false">9999</LastEnsemble>
          <StartDatetime Enabled="false">
          </StartDatetime>
          <EndDatetime Enabled="false">
          </EndDatetime>
          <MaskEchoIntensity Enabled="false">
            <Min>0</Min>
            <Max>255</Max>
          </MaskEchoIntensity>
          <MaskPercentGood Enabled="false">
            <Min>90</Min>
          </MaskPercentGood>
          <MaskCorrelationMagnitude Enabled="false">
            <Min>0</Min>
            <Max>255</Max>
          </MaskCorrelationMagnitude>
          <MaskCurrentSpeed Enabled="false">
            <Min>-2</Min>
            <Max>2</Max>
          </MaskCurrentSpeed>
          <MaskErrorVelocity Enabled="false">
            <Min>
            </Min>
            <Max>
            </Max>
          </MaskErrorVelocity>
          <MaskAbsoluteBackscatter Enabled="false">
            <Min>-100</Min>
            <Max>0</Max>
          </MaskAbsoluteBackscatter>
        </Masking>
      </Pd0>
      <PositionData>
        <Path>C:\Users\abja\OneDrive - DHI\61803553-05 EMMP Support Group\github\CSEMMPGUI\tests\20241002_F3(E)\RawDataPP\20241002_F3(E)_002extern.csv</Path>
        <Columns>
          <Column0>DateTime</Column0>
          <Column1>Ensemble</Column1>
          <Column2>Latitude</Column2>
          <Column3>Longitude</Column3>
          <Column4>Speed</Column4>
          <Column5>Course</Column5>
          <Column6>PosFix</Column6>
          <Column7>EastVesselDisplacement</Column7>
          <Column8>NorthVesselDisplacement</Column8>
        </Columns>
        <DateTimeColumn>DateTime</DateTimeColumn>
        <XColumn>Longitude</XColumn>
        <YColumn>Latitude</YColumn>
        <HeadingColumn>Course</HeadingColumn>
        <Pitch>0.0</Pitch>
        <Roll>0.0</Roll>
      </PositionData>
    </VesselMountedADCP>
"""
instrument = ET.fromstring(inst)
epsg = "4326"
waterProp = """<Water Density="1023" Salinity="32" Temperature="" pH="8.1" />"""
sedimentProp = """<Sediment Diameter="0.00025" Density="2650" />"""

water = ET.fromstring(waterProp)
sediment = ET.fromstring(sedimentProp)

def CreateADCPDict(instrument: ET.Element, water: ET.Element, sediment: ET.Element, epsg: str):
    pd0 = instrument.find("Pd0")
    configuration = pd0.find("Configuration")
    crp_offset = configuration.find("CRPOffset")
    rssis = configuration.find("RSSICoefficients")
    transect_shift = configuration.find("TransectShift")
    masking = pd0.find("Masking")
    maskEchoIntensity = masking.find("MaskEchoIntensity")
    maskPercentGood = masking.find("MaskPercentGood")
    maskCorrelationMagnitude = masking.find("MaskCorrelationMagnitude")
    maskCurrentSpeed = masking.find("MaskCurrentSpeed")
    maskErrorVelocity = masking.find("MaskErrorVelocity")
    maskAbsoluteBackscatter = masking.find("MaskAbsoluteBackscatter")
    position = instrument.find("PositionData")
    columns = position.find("Columns")

    filename = pd0.find("Path").text
    name = instrument.attrib.get("name", Path(filename).stem)
    if maskPercentGood.attrib["Enabled"] == "true":
        pg_min = float(get_value(maskPercentGood, "Min", 0))
    else:
        pg_min = 0
    if maskCurrentSpeed.attrib["Enabled"] == "true":
        vel_min = float(get_value(maskCurrentSpeed, "Min", Constants._LOW_NUMBER))
        vel_max = float(get_value(maskCurrentSpeed, "Max", Constants._HIGH_NUMBER))
    else:
        vel_min = Constants._LOW_NUMBER
        vel_max = Constants._HIGH_NUMBER
    if maskEchoIntensity.attrib["Enabled"] == "true":
        echo_min = float(get_value(maskEchoIntensity, "Min", 0))
        echo_max = float(get_value(maskEchoIntensity, "Max", 255))
    else:
        echo_min = 0
        echo_max = 255
    if maskCorrelationMagnitude.attrib["Enabled"] == "true":
        cormag_min = get_value(maskCorrelationMagnitude, "Min", None)
        cormag_min = float(cormag_min) if cormag_min is not None else None
        cormag_max = get_value(maskCorrelationMagnitude, "Max", None)
        cormag_max = float(cormag_max) if cormag_max is not None else None
    else:
        cormag_min = None
        cormag_max = None
    if maskAbsoluteBackscatter.attrib["Enabled"] == "true":
        absback_min = float(get_value(maskAbsoluteBackscatter, "Min", 0))
        absback_max = float(get_value(maskAbsoluteBackscatter, "Max", 255))
    else:
        absback_min = 0
        absback_max = 255
    if maskErrorVelocity.attrib["Enabled"] == "true":
        err_vel_max = get_value(maskErrorVelocity, "Max", "auto")
        if err_vel_max != "auto":
            err_vel_max = float(err_vel_max)
    else:
        err_vel_max = "auto"
    # velocity_average_window_len = get_value(masking, "VelocityAverageWindowLen", 0)
    start_datetime = get_value(masking, "StartDateTime", None)
    end_datetime = get_value(masking, "EndDateTime", None)
    first_good_ensemble = get_value(masking, "FirstEnsemble", None)
    first_good_ensemble = int(first_good_ensemble) if first_good_ensemble is not None else None
    last_good_ensemble = get_value(masking, "LastEnsemble", None)
    last_good_ensemble = int(last_good_ensemble) if last_good_ensemble is not None else None
    magnetic_declination = float(get_value(configuration, "MagneticDeclination", 0))
    utc_offset = get_value(configuration, "UTCOffset", None)
    utc_offset = float(utc_offset) if utc_offset is not None else None
    # beam_dr = float(get_value(configuration, "beam_dr", 0.1))
    # bt_bin_offset = int(get_value(configuration, "BTBinOffset", 1))
    crp_rotation_angle = float(get_value(configuration, "RotationAngle", 0.0))
    crp_offset_x = float(get_value(crp_offset, "X", 0))
    crp_offset_y = float(get_value(crp_offset, "Y", 0))
    crp_offset_z = float(get_value(crp_offset, "Z", 0))
    transect_shift_x = float(get_value(transect_shift, "X", 0))
    transect_shift_y = float(get_value(transect_shift, "Y", 0))
    transect_shift_z = float(get_value(transect_shift, "Z", 0))
    transect_shift_t = float(get_value(transect_shift, "T", 0))

    position_fname = get_value(position, "Path", "")
    X_mode = "Variable"
    Y_mode = "Variable"
    Depth_mode = "Constant"
    Pitch_mode = "Constant"
    Roll_mode = "Constant"
    Heading_mode = "Variable"
    DateTime_mode = "Variable"
    X_value = get_value(position, "XColumn", "Longitude")
    Y_value = get_value(position, "YColumn", "Latitude")
    Depth_value = 0
    Pitch_value = 0
    Roll_value = 0
    Heading_value = get_value(position, "HeadingColumn", "Course")
    DateTime_value = get_value(position, "DateTimeColumn", "DateTime")
    header = int(get_value(position, "Header", 0))
    sep = get_value(position, "Sep", ",")

    pos_cfg = {
        'filename': position_fname,
        'epsg': epsg,
        'X_mode': X_mode,
        'Y_mode': Y_mode,
        'Depth_mode': Depth_mode,
        'Pitch_mode': Pitch_mode,
        'Roll_mode': Roll_mode,
        'Heading_mode': Heading_mode,
        'DateTime_mode': DateTime_mode,
        'X_value': X_value,
        'Y_value': Y_value,
        'Depth_value': Depth_value,
        'Pitch_value': Pitch_value,
        'Roll_value': Roll_value,
        'Heading_value': Heading_value,
        'DateTime_value': DateTime_value,
        'header': header,
        'sep': sep,
        }
    
    water_density = float(water.attrib.get("Density", "1023"))
    salinity = float(water.attrib.get("Salinity", "32"))
    temperature = water.attrib.get("Temperature", None)
    print(temperature)
    if temperature is not None and temperature.strip() != "":
        temperature = float(temperature)
    pH = float(water.attrib.get("pH", "8.1"))
    water_properties = {
        'density' : water_density,
        'salinity' : salinity,
        'temperature' : temperature,
        'pH' : pH
        }

    sediment_density = float(sediment.attrib.get("Density", "2650"))
    diameter = float(sediment.attrib.get("Diameter", "2.5e-4"))
    sediment_properties = {
        'particle_density': sediment_density,
        'particle_diameter': diameter
    }

    C = float(get_value(configuration, "C", -139.0))
    P_dbw = float(get_value(configuration, "Pdbw", 9))
    E_r = float(get_value(rssis, "Er", 39))
    rssi_beam1 = float(get_value(rssis, "Beam1", 0.41))
    rssi_beam2 = float(get_value(rssis, "Beam2", 0.41))
    rssi_beam3 = float(get_value(rssis, "Beam3", 0.41))
    rssi_beam4 = float(get_value(rssis, "Beam4", 0.41))

    abs_params = {'C': C,
              'P_dbw': P_dbw,
              'E_r': E_r,
              'rssi_beam1': rssi_beam1,
              'rssi_beam2': rssi_beam2,
              'rssi_beam3': rssi_beam3,
              'rssi_beam4': rssi_beam4}

    ssc_params = {'A': 3.5, 'B':.049}

    cfg = {
        'filename': filename,
        'name': name,
        'pg_min': pg_min,
        'vel_min': vel_min,
        'vel_max': vel_max,
        'echo_min': echo_min,
        'echo_max': echo_max,
        'cormag_min': cormag_min,
        'cormag_max': cormag_max,
        'err_vel_max': err_vel_max,
        'start_datetime': start_datetime,
        'end_datetime': end_datetime,
        'first_good_ensemble': first_good_ensemble,
        'last_good_ensemble': last_good_ensemble,
        'abs_min' : absback_min,
        'abs_max': absback_max,
        'magnetic_declination': magnetic_declination,
        'utc_offset': utc_offset,
        'crp_rotation_angle': crp_rotation_angle,
        'crp_offset_x': crp_offset_x,
        'crp_offset_y': crp_offset_y,
        'crp_offset_z': crp_offset_z,
        'transect_shift_x': transect_shift_x,
        'transect_shift_y': transect_shift_y,
        'transect_shift_z': transect_shift_z,
        'transect_shift_t': transect_shift_t,
        'pos_cfg': pos_cfg,
        'water_properties': water_properties,
        'sediment_properties':sediment_properties,
        'abs_params': abs_params,
        'ssc_params': ssc_params,
    }

    return cfg


def get_value(element: ET.Element, tag: str, default) -> str:
    found = element.find(tag)
    if found is None or found.text is None or found.text.strip() == "":
        return default
    return found.text

cfg = CreateADCPDict(instrument, water, sediment, epsg)