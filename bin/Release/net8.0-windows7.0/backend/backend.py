
import xml.etree.ElementTree as ET
from .tasks import *
from .utils_xml import XMLUtils

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
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotBKS2SSCTransect(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask)

    elif task_type == "BKS2NTU":
        project = ET.fromstring(root.find("Project").text)
        sscmodel = ET.fromstring(root.find("SSCModel").text)
        results = BKS2NTUModel(project, sscmodel)

    elif task_type == "PlotBKS2NTURegression":
        project = ET.fromstring(root.find("Project").text)
        sscmodelid = root.find("SSCModelID").text
        title = root.find("Title").text
        results = PlotBKS2NTURegression(project, sscmodelid, title)

    elif task_type == "PlotBKS2NTUTransect":
        project = ET.fromstring(root.find("Project").text)
        sscmodelid = root.find("SSCModelID").text
        beam_sel = root.find("BeamSelection").text
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            beam_sel = "mean"
        field_name = root.find("FieldName").text
        yAxisMode = root.find("yAxisMode").text
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotBKS2NTUTransect(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask)

    elif task_type == "PlotPlatformOrientation":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        title = root.find("Title").text
        results = PlotPlatformOrientation(project, instrument_id, title)

    elif task_type == "PlotFourBeamFlood":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        field_name = root.find("FieldName").text
        xAxisMode = root.find("xAxisMode").text
        yAxisMode = root.find("yAxisMode").text
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotFourBeamFlood(project, instrument_id, field_name, xAxisMode, yAxisMode, cmap, vmin, vmax, title, mask)

    elif task_type == "PlotSingleBeamFlood":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        beam_sel = root.find("BeamSelection").text
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            beam_sel = "mean"
        field_name = root.find("FieldName").text
        xAxisMode = root.find("xAxisMode").text
        yAxisMode = root.find("yAxisMode").text
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotSingleBeamFlood(project, instrument_id, beam_sel, field_name, xAxisMode, yAxisMode, cmap, vmin, vmax, title, mask)

    elif task_type == "PlotVelocityFlood":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        field_name = root.find("FieldName").text.lower()
        coord = root.find("Coord").text.lower()
        xAxisMode = root.find("xAxisMode").text
        yAxisMode = root.find("yAxisMode").text
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        mask = root.find("Mask").text.lower() == 'yes'
        results = PlotVelocityFlood(project, instrument_id, field_name, coord, xAxisMode, yAxisMode, cmap, vmin, vmax, title, mask)

    elif task_type == "PlotTransectVelocities":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        bin_sel = int(root.find("BinSelection").text)
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            bin_sel = "mean"
        scale = float(root.find("VectorScale").text)
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        title = root.find("Title").text
        line_width = float(root.find("LineWidth").text)
        line_alpha = float(root.find("LineAlpha").text)
        hist_bins = int(root.find("HistBins").text)
        results = PlotTransectVelocities(project, instrument_id, bin_sel, scale, title, cmap, vmin, vmax, line_width, line_alpha, hist_bins)

    elif task_type == "PlotBeamGeometryAnimation":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        gif_path = XMLUtils._get_value(root, "AnimationOutputFile", None)
        if gif_path is not None:
            export_gif = True
        else:
            export_gif = False
        results = PlotBeamGeometryAnimation(project, instrument_id, export_gif, gif_path)

    elif task_type == "PlotTransectAnimation":
        project = ET.fromstring(root.find("Project").text)
        instrument_id = root.find("InstrumentID").text
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        gif_path = XMLUtils._get_value(root, "AnimationOutputFile", None)
        if gif_path is not None:
            save_gif = True
        else:
            save_gif = False
        results = PlotTransectAnimation(project, instrument_id, cmap, vmin, vmax, save_gif, gif_path)

    elif task_type == "PlotModelMesh":
        epsg = root.find("EPSG").text
        filename = root.find("Path").text
        title = root.find("Title").text
        results = PlotModelMesh(epsg, filename, title)

    elif task_type == "MapViewer2D":
        project = ET.fromstring(root.find("Project").text)
        results = CallMapViewer2D(project)

    elif task_type == "MapViewer3D":
        project = ET.fromstring(root.find("Project").text)
        results = CallMapViewer3D(project)

    elif task_type == "HDComparison":
        project = ET.fromstring(root.find("Project").text)
        model_id = root.find("ModelID").text
        adcp_id = root.find("ADCPID").text
        model_quiver_mode = root.find("ModelQuiverMode").text.lower()
        field_pixel_size = float(root.find("FieldPixelSize").text)
        field_quiver_stride_n = int(root.find("FieldQuiverStrideN").text)
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        
        results = HDComparison(project, model_id, adcp_id, model_quiver_mode, field_pixel_size, field_quiver_stride_n, cmap)

    elif task_type == "MTComparison":
        project = ET.fromstring(root.find("Project").text)
        model_id = root.find("ModelID").text
        adcp_id = root.find("ADCPID").text
        scale = XMLUtils._get_value(root, "Scale", "log").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        colorbar_tick_decimals = int(XMLUtils._get_value(root, "ColorBarTickDecimals", 2))
        axis_tick_decimals = int(XMLUtils._get_value(root, "AxisTickDecimals", 2))
        pad_m = float(XMLUtils._get_value(root, "PadM", 0.0))
        pixel_size_m = float(XMLUtils._get_value(root, "PixelSizeM", 50.0))
        cmap_bottom_threshold = float(XMLUtils._get_value(root, "CmapBottomThreshold", 0.0))
        transect_color = XMLUtils._get_value(root, "TransectColor", "black")
        bin_configuration = XMLUtils._get_value(root, "BinConfiguration", "bin").lower()
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            bin_target = "mean"
        else:
            if bin_configuration == "bin":
                bin_target = int(XMLUtils._get_value(root, "BinTarget", "1"))
            else:
                bin_target = float(XMLUtils._get_value(root, "BinTarget", "0"))
        results = MTComparison(project, model_id, adcp_id, scale, vmin, vmax, cmap, colorbar_tick_decimals, axis_tick_decimals, pad_m, pixel_size_m, cmap_bottom_threshold, transect_color, bin_configuration, bin_target)

    elif task_type == "HDMTComparison":
        project = ET.fromstring(root.find("Project").text)
        hd_model_id = root.find("HDModelID").text
        mt_model_id = root.find("MTModelID").text
        adcp_id = root.find("ADCPID").text
        scale = XMLUtils._get_value(root, "Scale", "log").lower()
        vmin = XMLUtils._get_value(root, "vmin", None)
        vmin = float(vmin) if vmin is not None else None
        vmax = XMLUtils._get_value(root, "vmax", None)
        vmax = float(vmax) if vmax is not None else None
        cmap = XMLUtils._get_value(root, "Colormap", "viridis").lower()
        cmap_bottom_threshold = float(XMLUtils._get_value(root, "CmapBottomThreshold", 0.0))
        pixel_size_m = float(XMLUtils._get_value(root, "PixelSizeM", 50.0))
        pad_m = float(XMLUtils._get_value(root, "PadM", 0.0))
        colorbar_tick_decimals = int(XMLUtils._get_value(root, "ColorBarTickDecimals", 2))
        axis_tick_decimals = int(XMLUtils._get_value(root, "AxisTickDecimals", 2))
        model_quiver_mode = XMLUtils._get_value(root, "ModelQuiverMode", "field").lower()
        quiver_every_n = int(XMLUtils._get_value(root, "QuiverEveryN", 20))
        quiver_scale = float(XMLUtils._get_value(root, "QuiverScale", 3.0))
        quiver_color_model = XMLUtils._get_value(root, "QuiverColorModel", "black").lower()
        transect_line_width = float(XMLUtils._get_value(root, "TransectLineWidth", 1.8))
        field_pixel_size = float(XMLUtils._get_value(root, "FieldPixelSize", 100.0))
        field_quiver_stride_n = int(XMLUtils._get_value(root, "FieldQuiverStrideN", 3))
        bin_configuration = XMLUtils._get_value(root, "BinConfiguration", "bin").lower()
        use_mean = root.find("UseMean").text.lower() == 'yes'
        if use_mean:
            bin_target = "mean"
        else:
            if bin_configuration == "bin":
                bin_target = int(XMLUtils._get_value(root, "BinTarget", "1"))
            else:
                bin_target = float(XMLUtils._get_value(root, "BinTarget", "0"))
        results = HDMTComparison(project, hd_model_id, mt_model_id, adcp_id, scale, vmin, vmax, cmap, cmap_bottom_threshold, pixel_size_m, pad_m, colorbar_tick_decimals, axis_tick_decimals, model_quiver_mode, quiver_every_n, quiver_scale, quiver_color_model, transect_line_width, field_pixel_size, field_quiver_stride_n, bin_configuration, bin_target)

    

    else:
        results = {"Status": "Error", "Message": "Unknown task type"}

    return GenerateOutputXML(results)