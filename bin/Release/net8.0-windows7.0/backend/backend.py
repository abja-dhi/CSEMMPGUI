
import xml.etree.ElementTree as ET
from .tasks import *

def Call(XML):

    root = ET.fromstring(XML)
    task_type = root.find("Task").text

    if task_type == "HelloBackend":
        results = {"Status": "Hi there"}

    elif task_type == "LoadPd0":
        filepath = root.find("Path").text
        results = LoadPd0(filepath)
        
    elif task_type == "Extern2CSVSingle":
        filepath = root.find("Path").text
        results = Extern2CSVSingle(filepath)

    elif task_type == "Extern2CSVBatch":
        folderpath = root.find("Path").text
        results = Extern2CSVBatch(folderpath)

    elif task_type == "ViSeaSample2CSV":
        filepath = root.find("Path").text
        results = ViSeaSample2CSV(filepath)

    elif task_type == "Dfs2ToDfsu":
        in_path = root.find("InPath").text
        out_path = root.find("OutPath").text
        results = Dfs2ToDfsu(in_path, out_path)

    elif task_type == "GetColumnsFromCSV":
        filepath = root.find("Path").text
        header = int(root.find("Header").text)
        sep = root.find("Sep").text
        results = GetColumnsFromCSV(filepath, header, sep)

    elif task_type == "InstrumentSummaryADCP":
        filepath = root.find("Path").text
        results = InstrumentSummaryADCP(filepath)
        
    elif task_type == "ReadCSV":
        Root = root.find("Root").text
        SubElement = root.find("SubElement").text
        filepath = root.find("Path").text
        header = int(root.find("Header").text)
        sep = root.find("Sep").text
        items = root.find("Items").text.split(",")
        columns = [int(c) for c in root.find("Columns").text.split(",")]
        results = ReadCSV(Root, SubElement, filepath, header, sep, items, columns)

    elif task_type == "NTU2SSC":
        project = ET.fromstring(root.find("Project").text)
        sscmodel = ET.fromstring(root.find("SSCModel").text)
        results = NTU2SSCModel(project, sscmodel)

    elif task_type == "PlotNTU2SSCRegression":
        project = ET.fromstring(root.find("Project").text)
        sscmodelid = root.find("SSCModelID").text
        title = root.find("Title").text
        results = PlotNTU2SSCRegression(project, sscmodelid, title)

    elif task_type == "BKS2SSC":
        project = ET.fromstring(root.find("Project").text)
        sscmodel = ET.fromstring(root.find("SSCModel").text)
        results = BKS2SSCModel(project, sscmodel)

    elif task_type == "PlotBKS2SSCRegression":
        project = ET.fromstring(root.find("Project").text)
        sscmodelid = root.find("SSCModelID").text
        title = root.find("Title").text
        results = PlotBKS2SSCRegression(project, sscmodelid, title)

    elif task_type == "PlotBKS2SSCTransect":
        project = ET.fromstring(root.find("Project").text)
        sscmodelid = root.find("SSCModelID").text
        beam_sel = root.find("BeamSelection").text
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            beam_sel = "mean"
        field_name = root.find("FieldName").text
        yAxisMode = root.find("yAxisMode").text
        cmap = get_value(root, "Colormap", "viridis").lower()
        vmin = get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotBKS2SSCTransect(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask)


    elif task_type == "PlotPlatformOrientation":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        title = root.find("Title").text
        results = PlotPlatformOrientation(project, instrument_id, title)

    elif task_type == "PlotFourBeamFlood":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        field_name = root.find("FieldName").text
        yAxisMode = root.find("yAxisMode").text
        cmap = get_value(root, "Colormap", "viridis").lower()
        vmin = get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotFourBeamFlood(project, instrument_id, field_name, yAxisMode, cmap, vmin, vmax, title, mask)

    elif task_type == "PlotSingleBeamFlood":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        beam_sel = root.find("BeamSelection").text
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            beam_sel = "mean"
        field_name = root.find("FieldName").text
        yAxisMode = root.find("yAxisMode").text
        cmap = get_value(root, "Colormap", "viridis").lower()
        vmin = get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotSingleBeamFlood(project, instrument_id, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask)

    elif task_type == "PlotTransectVelocities":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        bin_sel = root.find("BinSelection").text
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            bin_sel = "mean"
        scale = float(root.find("VectorScale").text)
        cmap = get_value(root, "Colormap", "viridis").lower()
        vmin = get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        line_width = float(root.find("LineWidth").text)
        line_alpha = float(root.find("LineAlpha").text)
        hist_bins = int(root.find("HistBins").text)
        results = PlotTransectVelocities(project, instrument_id, bin_sel, scale, title, cmap, vmin, vmax, line_width, line_alpha, hist_bins)

    elif task_type == "PlotBeamGeometryAnimation":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        results = PlotBeamGeometryAnimation(project, instrument_id)

    elif task_type == "PlotTransectAnimation":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        cmap = get_value(root, "Colormap", "viridis").lower()
        vmin = get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        results = PlotTransectAnimation(project, instrument_id, cmap, vmin, vmax)

    elif task_type == "PlotModelMesh":
        epsg = root.find("EPSG").text
        filename = root.find("Path").text
        title = root.find("Title").text
        results = PlotModelMesh(epsg, filename, title)

    elif task_type == "MapViewer2D":
        project = ET.fromstring(root.find("Project").text)
        settings = find_element(project, "1", "Settings")
        mapSettings = find_element(project, "2", "MapSettings")
        results = CallMapViewer2D(settings, mapSettings)

    else:
        results = {"Status": "Error", "Message": "Unknown task type"}

    return GenerateOutputXML(results)