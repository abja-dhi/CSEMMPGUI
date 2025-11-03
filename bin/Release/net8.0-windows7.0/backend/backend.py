
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
        adcp_series_mode = XMLUtils._get_value(root, "ADCPSeriesMode", "bin").lower()
        use_mean = XMLUtils._get_value(root, "UseMean", "no").lower() == 'yes'
        if use_mean:
            adcp_series_target = "mean"
        else:
            if adcp_series_mode == "bin":
                adcp_series_target = int(XMLUtils._get_value(root, "ADCPSeriesTarget", "1"))
            else:
                adcp_series_target = float(XMLUtils._get_value(root, "ADCPSeriesTarget", "0"))
        adcp_transect_color = XMLUtils._get_value(root, "ADCPTransectColor", "black")
        adcp_quiver_scale = float(XMLUtils._get_value(root, "ADCPQuiverScale", "1.0"))
        adcp_quiver_width = float(XMLUtils._get_value(root, "ADCPQuiverWidth", "0.005"))
        adcp_quiver_headwidth = float(XMLUtils._get_value(root, "ADCPQuiverHeadWidth", "3.0"))
        adcp_quiver_headlength = float(XMLUtils._get_value(root, "ADCPQuiverHeadLength", "2.5"))
        adcp_quiver_color = XMLUtils._get_value(root, "ADCPQuiverColor", "black")
        model_field_pixel_size_m = float(XMLUtils._get_value(root, "ModelFieldPixelSizeM", "100.0"))
        model_field_quiver_stride_n = int(XMLUtils._get_value(root, "ModelFieldQuiverStrideN", "3"))
        model_quiver_scale = float(XMLUtils._get_value(root, "ModelQuiverScale", "1.0"))
        model_quiver_width = float(XMLUtils._get_value(root, "ModelQuiverWidth", "0.005"))
        model_quiver_headwidth = float(XMLUtils._get_value(root, "ModelQuiverHeadWidth", "3.0"))
        model_quiver_headlength = float(XMLUtils._get_value(root, "ModelQuiverHeadLength", "2.5"))
        model_quiver_color = XMLUtils._get_value(root, "ModelQuiverColor", "black")
        model_quiver_mode = XMLUtils._get_value(root, "ModelQuiverMode", "field").lower()
        model_levels = [float(l) for l in XMLUtils._get_value(root, "ModelLevels", "0.0,0.1,0.2,0.3,0.4,0.5").split(",")]
        model_vmin = XMLUtils._get_value(root, "Modelvmin", None)
        model_vmin = float(model_vmin) if model_vmin is not None else None
        model_vmax = XMLUtils._get_value(root, "Modelvmax", None)
        model_vmax = float(model_vmax) if model_vmax is not None else None
        model_cmap_name = XMLUtils._get_value(root, "ModelCmapName", "viridis").lower()
        model_bottom_thresh = float(XMLUtils._get_value(root, "ModelBottomThreshold", "0.001"))
        cbar_tick_decimals = int(XMLUtils._get_value(root, "LayoutCbarTickDecimals", "2"))
        axis_tick_decimals = int(XMLUtils._get_value(root, "LayoutAxisTickDecimals", "3"))
        pad_m = float(XMLUtils._get_value(root, "LayoutPadM", "2000"))
        distance_bin_m = float(XMLUtils._get_value(root, "LayoutDistanceBinM", "50"))
        bar_width_scale = float(XMLUtils._get_value(root, "LayoutBarWidthScale", "0.15"))
        results = HDComparison(project, model_id, adcp_id,
                               adcp_series_mode, adcp_series_target, adcp_transect_color, adcp_quiver_scale, adcp_quiver_width, adcp_quiver_headwidth, adcp_quiver_headlength, adcp_quiver_color,
                               model_field_pixel_size_m, model_field_quiver_stride_n, model_quiver_scale, model_quiver_width, model_quiver_headwidth, model_quiver_headlength, model_quiver_color, model_quiver_mode, model_levels, model_vmin, model_vmax, model_cmap_name, model_bottom_thresh,
                               cbar_tick_decimals, axis_tick_decimals, pad_m, distance_bin_m, bar_width_scale)
        
    elif task_type == "MTComparison":
        project = ET.fromstring(root.find("Project").text)
        model_id = root.find("ModelID").text
        adcp_id = root.find("ADCPID").text
        adcp_series_mode = XMLUtils._get_value(root, "ADCPSeriesMode", "bin").lower()
        use_mean = XMLUtils._get_value(root, "UseMean", "no").lower() == 'yes'
        if use_mean:
            adcp_series_target = "mean"
        else:
            if adcp_series_mode == "bin":
                adcp_series_target = int(XMLUtils._get_value(root, "ADCPSeriesTarget", "1"))
            else:
                adcp_series_target = float(XMLUtils._get_value(root, "ADCPSeriesTarget", "0"))
        adcp_transect_color = XMLUtils._get_value(root, "ADCPTransectColor", "black")
        ssc_scale = XMLUtils._get_value(root, "SSCScale", "log").lower()
        ssc_levels = [float(l) for l in XMLUtils._get_value(root, "SSCLevels", "0.001,0.01,0.1,1.0,10.0").split(",")]
        ssc_vmin = XMLUtils._get_value(root, "SSCvmin", None)
        ssc_vmin = float(ssc_vmin) if ssc_vmin is not None else None
        ssc_vmax = XMLUtils._get_value(root, "SSCvmax", None)
        ssc_vmax = float(ssc_vmax) if ssc_vmax is not None else None
        ssc_cmap_name = XMLUtils._get_value(root, "SSCCmapName", "viridis").lower()
        ssc_bottom_thresh = float(XMLUtils._get_value(root, "SSCBottomThreshold", "0.001"))
        ssc_pixel_size_m = float(XMLUtils._get_value(root, "SSCPixelSizeM", "10.0"))
        cbar_tick_decimals = int(XMLUtils._get_value(root, "LayoutCbarTickDecimals", "2"))
        axis_tick_decimals = int(XMLUtils._get_value(root, "LayoutAxisTickDecimals", "3"))
        pad_m = float(XMLUtils._get_value(root, "LayoutPadM", "2000"))
        distance_bin_m = float(XMLUtils._get_value(root, "LayoutDistanceBinM", "50"))
        bar_width_scale = float(XMLUtils._get_value(root, "LayoutBarWidthScale", "0.15"))
        results = MTComparison(project, model_id, adcp_id,
                               adcp_series_mode, adcp_series_target, adcp_transect_color,
                               ssc_scale, ssc_levels, ssc_vmin, ssc_vmax, ssc_cmap_name, ssc_bottom_thresh, ssc_pixel_size_m,
                               cbar_tick_decimals, axis_tick_decimals, pad_m, distance_bin_m, bar_width_scale)

    elif task_type == "HDMTComparison":
        project = ET.fromstring(root.find("Project").text)
        hd_model_id = root.find("HDModelID").text
        mt_model_id = root.find("MTModelID").text
        adcp_id = root.find("ADCPID").text
        adcp_transect_lw = float(XMLUtils._get_value(root, "ADCPTransectLineWidth", "1.8"))
        adcp_series_mode = XMLUtils._get_value(root, "ADCPSeriesMode", "bin").lower()
        use_mean = XMLUtils._get_value(root, "UseMean", "no").lower() == 'yes'
        if use_mean:
            adcp_series_target = "mean"
        else:
            if adcp_series_mode == "bin":
                adcp_series_target = int(XMLUtils._get_value(root, "ADCPSeriesTarget", "1"))
            else:
                adcp_series_target = float(XMLUtils._get_value(root, "ADCPSeriesTarget", "0"))
        adcp_quiver_every_n = int(XMLUtils._get_value(root, "ADCPQuiverEveryN", "20"))
        adcp_quiver_width = float(XMLUtils._get_value(root, "ADCPQuiverWidth", "0.002"))
        adcp_quiver_headwidth = float(XMLUtils._get_value(root, "ADCPQuiverHeadWidth", "2.0"))
        adcp_quiver_headlength = float(XMLUtils._get_value(root, "ADCPQuiverHeadLength", "2.5"))
        adcp_quiver_scale = float(XMLUtils._get_value(root, "ADCPQuiverScale", "3.0"))
        ssc_scale = XMLUtils._get_value(root, "SSCScale", "log").lower()
        ssc_levels = [float(l) for l in XMLUtils._get_value(root, "SSCLevels", "0.001,0.01,0.1,1.0,10.0").split(",")]
        ssc_vmin = XMLUtils._get_value(root, "SSCvmin", None)
        ssc_vmin = float(ssc_vmin) if ssc_vmin is not None else None
        ssc_vmax = XMLUtils._get_value(root, "SSCvmax", None)
        ssc_vmax = float(ssc_vmax) if ssc_vmax is not None else None
        ssc_cmap_name = XMLUtils._get_value(root, "SSCCmapName", "viridis").lower()
        ssc_bottom_thresh = float(XMLUtils._get_value(root, "SSCBottomThreshold", "0.001"))
        model_field_pixel_size_m = float(XMLUtils._get_value(root, "ModelFieldPixelSizeM", "100.0"))
        model_field_quiver_stride_n = int(XMLUtils._get_value(root, "ModelFieldQuiverStrideN", "3"))
        model_quiver_scale = float(XMLUtils._get_value(root, "ModelQuiverScale", "1.0"))
        model_quiver_width = float(XMLUtils._get_value(root, "ModelQuiverWidth", "0.005"))
        model_quiver_headwidth = float(XMLUtils._get_value(root, "ModelQuiverHeadWidth", "3.0"))
        model_quiver_headlength = float(XMLUtils._get_value(root, "ModelQuiverHeadLength", "2.5"))
        model_quiver_color = XMLUtils._get_value(root, "ModelQuiverColor", "black")
        model_quiver_mode = XMLUtils._get_value(root, "ModelQuiverMode", "field").lower()
        cbar_tick_decimals = int(XMLUtils._get_value(root, "LayoutCbarTickDecimals", "2"))
        axis_tick_decimals = int(XMLUtils._get_value(root, "LayoutAxisTickDecimals", "3"))
        pad_m = float(XMLUtils._get_value(root, "LayoutPadM", "2000"))
        results = HDMTComparison(project, hd_model_id, mt_model_id, adcp_id,
                                 adcp_transect_lw, adcp_series_mode, adcp_series_target, adcp_quiver_every_n, adcp_quiver_width, adcp_quiver_headwidth, adcp_quiver_headlength, adcp_quiver_scale,
                                 ssc_scale, ssc_levels, ssc_vmin, ssc_vmax, ssc_cmap_name, ssc_bottom_thresh,
                                 model_field_pixel_size_m, model_field_quiver_stride_n, model_quiver_scale, model_quiver_width, model_quiver_headwidth, model_quiver_headlength, model_quiver_color, model_quiver_mode,
                                 cbar_tick_decimals, axis_tick_decimals, pad_m)

    elif task_type == "HDMTAnimation":
        project = ET.fromstring(root.find("Project").text)
        hd_model_id = root.find("HDModelID").text
        mt_model_id = root.find("MTModelID").text
        ssc_scale = XMLUtils._get_value(root, "SSCScale", "log").lower()
        ssc_levels = [float(l) for l in XMLUtils._get_value(root, "SSCLevels", "0.001,0.01,0.1,1.0,10.0").split(",")]
        ssc_vmin = XMLUtils._get_value(root, "SSCvmin", None)
        ssc_vmin = float(ssc_vmin) if ssc_vmin is not None else None
        ssc_vmax = XMLUtils._get_value(root, "SSCvmax", None)
        ssc_vmax = float(ssc_vmax) if ssc_vmax is not None else None
        ssc_cmap_name = XMLUtils._get_value(root, "SSCCmapName", "viridis").lower()
        ssc_bottom_thresh = float(XMLUtils._get_value(root, "SSCBottomThreshold", "0.001"))
        model_field_pixel_size_m = float(XMLUtils._get_value(root, "ModelFieldPixelSizeM", "100.0"))
        model_field_quiver_stride_n = int(XMLUtils._get_value(root, "ModelFieldQuiverStrideN", "3"))
        model_quiver_scale = float(XMLUtils._get_value(root, "ModelQuiverScale", "1.0"))
        model_quiver_width = float(XMLUtils._get_value(root, "ModelQuiverWidth", "0.005"))
        model_quiver_headwidth = float(XMLUtils._get_value(root, "ModelQuiverHeadWidth", "3.0"))
        model_quiver_headlength = float(XMLUtils._get_value(root, "ModelQuiverHeadLength", "2.5"))
        model_quiver_color = XMLUtils._get_value(root, "ModelQuiverColor", "black")
        animation_start_index = XMLUtils._get_value(root, "AnimationStartIndex", "Start")
        if animation_start_index.lower() != "start":
            animation_start_index = int(animation_start_index)
        else:
            animation_start_index = 0
        animation_end_index = XMLUtils._get_value(root, "AnimationEndIndex", "End")
        if animation_end_index.lower() != "end":
            animation_end_index = int(animation_end_index)
        else:
            animation_end_index = None
        animation_time_step = int(XMLUtils._get_value(root, "AnimationTimeStep", "1"))
        animation_interval = int(XMLUtils._get_value(root, "AnimationInterval", "200"))
        animation_output_file = XMLUtils._get_value(root, "AnimationOutputFile", "")
        if animation_output_file == "":
            animation_output_file = None
        cbar_tick_decimals = int(XMLUtils._get_value(root, "LayoutCbarTickDecimals", "2"))
        axis_tick_decimals = int(XMLUtils._get_value(root, "LayoutAxisTickDecimals", "3"))
        bbox_path = XMLUtils._get_value(root, "LayoutBBox", None)
        if bbox_path is None:
            results = {"Error": "For HD-MT animation, a bounding box shapefile must be provided in BBox Layer."}
            return GenerateOutputXML(results)

        results = HDMTAnimation(project, hd_model_id, mt_model_id,
                                ssc_scale, ssc_levels, ssc_vmin, ssc_vmax, ssc_cmap_name, ssc_bottom_thresh,
                                model_field_pixel_size_m, model_field_quiver_stride_n, model_quiver_scale, model_quiver_width, model_quiver_headwidth, model_quiver_headlength, model_quiver_color,
                                animation_start_index, animation_end_index, animation_time_step, animation_interval, animation_output_file,
                                cbar_tick_decimals, axis_tick_decimals, bbox_path)

    else:
        results = {"Status": "Error", "Message": "Unknown task type"}

    return GenerateOutputXML(results)