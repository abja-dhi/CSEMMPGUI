# -*- coding: utf-8 -*-
"""
3D ADCP curtain plots with optional shapefile overlay at z=0.

- XY aspect = 1:1. Z scaled to data span; hover omits depth.
- View clipped to ADCP lon/lat extent with ±pad_deg.
- Axes show degrees (ticks), geometry in meters.
- Equal-spacing lat/lon graticule over final padded view at z=0.
- Hover: survey, transect name, start/end times, lon, lat.
- Shapefile lines at z=0 with per-file color/width and optional labels.
- Colorbar bottom-right, smaller, contrast-aware text.
- North arrow top-right. North = +latitude.
"""

import sys, os
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import geopandas as gpd
from shapely.geometry import LineString, Polygon, MultiLineString, MultiPolygon

# ---- project imports ----
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils_xml import XMLUtils
from adcp import ADCP as ADCPDataset

pio.renderers.default = "browser"

# ---------------- helpers ----------------
def meters_per_degree(lat_deg: float) -> tuple[float, float]:
    lat = np.deg2rad(lat_deg)
    m_per_deg_lat = 111_132.92 - 559.82*np.cos(2*lat) + 1.175*np.cos(4*lat)
    m_per_deg_lon = 111_412.84*np.cos(lat) - 93.5*np.cos(3*lat)
    return float(m_per_deg_lon), float(m_per_deg_lat)

def global_frame_from_adcps(adcps):
    lon = np.concatenate([np.asarray(a.position.x, float).ravel() for a in adcps if np.size(a.position.x)])
    lat = np.concatenate([np.asarray(a.position.y, float).ravel() for a in adcps if np.size(a.position.y)])
    if lon.size == 0 or lat.size == 0:
        raise ValueError("No positions found in ADCPs.")
    lon0 = float(np.nanmedian(lon))
    lat0 = float(np.nanmedian(lat))
    m_per_deg_lon, m_per_deg_lat = meters_per_degree(lat0)
    return lon0, lat0, m_per_deg_lon, m_per_deg_lat

def _font_color_for_bg(bg_color: str) -> str:
    c = (bg_color or "").strip().lower().replace(" ", "")
    return "#ffffff" if c in ("black", "#000", "#000000", "rgb(0,0,0)") else "#000000"

# ------------- curtains -------------
def build_curtain_figure(
    adcps,
    field_name="absolute_backscatter",  # absolute_backscatter | echo_intensity | correlation_magnitude | suspended_solids_concentration
    cmap="jet",
    vmin=None,
    vmax=None,
    zscale=1.0,
    bg_color="black",
    survey_by_name=None,        # dict: {adcp.name -> survey name}
    hover_fontsize=None         # int; if None, computed ~25% smaller than tick font
):
    def format_field_label(field: str) -> str:
        mapping = {
            "absolute_backscatter": "Absolute Backscatter (dB)",
            "echo_intensity": "Echo Intensity (Counts)",
            "correlation_magnitude": "Correlation Magnitude (Counts)",
            "suspended_solids_concentration": "Suspended Solids Concentration (mg/L)"
        }
        return mapping.get(field, field.replace("_", " ").title())

    def _time_bounds(adcp):
        """Start/end from adcp.time.ensemble_datetimes (datetime.datetime objects)."""
        try:
            dts = getattr(getattr(adcp, "time", None), "ensemble_datetimes", None)
        except Exception:
            dts = None
        if dts is None:
            return "n/a", "n/a"
        arr = np.array(list(dts), dtype=object).ravel()
        vals = [t for t in arr if t is not None]
        if not vals:
            return "n/a", "n/a"
        start, end = min(vals), max(vals)
        return start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")

    survey_by_name = survey_by_name or {}
    lon0, lat0, m_per_deg_lon, m_per_deg_lat = global_frame_from_adcps(adcps)
    scale = float(zscale) if zscale else 1.0

    traces = []
    pool_vals = []
    z_true_all = []
    z_scaled_all = []

    for adcp in adcps:
        lon = np.asarray(adcp.position.x, float).ravel()
        lat = np.asarray(adcp.position.y, float).ravel()
        relz = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, float)      # (t,b,beam)
        vals = np.asarray(adcp.get_beam_data(field_name=field_name, mask=True), float)  # (t,b,beam)
        if relz.shape != vals.shape:
            raise ValueError(f"{getattr(adcp,'name','ADCP')}: relz {relz.shape} != values {vals.shape}")

        n = min(lon.size, lat.size, vals.shape[0])
        lon, lat, relz, vals = lon[:n], lat[:n], relz[:n], vals[:n]

        V = np.nanmean(vals, axis=2)            # (t,b)
        Z_true = np.nanmean(relz, axis=2)       # (t,b) true meters (negative down)
        Z_plot = Z_true * scale                 # (t,b) scaled for vertical exaggeration

        nb = V.shape[1]
        x_m = (lon - lon0) * m_per_deg_lon
        y_m = (lat - lat0) * m_per_deg_lat
        X = np.tile(x_m, (nb, 1))               # (b,t)
        Y = np.tile(y_m, (nb, 1))               # (b,t)
        C = V.T
        ZZ_plot = Z_plot.T
        ZZ_true = Z_true.T

        mask = ~np.isfinite(C)
        C = C.astype(float); ZZ_plot = ZZ_plot.astype(float); ZZ_true = ZZ_true.astype(float)
        C[mask] = np.nan; ZZ_plot[mask] = np.nan; ZZ_true[mask] = np.nan

        Lon_deg = (X / m_per_deg_lon) + lon0
        Lat_deg = (Y / m_per_deg_lat) + lat0
        custom = np.stack([Lon_deg, Lat_deg], axis=-1)

        start_str, end_str = _time_bounds(adcp)
        tr_name = str(getattr(adcp, "name", "transect"))
        svy_name = str(survey_by_name.get(tr_name, "n/a"))

        traces.append(go.Surface(
            x=X, y=Y, z=ZZ_plot, surfacecolor=C,
            customdata=custom,
            colorscale=cmap,
            opacity=0.95,
            showscale=False,
            name=tr_name,
            meta=dict(transect=tr_name, start=start_str, end=end_str, survey=svy_name),
            hovertemplate=(
                "<b>%{meta.transect}</b><br>"
                "survey: %{meta.survey}<br>"
                "start: %{meta.start}<br>"
                "end: %{meta.end}<br>"
                "lon = %{customdata[0]:.5f}°<br>"
                "lat = %{customdata[1]:.5f}°"
                "<extra></extra>"
            )
        ))

        valid = C[~np.isnan(C)]
        if valid.size:
            pool_vals.append(valid)
        z_true_all.append(ZZ_true[~np.isnan(ZZ_true)])
        z_scaled_all.append(ZZ_plot[~np.isnan(ZZ_plot)])

    # color limits
    if vmin is None or vmax is None:
        if pool_vals:
            pool_flat = np.concatenate(pool_vals)
            cmin, cmax = float(np.nanmin(pool_flat)), float(np.nanmax(pool_flat))
        else:
            cmin, cmax = 0.0, 1.0
    else:
        cmin, cmax = float(vmin), float(vmax)

    font_col = _font_color_for_bg(bg_color)
    label_text = format_field_label(field_name)

    for i, tr in enumerate(traces):
        tr.update(cmin=cmin, cmax=cmax, showscale=(i == 0))
        if i == 0:
            tr.update(colorbar=dict(
                title=dict(text=label_text, side="right", font=dict(color=font_col)),
                thickness=15, len=0.33,
                x=1.02, xanchor="left",
                y=0.02, yanchor="bottom",
                bgcolor=bg_color,
                outlinecolor="#777",
                tickcolor=font_col,
                tickfont=dict(color=font_col),
                ticklen=4, tickwidth=1
            ))

    # ranges to drive layout outside
    z_true_all = np.concatenate(z_true_all) if z_true_all else np.array([0.0])
    z_scaled_all = np.concatenate(z_scaled_all) if z_scaled_all else np.array([0.0])
    zmin_raw  = min(float(np.nanmin(z_true_all)), 0.0)
    zmax_raw  = max(float(np.nanmax(z_true_all)), 0.0)
    zmin_scal = min(float(np.nanmin(z_scaled_all)), 0.0)
    zmax_scal = max(float(np.nanmax(z_scaled_all)), 0.0)

    # hover label styling
    if hover_fontsize is None:
        # default ~25% smaller than a typical 12 px tick label
        hover_fontsize = 9
    hover_font_color = font_col
    hover_bg = "rgba(0,0,0,0.7)" if font_col == "#ffffff" else "rgba(255,255,255,0.9)"

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(text="Longitude (°)", font=dict(color=font_col)),
                backgroundcolor=bg_color, showgrid=False, zeroline=False,
                tickfont=dict(color=font_col)
            ),
            yaxis=dict(
                title=dict(text="Latitude (°)", font=dict(color=font_col)),
                backgroundcolor=bg_color, showgrid=False, zeroline=False,
                tickfont=dict(color=font_col)
            ),
            zaxis=dict(
                title=dict(text="Depth (m)", font=dict(color=font_col)),
                backgroundcolor=bg_color,
                showgrid=False, zeroline=False, showticklabels=False,
                tickfont=dict(color=font_col)
            ),
        ),
        hoverlabel=dict(font=dict(size=hover_fontsize, color=hover_font_color), bgcolor=hover_bg),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(l=0, r=0, t=30, b=0),
        template=None
    )

    frame = dict(lon0=lon0, lat0=lat0, m_per_deg_lon=m_per_deg_lon, m_per_deg_lat=m_per_deg_lat)
    return fig, frame, zmin_raw, zmax_raw, zmin_scal, zmax_scal

# ------------- shapefile overlay -------------
def add_shapefiles_z0(fig, shp_inputs, frame):
    """
    Supports line/polygon and point/multipoint layers.

    shp_inputs: list of str or dicts
      Common keys:
        - path (str) [required]
        - type (str) in {"auto","line","polygon","point"}  default "auto"
      Line/Polygon style:
        - color (str) default "#00FFAA"
        - width (int) default 2
        - label (str|None) default None   # single label for layer
        - label_fontsize (int) default 12
        - label_color (str) default "#ffffff"
      Point style:
        - color (str) default "#00FFAA"
        - markersize (int|float) default 6
        - text_attr (str|None)  # take per-point text from this column
        - label (str|None)      # constant text if text_attr not provided
        - label_fontsize (int) default 12
        - label_color (str) default "#ffffff"
    """
    import geopandas as gpd
    from shapely.geometry import LineString, Polygon, MultiLineString, MultiPolygon, Point, MultiPoint
    import numpy as np
    import plotly.graph_objects as go

    lon0 = frame["lon0"]; lat0 = frame["lat0"]
    m_per_deg_lon = frame["m_per_deg_lon"]; m_per_deg_lat = frame["m_per_deg_lat"]

    def to_cfg(item):
        if isinstance(item, str):
            return dict(path=item, type="auto", color="#00FFAA", width=2,
                        label=None, label_fontsize=12, label_color="#ffffff",
                        markersize=6, text_attr=None)
        base = dict(type="auto", color="#00FFAA", width=2,
                    label=None, label_fontsize=12, label_color="#ffffff",
                    markersize=6, text_attr=None)
        base.update(item)
        return base

    def add_linestring_coords(xs, ys, color, width):
        xs = np.asarray(xs, float); ys = np.asarray(ys, float)
        x_m = (xs - lon0) * m_per_deg_lon
        y_m = (ys - lat0) * m_per_deg_lat
        fig.add_trace(go.Scatter3d(
            x=x_m, y=y_m, z=np.zeros_like(x_m),
            mode="lines",
            line=dict(color=color, width=int(width)),
            showlegend=False, hoverinfo="skip"
        ))

    def add_points_arrays(x_list, y_list, color, size, texts, tcolor, tsize):
        xs = np.asarray(x_list, float); ys = np.asarray(y_list, float)
        x_m = (xs - lon0) * m_per_deg_lon
        y_m = (ys - lat0) * m_per_deg_lat
        kwargs = dict(
            x=x_m, y=y_m, z=np.zeros_like(x_m),
            mode="markers+text" if texts is not None else "markers",
            marker=dict(size=float(size), color=color),
            showlegend=False, hoverinfo="skip"
        )
        if texts is not None:
            kwargs["text"] = texts
            kwargs["textfont"] = dict(size=int(tsize), color=tcolor)
        fig.add_trace(go.Scatter3d(**kwargs))

    for item in shp_inputs:
        cfg = to_cfg(item)
        shp_path = cfg["path"]
        layer_type = str(cfg.get("type", "auto")).lower()
        color = cfg.get("color", "#00FFAA")
        width = cfg.get("width", 2)
        label = cfg.get("label")
        lab_size = int(cfg.get("label_fontsize", 12))
        lab_color = cfg.get("label_color", "#ffffff")
        markersize = cfg.get("markersize", 6)
        text_attr = cfg.get("text_attr")

        gdf = gpd.read_file(shp_path)
        if gdf.crs is None:
            raise ValueError(f"{shp_path}: CRS undefined. Reproject to EPSG:4326.")
        gdf = gdf.to_crs("EPSG:4326")

        # Auto-detect type if requested
        if layer_type == "auto":
            gtypes = set(gdf.geom_type.str.lower())
            if any(t in gtypes for t in ("point", "multipoint")):
                layer_type = "point"
            elif any(t in gtypes for t in ("polygon", "multipolygon")):
                layer_type = "polygon"
            else:
                layer_type = "line"

        if layer_type in ("line", "polygon"):
            for geom in gdf.geometry:
                if geom is None or geom.is_empty:
                    continue
                if isinstance(geom, LineString):
                    xs, ys = geom.xy; add_linestring_coords(xs, ys, color, width)
                elif isinstance(geom, MultiLineString):
                    for part in geom.geoms:
                        xs, ys = part.xy; add_linestring_coords(xs, ys, color, width)
                elif isinstance(geom, Polygon):
                    xs, ys = geom.exterior.xy; add_linestring_coords(xs, ys, color, width)
                elif isinstance(geom, MultiPolygon):
                    for pg in geom.geoms:
                        xs, ys = pg.exterior.xy; add_linestring_coords(xs, ys, color, width)
            # Optional single label at layer centroid
            if label:
                minx, miny, maxx, maxy = gdf.total_bounds
                cx, cy = 0.5*(minx+maxx), 0.5*(miny+maxy)
                add_points_arrays([cx], [cy], color, 0, [label], lab_color, lab_size)

        elif layer_type == "point":
            x_all, y_all, texts = [], [], []
            has_text = False
            for idx, geom in enumerate(gdf.geometry):
                if geom is None or geom.is_empty:
                    continue
                # collect coords
                coords = []
                if isinstance(geom, Point):
                    coords = [(geom.x, geom.y)]
                elif isinstance(geom, MultiPoint):
                    coords = [(p.x, p.y) for p in geom.geoms]
                else:
                    # if a non-point sneaks in, skip it
                    continue

                # assign text per feature
                if text_attr and text_attr in gdf.columns:
                    txt = str(gdf.iloc[idx][text_attr])
                    texts.extend([txt]*len(coords))
                    has_text = True
                elif label:
                    texts.extend([str(label)]*len(coords))
                    has_text = True
                else:
                    texts.extend([None]*len(coords))

                for x, y in coords:
                    x_all.append(x); y_all.append(y)

            texts_array = np.array(texts, dtype=object)
            if not has_text:
                texts_array = None
            add_points_arrays(x_all, y_all, color, markersize, texts_array, lab_color, lab_size)
        else:
            raise ValueError(f"Unsupported layer type: {layer_type}")

    return fig


# ------------- graticule (equal spacing) -------------
def add_graticule_equal(fig, frame, lon_min_deg, lon_max_deg, lat_min_deg, lat_max_deg,
                        xr_m, yr_m, color="#444", width=1, n_lines=9):
    lon0, lat0 = frame["lon0"], frame["lat0"]
    m_per_deg_lon = frame["m_per_deg_lon"]; m_per_deg_lat = frame["m_per_deg_lat"]

    lon_vals = np.linspace(lon_min_deg, lon_max_deg, n_lines)
    lat_vals = np.linspace(lat_min_deg, lat_max_deg, n_lines)
    z0 = 0.0

    y0_m, y1_m = yr_m[0], yr_m[1]
    for LON in lon_vals:
        x_m = (LON - lon0) * m_per_deg_lon
        fig.add_trace(go.Scatter3d(
            x=[x_m, x_m], y=[y0_m, y1_m], z=[z0, z0],
            mode="lines", line=dict(color=color, width=width),
            showlegend=False, hoverinfo="skip"
        ))

    x0_m, x1_m = xr_m[0], xr_m[1]
    for LAT in lat_vals:
        y_m = (LAT - lat0) * m_per_deg_lat
        fig.add_trace(go.Scatter3d(
            x=[x0_m, x1_m], y=[y_m, y_m], z=[z0, z0],
            mode="lines", line=dict(color=color, width=width),
            showlegend=False, hoverinfo="skip"
        ))
    return fig

# ------------- run -------------
if __name__ == "__main__":
    inputs = {
        "xml": r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj",
        "surveys": ["Survey 1", "Survey 2"],

        # Per-shapefile styling and optional label
        "shp": [
            # line/polygon layer
            {
                "path": r"C:/Users/anba/Downloads/v20250509/v20250509/RD7550_CEx_SG_v20250509.shp",
                "type": "line",
                "color": "#00FFAA",
                "width": 2,
                "label": "Channel Centerline",
                "label_fontsize": 13,
                "label_color": "#FFFFFF"
            },
            # point layer
            {
                "path": r"C:/Users/anba/Downloads/v20250509/v20250509/points_labels.shp",
                "type": "point",
                "color": "#FFD166",
                "markersize": 6,
                "text_attr": "name",          # or omit and use constant label:
                "label_fontsize": 11,
                "label_color": "#FFD166"
            }
        ],

        "cmap": "jet",
        "field_name": "absolute_backscatter",  # echo_intensity | correlation_magnitude | suspended_solids_concentration
        "vmin": None,
        "vmax": None,
        "zscale": 3.0,
        "pad_deg": 0.001,
        "grid_lines": 9,
        "bgcolor": "black",
        "axis_ticks": 7,

        # Axis ticks and labels
        "tick_fontsize": 10,           # numeric tick labels font size
        "tick_decimals": 4,            # decimals for lon/lat tick labels
        "axis_label_fontsize": 12,     # axis title font size
        "axis_label_color": "#cccccc", # axis title color

        # Hover label text size (~25% smaller is typical)
        "hover_fontsize": 9,

        "out": r"C:\Users\anba\OneDrive - DHI\Desktop\Documents\GitHub\PlumeTrack\backend\adcp_curtains.html"
    }

    project = XMLUtils(inputs["xml"])

    # collect ADCP configs with survey association
    adcp_entries = []
    for svy in inputs["surveys"]:
        for cfg in project.get_survey_adcp_cfgs(svy):
            adcp_entries.append((svy, cfg))

    # load ADCP datasets and build name->survey map
    adcps = []
    survey_by_name = {}
    for svy, cfg in adcp_entries:
        adcp = ADCPDataset(cfg, name=cfg['name'])
        adcps.append(adcp)
        survey_by_name[str(adcp.name)] = svy

    fig, frame, zmin_raw, zmax_raw, zmin_scal, zmax_scal = build_curtain_figure(
        adcps,
        field_name=inputs["field_name"],
        cmap=inputs["cmap"],
        vmin=inputs["vmin"], vmax=inputs["vmax"],
        zscale=inputs["zscale"],
        bg_color=inputs["bgcolor"],
        survey_by_name=survey_by_name,
        hover_fontsize=inputs.get("hover_fontsize")
    )

    if inputs["shp"]:
        fig = add_shapefiles_z0(fig, inputs["shp"], frame)

    # XY limits from ADCP positions with pad (degrees -> meters)
    lon_all = np.concatenate([np.asarray(a.position.x, float).ravel() for a in adcps if np.size(a.position.x)])
    lat_all = np.concatenate([np.asarray(a.position.y, float).ravel() for a in adcps if np.size(a.position.y)])
    lon_min_deg = float(np.nanmin(lon_all)) - inputs["pad_deg"]
    lon_max_deg = float(np.nanmax(lon_all)) + inputs["pad_deg"]
    lat_min_deg = float(np.nanmin(lat_all)) - inputs["pad_deg"]
    lat_max_deg = float(np.nanmax(lat_all)) + inputs["pad_deg"]

    lon0, lat0 = frame["lon0"], frame["lat0"]
    m_per_deg_lon = frame["m_per_deg_lon"]; m_per_deg_lat = frame["m_per_deg_lat"]
    xr = np.array([(lon_min_deg - lon0) * m_per_deg_lon, (lon_max_deg - lon0) * m_per_deg_lon], float)
    yr = np.array([(lat_min_deg - lat0) * m_per_deg_lat, (lat_max_deg - lat0) * m_per_deg_lat], float)

    # Aspect uses scaled Z span
    dx = float(xr[1] - xr[0]); dy = float(yr[1] - yr[0])
    span_xy = max(dx, dy) if max(dx, dy) > 0 else 1.0
    dz_scaled = float(zmax_scal - zmin_scal)
    z_ratio = dz_scaled / span_xy if span_xy > 0 else 1.0

    # Degree ticks with requested precision and font sizes
    Nt = max(2, int(inputs["axis_ticks"]))
    x_tickvals = np.linspace(xr[0], xr[1], Nt)
    y_tickvals = np.linspace(yr[0], yr[1], Nt)
    d = int(inputs["tick_decimals"])
    x_ticktext = [f"{lon_min_deg + (lon_max_deg - lon_min_deg)*i/(Nt-1):.{d}f}" for i in range(Nt)]
    y_ticktext = [f"{lat_min_deg + (lat_max_deg - lat_min_deg)*i/(Nt-1):.{d}f}" for i in range(Nt)]

    font_col = _font_color_for_bg(inputs["bgcolor"])
    axis_label_color = inputs.get("axis_label_color", font_col)
    axis_label_fontsize = int(inputs.get("axis_label_fontsize", 12))
    tick_fontsize = int(inputs.get("tick_fontsize", 10))

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                range=[xr[0], xr[1]],
                tickmode="array", tickvals=x_tickvals.tolist(), ticktext=x_ticktext,
                title=dict(text="Longitude (°)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                tickfont=dict(color=font_col, size=tick_fontsize),
                backgroundcolor=inputs["bgcolor"], showgrid=False, zeroline=False
            ),
            yaxis=dict(
                range=[yr[0], yr[1]],
                tickmode="array", tickvals=y_tickvals.tolist(), ticktext=y_ticktext,
                title=dict(text="Latitude (°)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                tickfont=dict(color=font_col, size=tick_fontsize),
                backgroundcolor=inputs["bgcolor"], showgrid=False, zeroline=False
            ),
            zaxis=dict(
                range=[zmin_scal, zmax_scal],
                showgrid=False, zeroline=False, showticklabels=False,
                title=dict(text="Depth (m)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                tickfont=dict(color=font_col, size=tick_fontsize),
                backgroundcolor=inputs["bgcolor"]
            ),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=z_ratio),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=0.0, y=-0.45, z=0.22)  # look north
            )
        ),
        paper_bgcolor=inputs["bgcolor"],
        plot_bgcolor=inputs["bgcolor"],
        uirevision="lock_ranges"
    )

    # Graticule across full padded domain
    fig = add_graticule_equal(
        fig, frame,
        lon_min_deg, lon_max_deg, lat_min_deg, lat_max_deg,
        xr_m=(xr[0], xr[1]), yr_m=(yr[0], yr[1]),
        color="#333", width=1, n_lines=inputs["grid_lines"]
    )

    # Write HTML with north arrow overlay
    out_path = inputs["out"]
    html = fig.to_html(include_plotlyjs="cdn", full_html=True, div_id="plotly-div")
    north_js = r"""
<script>
(function(){
  const pad = 56;
  const wrap = document.createElement('div');
  wrap.style.position='fixed';
  wrap.style.top= pad + 'px';
  wrap.style.right= pad + 'px';
  wrap.style.width='56px';
  wrap.style.height='56px';
  wrap.style.zIndex=1000;
  wrap.style.pointerEvents='none';
  wrap.innerHTML = `
    <svg id="northArrow" viewBox="0 0 100 100" width="56" height="56" style="opacity:0.95">
      <circle cx="50" cy="50" r="48" fill="rgba(0,0,0,0.35)" stroke="#aaa" stroke-width="2"/>
      <g id="arrow" transform="translate(50,50)">
        <polygon points="0,-30 9,10 0,5 -9,10" fill="#ffffff"/>
        <text x="0" y="-38" text-anchor="middle" fill="#ffffff" font-size="14" font-family="Arial">N</text>
      </g>
    </svg>`;
  document.body.appendChild(wrap);

  function norm(v){ const n=Math.hypot(v.x||0,v.y||0,v.z||0); return n?{x:(v.x||0)/n,y:(v.y||0)/n,z:(v.z||0)/n}:{x:0,y:0,z:0}; }
  function cross(a,b){ return {x:a.y*b.z-a.z*b.y, y:a.z*b.x-a.x*b.z, z:a.x*b.y-a.y*b.x}; }
  function dot(a,b){ return (a.x*b.x + a.y*b.y + a.z*b.z); }
  function updateArrow(cam){
    if(!cam || !cam.eye) return;
    const eye = cam.eye, up = cam.up || {x:0,y:0,z:1};
    const v = norm({x:-eye.x, y:-eye.y, z:-eye.z});
    const r = norm(cross(v, up));
    const u = norm(cross(r, v));
    const Y = {x:0,y:1,z:0};
    const px = dot(Y, r);
    const py = dot(Y, u);
    const deg = -Math.atan2(px, py) * 180/Math.PI;
    const g = document.getElementById('arrow');
    if (g) g.setAttribute('transform', `translate(50,50) rotate(${deg})`);
  }
  const gd = document.getElementById('plotly-div');
  function currentCam(){
    const L = gd && gd.layout && gd.layout.scene && gd.layout.scene.camera ? gd.layout.scene.camera : {};
    const eye = L.eye || {x:0.0,y:-0.45,z:0.22};
    const up  = L.up  || {x:0,y:0,z:1};
    return {eye:eye, up:up};
  }
  if (gd) {
    updateArrow(currentCam());
    gd.on('plotly_relayout', (ev) => {
      const eye = {
        x: (ev['scene.camera.eye.x'] ?? ev?.['scene.camera']?.eye?.x ?? currentCam().eye.x),
        y: (ev['scene.camera.eye.y'] ?? ev?.['scene.camera']?.eye?.y ?? currentCam().eye.y),
        z: (ev['scene.camera.eye.z'] ?? ev?.['scene.camera']?.eye?.z ?? currentCam().eye.z)
      };
      const up = {
        x: (ev['scene.camera.up.x'] ?? ev?.['scene.camera']?.up?.x ?? 0),
        y: (ev['scene.camera.up.y'] ?? ev?.['scene.camera']?.up?.y ?? 0),
        z: (ev['scene.camera.up.z'] ?? ev?.['scene.camera']?.up?.z ?? 1)
      };
      updateArrow({eye:eye, up:up});
    });
  }
})();
</script>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html.replace("</body>", north_js + "\n</body>"))
    fig.show()
