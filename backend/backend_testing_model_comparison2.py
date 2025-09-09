from utils_dfsu2d import DfsuUtils2D
from utils_xml import XMLUtils
from adcp import ADCP as ADCPDataset
from utils_crs import CRSHelper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker as mticker
from matplotlib.colors import LogNorm, Normalize
from matplotlib.ticker import FixedLocator
from plotting import PlottingShell
from utils_shapefile import ShapefileLayer
# ============================== LOAD DATA (run once) ==============================
# Load heavy objects a single time, then reuse during plotting.


# Project and configs
xml_path = r'//usden1-stor.dhi.dk/Projects/61803553-05/Projects/Clean Project F3 2 Oct 2024.mtproj'
project = XMLUtils(xml_path)
adcp_cfgs = project.get_cfgs_from_survey(survey_name="20241002_F3(E)", survey_id=0, instrument_type="VesselMountedADCP")
adcp_cfg = adcp_cfgs[0]

# CRS + model path
crs_helper = CRSHelper(project_crs=4326)
model_fpath = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002_1.dfsu'

# Heavy objects
mt_model = DfsuUtils2D(model_fpath, crs_helper=crs_helper)
adcp     = ADCPDataset(adcp_cfg, name=adcp_cfg["name"])

# Lightweight aliases for plotting
xq = adcp.position.x
yq = adcp.position.y
t  = adcp.time.ensemble_datetimes


#%%
#%% ============================== PLOT (portrait, stacked) ==============================
# Three rows, one column. Word page portrait. Space left for caption.



# ---- Inputs ----
mt_model_item_number   = 1
scale                  = "log"                   # "log" or "normal"
vmin, vmax             = None, None              # mg/L
levels                 = [0.01, 0.1, 1, 10, 100] # mg/L ticks
cmap_name              = "turbo"
tick_decimals          = 2
tick_decimal_precision = 3
pad_m                  = 1500
pixel_size_m           = 10
cmap_bottom_thresh     = 0.01
adcp_transect_color    = "magenta"
distance_bin_m         = 50
bar_width_scale        = 0.15                    # thinner bars
adcp_series_field      = "suspended_solids_concentration"
adcp_series_mode       = "bin"                   # "bin" | "depth" | "hab"
adcp_series_target     = "mean"                  # "mean" | "pXX"

# Axis labels from CRS helper
x_label, y_label = crs_helper.axis_labels()

# Optional shapefile overlays (list)
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
    # add more ShapefileLayer(...) here as needed
]

# ======================================================================
# CLEAN LAYOUT CONTROLS — explicit margins and spacing
# ======================================================================
FIG_W, FIG_H   = 6.5, 9.0            # figure size (inches)
LEFT, RIGHT    = 0.06, 0.96          # figure margins
TOP, BOTTOM    = 0.98, 0.10
HSPACE         = 0.22                 # spacing between stacked subplots
CB_WIDTH       = 0.012                # colorbar width (figure fraction)

#%%
# ======================================================================
# FIGURE SHELL
# ======================================================================
fig, ax = PlottingShell.subplots(
    figheight=FIG_H, figwidth=FIG_W, nrow=3, ncol=1,
    height_ratios=[1.00, 0.30, 0.22]
)
fig.subplots_adjust(left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM, hspace=HSPACE)
ax0, ax1, ax2 = ax

# ======================================================================
# TOP — Model SSC raster (mg/L)
# ======================================================================
bbox = crs_helper.bbox_from_coords(xq, yq, pad_m=pad_m, from_crs=adcp.position.epsg)
model_img = mt_model.rasterize_idw_bbox(item_number=mt_model_item_number, bbox=bbox, t=t, pixel_size_m=pixel_size_m)
model_ssc_img = model_img[0] * 1000.0
model_extent  = model_img[1]

data = np.asarray(model_ssc_img, dtype=float)
finite = np.isfinite(data)
if not finite.any():
    raise ValueError("No finite SSC values in model raster.")

auto_min = float(np.nanmin(data[finite])); auto_max = float(np.nanmax(data[finite]))
cbar_min = vmin if vmin is not None else (min(levels) if levels else max(cmap_bottom_thresh, auto_min))
cbar_max = vmax if vmax is not None else (max(levels) if levels else auto_max)
cbar_min = max(cmap_bottom_thresh, cbar_min)
if (not np.isfinite(cbar_min)) or (not np.isfinite(cbar_max)) or (cbar_min >= cbar_max):
    cbar_min, cbar_max = max(cmap_bottom_thresh, 0.01), max(cmap_bottom_thresh * 100, 100.0)

cmap = plt.get_cmap(cmap_name).copy(); cmap.set_under(alpha=0.0)
norm = LogNorm(vmin=cbar_min, vmax=cbar_max, clip=True) if scale.lower() == "log" else Normalize(vmin=cbar_min, vmax=cbar_max, clip=True)

im = ax0.imshow(data, extent=model_extent, origin="lower", cmap=cmap, norm=norm, interpolation="nearest")
for layer in shapefile_layers:
    layer.plot(ax0)
ax0.plot(xq, yq, color=adcp_transect_color, lw=1.0, alpha=0.9)

ax0.set_xlabel(x_label); ax0.set_ylabel(y_label)
xmin, xmax, ymin, ymax = bbox
ax0.set_xlim(xmin, xmax); ax0.set_ylim(ymin, ymax)
ax0.set_aspect("equal", adjustable="box")
ax0.set_title("Model SSC (mg/L)", fontsize=8)

xy_fmt = mticker.FuncFormatter(lambda v, pos: f"{v:.{tick_decimal_precision}f}")
ax0.xaxis.set_major_formatter(xy_fmt); ax0.yaxis.set_major_formatter(xy_fmt)

# --- FLUSH COLORBAR USING A DEDICATED AXIS, ALIGNED TO ax0 RIGHT EDGE ---
fig.canvas.draw()                       # freeze layout before reading positions
pos0 = ax0.get_position()
ax0.set_position([pos0.x0, pos0.y0, pos0.width - CB_WIDTH, pos0.height])  # make room exactly equal to CB_WIDTH
fig.canvas.draw()
pos = ax0.get_position()
cb_ax = fig.add_axes([pos.x1, pos.y0, CB_WIDTH, pos.height])              # exact vertical match with ax0
cb = plt.colorbar(im, cax=cb_ax)
cb.ax.set_ylabel("Mean SSC During Transect (mg/L)", fontsize=7)
cb.ax.tick_params(labelsize=6)
# numeric tick labels
def _fmt_num(v: float, nd: int) -> str: return f"{v:.{nd}f}"
_ticks = sorted(set((levels or []) + [cbar_min])); _ticks = [v for v in _ticks if cbar_min <= v <= cbar_max]
if _ticks:
    cb.set_ticks(_ticks); cb.set_ticklabels([_fmt_num(v, tick_decimals) for v in _ticks])
else:
    _cb_ticks = np.linspace(cbar_min, cbar_max, 5)
    cb.set_ticks(_cb_ticks); cb.set_ticklabels([_fmt_num(v, tick_decimals) for v in _cb_ticks])

# ======================================================================
# MIDDLE — Distance-binned SSC (Model vs ADCP)
# ======================================================================
model_transect = mt_model.extract_transect(xq, yq, t, item_number=mt_model_item_number)
model_ssc_ts   = np.asarray(model_transect[0], dtype=float) * 1000.0
adcp_series    = adcp.get_beam_series(field_name=adcp_series_field, mode=adcp_series_mode, target=adcp_series_target)
adcp_ssc_ts    = np.asarray(adcp_series[0], dtype=float)
dist_m         = np.asarray(adcp.position.distance, dtype=float).ravel()

n = min(dist_m.size, model_ssc_ts.size, adcp_ssc_ts.size)
dist_m, model_ssc_ts, adcp_ssc_ts = dist_m[:n], model_ssc_ts[:n], adcp_ssc_ts[:n]
valid = np.isfinite(dist_m) & np.isfinite(model_ssc_ts) & np.isfinite(adcp_ssc_ts)
dist_m, model_ssc_ts, adcp_ssc_ts = dist_m[valid], model_ssc_ts[valid], adcp_ssc_ts[valid]
if dist_m.size == 0:
    raise ValueError("No valid samples for distance binning.")

dmax   = float(np.nanmax(dist_m))
edges  = np.arange(0.0, dmax + distance_bin_m, distance_bin_m)
if edges.size < 2:
    edges = np.array([0.0, max(distance_bin_m, dmax if np.isfinite(dmax) else distance_bin_m)], dtype=float)
centers = 0.5 * (edges[:-1] + edges[1:]); nbins = edges.size - 1
bin_idx = np.clip(np.digitize(dist_m, edges) - 1, 0, nbins - 1)

def binned_mean(values: np.ndarray, idx: np.ndarray, nb: int) -> np.ndarray:
    sums = np.bincount(idx, weights=values, minlength=nb).astype(float)
    cnts = np.bincount(idx, minlength=nb).astype(float)
    out  = np.full(nb, np.nan, dtype=float); ok = cnts > 0
    out[ok] = sums[ok] / cnts[ok]; return out

model_bin_mean = binned_mean(model_ssc_ts, bin_idx, nbins)
adcp_bin_mean  = binned_mean(adcp_ssc_ts,  bin_idx, nbins)

bar_w = max(0.5, distance_bin_m * bar_width_scale)
if scale.lower() == "log":
    m_plot = np.where(np.isfinite(model_bin_mean) & (model_bin_mean > 0), model_bin_mean, np.nan)
    a_plot = np.where(np.isfinite(adcp_bin_mean)  & (adcp_bin_mean  > 0), adcp_bin_mean,  np.nan)
    m_plot = np.where(m_plot < cbar_min, cbar_min, m_plot)
    a_plot = np.where(a_plot < cbar_min, cbar_min, a_plot)
else:
    m_plot = model_bin_mean; a_plot = adcp_bin_mean

ax1.bar(centers - bar_w/2, m_plot, width=bar_w, color=PlottingShell.blue1, alpha=0.9, label="Model", align="center")
ax1.bar(centers + bar_w/2, a_plot,  width=bar_w, color=PlottingShell.red1,  alpha=0.9, label="ADCP",  align="center")

ax1.set_xlim(edges[0], edges[-1])
ax1.set_xlabel("Distance along transect (m)")
ax1.set_ylabel("Mean SSC (mg/L)")
ax1.set_title("SSC by distance bin")
ax1.grid(alpha=0.3); ax1.legend(frameon=False, fontsize=7)

ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, pos: f"{v:.1f}"))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, pos: f"{v:.{tick_decimal_precision}f}"))

ax1.set_box_aspect(1); ax1.set_anchor("C")
if scale.lower() == "log":
    ax1.set_yscale("log")
    ymin = cbar_min
    ymax = np.nanmax([np.nanmax(m_plot), np.nanmax(a_plot)])
    if np.isfinite(ymax) and ymax > ymin:
        ax1.set_ylim(ymin, ymax * 1.4)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, pos: f"{v:.{tick_decimal_precision}f}"))

# ======================================================================
# BOTTOM — Metadata (three columns)
# ======================================================================
t_arr = np.asarray(t)[:n]; t_valid = t_arr[valid]
t0 = pd.to_datetime(t_valid.min()); t1 = pd.to_datetime(t_valid.max())
dur_min = (t1 - t0).total_seconds() / 60.0
mean_model = float(np.nanmean(model_ssc_ts[:n][valid]))
mean_obs   = float(np.nanmean(adcp_ssc_ts[:n][valid]))
mean_err   = float(np.nanmean(model_ssc_ts[:n][valid] - adcp_ssc_ts[:n][valid]))

ax2.clear(); ax2.set_axis_off()
fmt_time = lambda dt: dt.strftime("%d %b. %Y %H:%M")
def H(x, y, text): ax2.text(x, y, text, ha="left", va="top", fontsize=8, fontweight="bold", family="monospace")
def I(x, y, k, v): ax2.text(x+0.02, y, f"{k}: {v}", ha="left", va="top", fontsize=7, family="monospace")

y0 = 0.92; dy = 0.12; cols_x = [0.02, 0.36, 0.70]

x = cols_x[0]; y = y0
H(x, y, "Observation Aggregation"); y -= dy
I(x, y, "Field",  adcp_series_field); y -= dy*0.8
I(x, y, "Mode",   adcp_series_mode);  y -= dy*0.8
I(x, y, "Target", adcp_series_target)

x = cols_x[1]; y = y0
H(x, y, "Transect Timing"); y -= dy
I(x, y, "Start",   fmt_time(t0)); y -= dy*0.8
I(x, y, "End",     fmt_time(t1)); y -= dy*0.8
I(x, y, "Duration", f"{dur_min:.1f} min")

x = cols_x[2]; y = y0
H(x, y, "Model Fit"); y -= dy
I(x, y, "Mean error",     f"{mean_err:.{tick_decimals}f} mg/L"); y -= dy*0.8
I(x, y, "Mean observed",  f"{mean_obs:.{tick_decimals}f} mg/L"); y -= dy*0.8
I(x, y, "Mean simulated", f"{mean_model:.{tick_decimals}f} mg/L")
