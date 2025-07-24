# {
#   "function": "compareWaterSamples",
#   "input": XML,
# }

import subplots
import pandas as pd
import pyplume as pp

def call(json_args):
  
  if function == "loadADCP":
    metadata = json_args.get("input")
    pd0Path = metadata.get("path")
    ds = pp.Dataset(pd0Path)
    return ds

  elif function == "fourBeamPlot":
    metadata = json_args.get("input")
    pd0Path = metadata.get("path")
    ds = pp.Dataset(pd0Path)
    plot_by = json_args.get("plot_by", "bin")
    variable = json_args.get("variable", "echo_intensity")
    ax = ds.four_beam_plot(plot_by=plot_by, variable=variable)

  elif function == "surveyPositionPlot":
    metadata = json_args.get("input")
    metadata = pd.read_xml(metadata)
    fig, ax = subplots()
    for item in metadata:
      pd0Path = item.get("path")
      ds = pp.Dataset(pd0Path)
      ds.survey_position_plot(ax=ax, variable="position", label=item.get("label"))
    return ax

  elif function == "NTUTSSmodel":
   metadata = json_args.get("input")
   metadata = pd.read_xml(metadata)
   water_samples_mask = metadata.type == ["Water Sample"]
   OBS_mask = metadata.type == ["OBS"]
   water_samples = metadata[water_samples_mask]
   OBSs = metadata[OBS_mask]

   return a, b

  elif function == "NTU2SSC":
   metadata = json_args.get("input")
   metadata = pd.read_xml(metadata)
   OBS_mask = metadata.type == ["OBS"]
   regParameters_mask = metadata.type == ["Regression Parameters"]
   OBSs = metadata[OBS_mask]
   regParameters = metadata[regParameters_mask]
   a = regParameters.a
   b = regParameters.b
   for OBS in OBSs:
      OBS.NTU2SSC(a=a, b=b)

  elif function == "OBSplotBySSC":
   metadata = json_args.get("input")
   metadata = pd.read_xml(metadata)
   OBS_mask = metadata.type == ["OBS"]
   regParameters_mask = metadata.type == ["Regression Parameters"]
   OBSs = metadata[OBS_mask]
   regParameters = metadata[regParameters_mask]
   a = regParameters.a
   b = regParameters.b
   for OBS in OBSs:
      OBS.NTU2SSC(a=a, b=b)
   fig, ax = subplots()
   ax.plot(OBS.depth, OBS.SSC, label=OBS.name)
   return ax


  elif function == "Backscatter2SSC":
    metadata = json_args.get("input")
    metadata = pd.read_xml(metadata)
    OBS_mask = metadata.type == ["OBS"]
    WaterSample_mask = metadata.type == ["Water Sample"]
    ADCP_mask = metadata.type == ["ADCP"]
    WaterSamples = metadata[WaterSample_mask]
    ADCPs = metadata[ADCP_mask]
    OBSs = metadata[OBS_mask]

  elif function == "CompareTransect2Model":
    pass