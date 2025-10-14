# ===== Imports =====
from typing import Tuple, List, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker as mticker
from matplotlib.colors import LogNorm, Normalize
from matplotlib.collections import LineCollection
from matplotlib.patches import FancyArrowPatch
from matplotlib.legend_handler import HandlerPatch
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import cmocean as cmo  # optional colormaps
from matplotlib import ticker as mticker
from matplotlib.ticker import FixedLocator

from .utils_dfsu2d import DfsuUtils2D
from .utils_xml import XMLUtils
from .adcp import ADCP as ADCPDataset
from .utils_crs import CRSHelper
from .plotting import PlottingShell
from .utils_shapefile import ShapefileLayer

def plot_mixed_mt_hd_transect(
    mt_model: DfsuUtils2D,
    hd_model: DfsuUtils2D,
    adcp: ADCPDataset,
    crs_helper: CRSHelper,
        

    *,
    # ----- SSC map options -----
    mt_item_number: int = 1,
    scale: str = "log",                               # "log" | "normal"
    levels: Tuple[float, ...] = (0.01, 0.1, 1, 10, 100),
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,                     # mg/L; None → auto
    cmap_name="turbo",                                # or a Colormap object
    cmap_bottom_thresh: float = 0.01,                 # mg/L; transparent below
    pixel_size_m: int = 10,                           # MT raster resolution
    pad_m: float = 2000,                              # bbox padding
    tick_decimals: int = 2,                           # colorbar tick precision
    tick_decimal_precision: int = 3,                  # map axis tick precision
    # ----- Currents (HD) -----
    u_item_number: int = 4,
    v_item_number: int = 5,
    model_quiver_mode: str = "field",                 # "transect" | "field"
    quiver_every_n: int = 20,                         # along-track thinning
    quiver_scale: float = 3,                          # both layers
    quiver_color_model: str = "black",
    adcp_transect_lw: float = 1.8,
    field_pixel_size_m: int = 100,                    # coarse field res (field mode)
    field_quiver_stride_n: int = 3,                   # stride for field vectors
    # ----- ADCP aggregation (SSC coloring + vectors) -----
    adcp_series_mode: str = "bin",                    # "bin" | "range" | "hab"
    adcp_series_target="mean",                        # numeric or "mean"/"pXX"
    # ----- Shapefiles (optional) -----
    shapefile_layers: Optional[List[ShapefileLayer]] = None,
    # ----- Layout: figure + colorbar + metadata -----
    FIG_W: float = 6.5,
    FIG_H: float = 9.0,
    LEFT: float = 0.06,
    RIGHT: float = 0.6, 
    TOP: float = 0.98, 
    BOTTOM: float = 0.00,
    HSPACE: float = 0.22, 
    CB_WIDTH: float = 0.012,
    CB_GAP: float = 0.008,
    META_TOP_Y: float = 0.95,
    META_SECTION_GAP: float = 0.20,
    META_LINE_GAP: float = 0.16,
    META_LEFT_OVERSHOOT: float = 0.0,
    META_COL_START: float = 0.02, 
    META_COL_END: float = 0.70, META_COLS: int = 3,
):
    """
    Mixed MT–HD transect plot.

    Top:
        MT SSC raster over bbox, ADCP track colored by SSC, ADCP quivers colored by SSC,
        Model quivers single color (or coarse field vectors).
    Bottom:
        Metadata block.

    Returns
    -------
    fig : matplotlib.figure.Figure
    (ax0, ax2) : tuple[Axes, Axes]
    """
    if shapefile_layers is None:
        shapefile_layers = []

    # ----- Aliases -----
    xq = np.asarray(adcp.position.x).ravel()
    yq = np.asarray(adcp.position.y).ravel()
    t = adcp.time.ensemble_datetimes

    # ============================== DERIVED / HELPERS ==============================
    def _fmt_num(v: float, nd: int) -> str:
        return f"{v:.{nd}f}"

    x_label, y_label = crs_helper.axis_labels()
    bbox = crs_helper.bbox_from_coords(xq, yq, pad_m=pad_m, from_crs=adcp.position.epsg)
    META_COL_X = list(np.linspace(META_COL_START, META_COL_END, META_COLS))

    # ============================== FIGURE SHELL ==============================
    fig, ax = PlottingShell.subplots(
        figheight=FIG_H, figwidth=FIG_W, nrow=2, ncol=1, height_ratios=[1.00, 0.28]
    )
    fig.subplots_adjust(left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM, hspace=HSPACE)
    ax0, ax2 = ax

    # ====================================================================== TOP — MT SSC raster + ADCP/Model vectors
    ssc_img, extent = mt_model.rasterize_idw_bbox(
        item_number=mt_item_number, bbox=bbox, t=t, pixel_size_m=pixel_size_m
    )
    ssc_img = np.asarray(ssc_img, float) * 1000.0  # mg/L
    finite = np.isfinite(ssc_img)
    if not finite.any():
        raise ValueError("No finite SSC values in model raster.")

    auto_min = float(np.nanmin(ssc_img[finite]))
    auto_max = float(np.nanmax(ssc_img[finite]))
    cbar_min = vmin if vmin is not None else (min(levels) if levels else max(cmap_bottom_thresh, auto_min))
    cbar_max = vmax if vmax is not None else (max(levels) if levels else auto_max)
    cbar_min = max(cmap_bottom_thresh, cbar_min)
    if (not np.isfinite(cbar_min)) or (not np.isfinite(cbar_max)) or (cbar_min >= cbar_max):
        cbar_min, cbar_max = max(cmap_bottom_thresh, 0.01), max(cmap_bottom_thresh * 100.0, 100.0)

    norm = LogNorm(vmin=cbar_min, vmax=cbar_max, clip=True) if str(scale).lower() == "log" \
        else Normalize(vmin=cbar_min, vmax=cbar_max, clip=True)
    cmap = plt.get_cmap(cmap_name) if isinstance(cmap_name, str) else cmap_name
    cmap = cmap.copy()
    cmap.set_under(alpha=0.0)

    # ADCP SSC for coloring track + ADCP vectors
    adcp_ssc_ts, _ = adcp.get_beam_series(
        field_name="suspended_solids_concentration", mode=adcp_series_mode, target=adcp_series_target
    )
    adcp_ssc_ts = np.asarray(adcp_ssc_ts, float)

    # Draw base SSC raster + shapefiles
    im = ax0.imshow(ssc_img, extent=extent, origin="lower", cmap=cmap, norm=norm, interpolation="nearest")
    for layer in shapefile_layers:
        layer.plot(ax0)

    # ADCP track colored by SSC
    pts = np.column_stack([xq, yq])
    if pts.shape[0] >= 2:
        segs = np.stack([pts[:-1], pts[1:]], axis=1)  # (n-1, 2, 2)
        n_seg = segs.shape[0]
        ssc_line = np.asarray(adcp_ssc_ts[:n_seg], float)
        lc = LineCollection(segs, cmap=cmap, norm=norm, linewidths=adcp_transect_lw, alpha=0.95, zorder=12)
        lc.set_array(np.clip(ssc_line, cbar_min, cbar_max))
        ax0.add_collection(lc)
    else:
        ax0.plot(xq, yq, color="k", lw=adcp_transect_lw, alpha=0.9, zorder=12)

    # ADCP quivers colored by SSC
    adcp_u_ts, _ = adcp.get_velocity_series(component="u", mode=adcp_series_mode, target=adcp_series_target)
    adcp_v_ts, _ = adcp.get_velocity_series(component="v", mode=adcp_series_mode, target=adcp_series_target)
    adcp_u_ts = np.asarray(adcp_u_ts, float)
    adcp_v_ts = np.asarray(adcp_v_ts, float)
    idx = np.arange(0, xq.size, max(1, int(quiver_every_n)))
    C_adcp = np.clip(adcp_ssc_ts[:xq.size][idx], cbar_min, cbar_max)
    ax0.quiver(
        xq[idx], yq[idx], adcp_u_ts[idx], adcp_v_ts[idx],
        C_adcp, cmap=cmap, norm=norm,
        scale=quiver_scale, width=0.002, headwidth=3, headlength=4, pivot="tail",
        alpha=0.95, zorder=14
    )

    # MODEL quivers: transect or coarse field
    if model_quiver_mode.lower() == "transect":
        mu = np.asarray(hd_model.extract_transect_idw(xq, yq, t, item_number=u_item_number)[0], float)
        mv = np.asarray(hd_model.extract_transect_idw(xq, yq, t, item_number=v_item_number)[0], float)
        ax0.quiver(
            xq[idx], yq[idx], mu[idx], mv[idx],
            color=quiver_color_model, scale=quiver_scale, width=0.002,
            headwidth=3, headlength=4, pivot="tail", alpha=0.9, zorder=13
        )
    elif model_quiver_mode.lower() == "field":
        Uc, ext_u = hd_model.rasterize_idw_bbox(item_number=u_item_number, bbox=bbox, t=t, pixel_size_m=field_pixel_size_m)
        Vc, ext_v = hd_model.rasterize_idw_bbox(item_number=v_item_number, bbox=bbox, t=t, pixel_size_m=field_pixel_size_m)
        if ext_u != ext_v:
            raise RuntimeError("Field-mode U and V raster extents differ.")
        xmin, xmax, ymin, ymax = ext_u
        ny, nx = np.asarray(Uc).shape
        dx = (xmax - xmin) / nx
        dy = (ymax - ymin) / ny
        xs = np.linspace(xmin + dx * 0.5, xmax - dx * 0.5, nx)
        ys = np.linspace(ymin + dy * 0.5, ymax - dy * 0.5, ny)
        XX, YY = np.meshgrid(xs, ys)
        stride = max(1, int(field_quiver_stride_n))
        ax0.quiver(
            XX[::stride, ::stride], YY[::stride, ::stride],
            Uc[::stride, ::stride], Vc[::stride, ::stride],
            color=quiver_color_model, scale=quiver_scale, width=0.002,
            headwidth=3, headlength=4, pivot="tail", alpha=0.85, zorder=13
        )
    else:
        raise ValueError("model_quiver_mode must be 'transect' or 'field'.")

    # Axes, limits, labels
    ax0.set_xlabel(x_label)
    ax0.set_ylabel(y_label)
    xmin, xmax, ymin, ymax = bbox
    ax0.set_xlim(xmin, xmax)
    ax0.set_ylim(ymin, ymax)
    ax0.set_aspect("equal", adjustable="box")
    ax0.set_title(f"SSC Field + Currents — {adcp.name}", fontsize=8)
    xy_fmt = mticker.FuncFormatter(lambda v, pos: f"{v:.{tick_decimal_precision}f}")
    ax0.xaxis.set_major_formatter(xy_fmt)
    ax0.yaxis.set_major_formatter(xy_fmt)

    # ----- Colorbar (robust, no clipping) -----
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    fig.canvas.draw()
    divider = make_axes_locatable(ax0)
    
    # convert your figure-fraction widths to axes-relative percent and inch pad
    fig_w_in = fig.get_size_inches()[0]
    axw_fig  = ax0.get_position().width
    cb_pct   = (CB_WIDTH / axw_fig) * 100.0                 # e.g., "1.2%"
    pad_in   = max(0.02, CB_GAP * fig_w_in)                 # gap in inches
    
    cax = divider.append_axes("right", size=f"{cb_pct:.3f}%", pad=pad_in)
    cb  = fig.colorbar(im, cax=cax)
    cb.ax.set_ylabel("Mean SSC During Transect (mg/L)", fontsize=7)
    cb.ax.tick_params(labelsize=6)

    
    # choose ticks: prefer your `levels`, fall back if empty
    _ticks = [v for v in (levels or []) if cbar_min <= v <= cbar_max]
    if not _ticks:
        _ticks = (np.geomspace(cbar_min, cbar_max, 6)
                  if scale.lower() == "log" else
                  np.linspace(cbar_min, cbar_max, 6))
    
    # force numeric labels, no sci notation
    cb.locator   = FixedLocator(_ticks)      # lock tick positions
    cb.set_ticks(_ticks)
    cb.formatter = mticker.FuncFormatter(lambda v, pos: f"{v:.{tick_decimals}f}")
    cb.update_ticks()

    
    # Legend with arrow patches
    EDGE_LW = 0.05
    TAIL_W = 0.1
    HEAD_W = 0.5
    HEAD_L = 0.5

    if np.isfinite(C_adcp).any():
        _mean_ssc_leg = float(np.nanmean(C_adcp))
    else:
        _mean_ssc_leg = 0.5 * (cbar_min + cbar_max)
    adcp_mean_rgba = cmap(norm(_mean_ssc_leg))

    # Thin overlay of ADCP track in the same mean color
    ax0.plot(xq, yq, color=adcp_mean_rgba, lw=adcp_transect_lw * 0.75, alpha=0.9, zorder=12.5)

    def _legend_arrow(legend, orig_handle, xdescent, ydescent, width, height, fontsize):
        y = ydescent + 0.5 * height
        x0 = xdescent + 0.12 * width
        x1 = xdescent + 0.88 * width
        ms = 0.95 * height
        arr = FancyArrowPatch(
            (x0, y), (x1, y),
            arrowstyle=f"Simple,tail_width={TAIL_W},head_width={HEAD_W},head_length={HEAD_L}",
            mutation_scale=ms,
            facecolor=orig_handle.get_facecolor(),
            edgecolor=orig_handle.get_edgecolor(),
            linewidth=EDGE_LW,
            joinstyle="miter", capstyle="projecting",
        )
        arr.set_path_effects([
            pe.Stroke(linewidth=max(EDGE_LW + 0.2, 0.3), foreground=orig_handle.get_edgecolor()),
            pe.Normal()
        ])
        return arr

    h_model = FancyArrowPatch((0, 0), (1, 0),
                              facecolor=quiver_color_model, edgecolor="black", linewidth=EDGE_LW)
    h_adcp = FancyArrowPatch((0, 0), (1, 0),
                             facecolor=adcp_mean_rgba, edgecolor="black", linewidth=EDGE_LW)
    h_trk = Line2D([0], [0], color=adcp_mean_rgba, lw=adcp_transect_lw)

    leg = ax0.legend(
        [h_model, h_adcp, h_trk],
        ["Model vectors", "ADCP vectors (mean SSC color)", "ADCP track (mean SSC color)"],
        handler_map={FancyArrowPatch: HandlerPatch(patch_func=_legend_arrow)},
        loc="upper left", frameon=True, fontsize=7, framealpha=1.0, fancybox=False,
    )
    leg.get_frame().set_edgecolor("black")

    # ====================================================================== BOTTOM — metadata
    u_ts = np.asarray(hd_model.extract_transect_idw(xq, yq, t, item_number=u_item_number)[0], float)
    v_ts = np.asarray(hd_model.extract_transect_idw(xq, yq, t, item_number=v_item_number)[0], float)
    spd_ts = np.hypot(u_ts, v_ts)
    model_ssc_ts = np.asarray(
        mt_model.rasterize_idw_bbox(item_number=mt_item_number, bbox=bbox, t=t, pixel_size_m=pixel_size_m)[0],
        float
    ).ravel() * 1000.0

    n = min(adcp_ssc_ts.size, model_ssc_ts.size, spd_ts.size)
    valid = np.isfinite(adcp_ssc_ts[:n]) & np.isfinite(model_ssc_ts[:n]) & np.isfinite(spd_ts[:n])
    adcp_ssc_ts = adcp_ssc_ts[:n][valid]
    model_ssc_ts = model_ssc_ts[:n][valid]
    spd_ts = spd_ts[:n][valid]
    t_arr = np.asarray(t)[:n][valid]

    t0 = pd.to_datetime(t_arr.min())
    t1 = pd.to_datetime(t_arr.max())
    dur_min = (t1 - t0).total_seconds() / 60.0
    mean_ssc_model = float(np.nanmean(model_ssc_ts))
    mean_ssc_obs = float(np.nanmean(adcp_ssc_ts))
    mean_ssc_err = float(np.nanmean(model_ssc_ts - adcp_ssc_ts))
    mean_spd = float(np.nanmean(spd_ts))

    ax2.clear()
    ax2.set_axis_off()
    fmt_time = lambda dt: dt.strftime("%d %b. %Y %H:%M")

    def H(x, y, text):
        ax2.text(x, y, text, ha="left", va="top", fontsize=8, fontweight="bold", family="monospace")

    def I(x, y, k, v):
        ax2.text(x, y, f"{k}: {v}", ha="left", va="top", fontsize=7, family="monospace")

    fig.canvas.draw()
    p2 = ax2.get_position()
    ax2.set_aspect("auto")
    ax2.set_anchor("W")
    try:
        ax2.set_box_aspect(None)
    except Exception:
        pass
    new_x0 = ax0.get_position().x0 - META_LEFT_OVERSHOOT
    new_w = min(ax0.get_position().width + META_LEFT_OVERSHOOT, 1.0 - new_x0)
    ax2.set_position([new_x0, p2.y0, new_w, p2.height])

    y0 = META_TOP_Y
    sec = META_SECTION_GAP
    line = META_LINE_GAP
    cols_x = META_COL_X

    # Column 1
    x = cols_x[0]
    y = y0
    H(x, y, "Observation Aggregation")
    y -= sec
    I(x, y, "SSC mode", adcp_series_mode)
    y -= line
    I(x, y, "SSC target", adcp_series_target)
    y -= line
    I(x, y, "Vector mode", model_quiver_mode)

    # Column 2
    x = cols_x[1]
    y = y0
    H(x, y, "Transect Timing")
    y -= sec
    I(x, y, "Start", fmt_time(t0))
    y -= line
    I(x, y, "End", fmt_time(t1))
    y -= line
    I(x, y, "Duration", f"{dur_min:.1f} min")

    # Column 3
    x = cols_x[2]
    y = y0
    H(x, y, "Summary")
    y -= sec
    I(x, y, "Mean SSC (obs)", f"{mean_ssc_obs:.{tick_decimals}f} mg/L")
    y -= line
    I(x, y, "Mean SSC (model)", f"{mean_ssc_model:.{tick_decimals}f} mg/L")
    y -= line
    I(x, y, "Mean SSC error", f"{mean_ssc_err:.{tick_decimals}f} mg/L")
    y -= line
    I(x, y, "Mean speed (model)", f"{mean_spd:.{tick_decimals}f} m/s")

    return fig, (ax0, ax2)


# ===== Example usage =====
if __name__ == "__main__":
    # Project + ADCP config
    xml_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Projects/Clean Project F3 2 Oct 2024.mtproj'
    project = XMLUtils(xml_path)
    adcp_cfgs = project.get_cfgs_from_survey(
        survey_name="20241002_F3(E)", survey_id=0, instrument_type="VesselMountedADCP"
    )
    adcp_cfg = adcp_cfgs[9]
    adcp_cfg["velocity_average_window_len"] = 10

    # CRS + models
    crs_helper = CRSHelper(project_crs=4326)

    model_fpath_hd = r'\\USDEN1-STOR.DHI.DK\\Projects\\61803553-05\\Models\\F3\\2024\\10. October\\HD\\HDD20241002.dfsu'
    hd_model = DfsuUtils2D(model_fpath_hd, crs_helper=crs_helper)

    model_fpath_mt = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002_1.dfsu'
    mt_model = DfsuUtils2D(model_fpath_mt, crs_helper=crs_helper)

    adcp = ADCPDataset(adcp_cfg, name=adcp_cfg["name"])

    # Optional shapefiles
    shapefile_layers = [
        ShapefileLayer(
            path=r"\\usden1-stor.dhi.dk\Projects\61803553-05\GIS\SG Coastline\RD7550_CEx_SG_v20250509.shp",
            kind="polygon",
            crs_helper=crs_helper,
            poly_edgecolor="black",
            poly_linewidth=0.6,
            poly_facecolor="none",
            alpha=1.0,
            zorder=10,
        ),
        ShapefileLayer(
            path=r"\\usden1-stor.dhi.dk\Projects\61803553-05\GIS\F3\example point layer\points_labels.shp",
            kind="point",
            crs_helper=crs_helper,
            point_color="black",
            point_marker="o",
            point_markersize=10,
            alpha=1.0,
            zorder=14,
            label_text="Source Location",
            label_offset_pts=(1, 1),
            label_fontsize=8,
            label_color="black",
            label_ha="left",
            label_va="center",
        ),
    ]

    fig, (ax_map, ax_meta) = plot_mixed_mt_hd_transect(
        mt_model,
        hd_model,
        adcp,
        crs_helper,
        mt_item_number=1,
        scale="log",
        levels=(0.01, 0.1, 1, 10, 100),
        vmin=None,
        vmax=None,
        cmap_name="turbo",
        cmap_bottom_thresh=0.01,
        pixel_size_m=10,
        pad_m=2000,
        tick_decimals=2,
        tick_decimal_precision=3,
        u_item_number=4,
        v_item_number=5,
        model_quiver_mode="field",          # "transect" | "field"
        quiver_every_n=20,
        quiver_scale=3,
        quiver_color_model="black",
        adcp_transect_lw=1.8,
        field_pixel_size_m=100,
        field_quiver_stride_n=3,
        adcp_series_mode="bin",
        adcp_series_target="mean",
        shapefile_layers=shapefile_layers,
        FIG_W=6.5,
        FIG_H=9.0,
        LEFT=0.06,
        RIGHT=0.90,
        TOP=0.98, 
        BOTTOM=0.00,
        HSPACE=0.22,
        CB_WIDTH=0.012,
        CB_GAP=0.008,
        META_TOP_Y=0.95,
        META_SECTION_GAP=0.20,
        META_LINE_GAP=0.16,
        META_LEFT_OVERSHOOT=0.0,
        META_COL_START=0.02, META_COL_END=0.70, META_COLS=3,
    )

    plt.show()

