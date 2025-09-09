# -*- coding: utf-8 -*-
"""
TransectViewer3D: Plot 3D ADCP curtain transects in Plotly with optional
shapefile overlays (lines/polygons/points), lat/lon graticules, and a
dynamic north arrow. Accepts a single configuration dictionary.

Key features
------------
- XY aspect = 1:1 (meters). Z optionally exaggerated via `zscale`.
- Domain clipped to ADCP lon/lat extent with ±`pad_deg` (degrees).
- Axes show degrees; geometry rendered in meters.
- Equal-spacing graticule across the full padded domain at z = 0.
- Surfaces built from ADCP beam-mean values (axis=2). NaNs transparent.
- Hover: survey name, transect name, start/end times, lon, lat.
- Colorbar bottom-right, compact, contrast-aware text.
- North arrow overlay. North = +latitude direction.
- Shapefile overlays:
    * type: "auto" | "line" | "polygon" | "point"
    * lines/polygons: color, width, optional label text
    * points: color, markersize, optional per-point text via column or constant

Inputs (dict)
-------------
Required
- xml: str (path to project file)
- surveys: list[str] (survey names to load)

Optional
- shp: list[dict|str]  (see "Shapefile styling" below)
- cmap: str, default "jet"
- field_name: str in {
    "absolute_backscatter",
    "echo_intensity",
    "correlation_magnitude",
    "suspended_solids_concentration"
  }
- vmin, vmax: float | None (color limits)
- zscale: float, default 1.0 (vertical exaggeration factor)
- pad_deg: float, default 0.05 (domain padding in degrees)
- grid_lines: int, default 9 (graticule lines per axis)
- bgcolor: str, default "black"
- axis_ticks: int, default 7 (degree ticks per axis)
- tick_fontsize: int, default 10 (numeric tick labels)
- tick_decimals: int, default 4 (lon/lat tick formatting)
- axis_label_fontsize: int, default 12
- axis_label_color: str | None, default auto-contrast
- hover_fontsize: int | None, default ~25% smaller than ticks
- out: str | None (HTML output path)

Shapefile styling (per-entry dict)
----------------------------------
Common
- path: str (required)
- type: "auto" | "line" | "polygon" | "point"  (default "auto")

Line/Polygon
- color: "#RRGGBB", default "#00FFAA"
- width: int, default 2
- label: str | None, default None
- label_fontsize: int, default 12
- label_color: "#RRGGBB", default "#ffffff"

Point/MultiPoint
- color: "#RRGGBB", default "#00FFAA"
- markersize: int|float, default 6
- text_attr: str | None  (column to use for text)
- label: str | None      (constant text if text_attr not provided)
- label_fontsize: int, default 12
- label_color: "#RRGGBB", default "#ffffff"
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Project imports (assumes this file lives under /backend or similar)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils_xml import XMLUtils          # noqa: E402
from adcp import ADCP as ADCPDataset    # noqa: E402

# Use system browser by default
pio.renderers.default = "browser"


class TransectViewer3D:
    """
    Build and render a 3D interactive ADCP transect viewer in Plotly.

    Usage
    -----
    viewer = TransectViewer3D(config_dict)
    fig = viewer.render()             # returns plotly Figure
    viewer.save_html()                # writes HTML with north arrow overlay
    """

    # ---------- Construction ----------

    def __init__(self, inputs: Dict[str, Any]) -> None:
        """Store configuration, load ADCP datasets, and map survey names."""
        self.cfg = dict(inputs)  # shallow copy

        # Load ADCP sets from XML and surveys.
        xml_path = self.cfg["xml"]
        surveys = self.cfg.get("surveys", [])
        if not surveys:
            raise ValueError("`surveys` must be a non-empty list of survey names.")

        project = XMLUtils(xml_path)

        adcp_entries: List[Tuple[str, Dict[str, Any]]] = []
        for svy in surveys:
            for acfg in project.get_survey_adcp_cfgs(svy):
                if acfg:
                    adcp_entries.append((svy, acfg))

        self.adcps: List[ADCPDataset] = []
        self.survey_by_name: Dict[str, str] = {}
        for svy, acfg in adcp_entries:
            adcp = ADCPDataset(acfg, name=acfg["name"])
            self.adcps.append(adcp)
            self.survey_by_name[str(adcp.name)] = svy

        # Will be populated by build step
        self.frame: Dict[str, float] = {}
        self.zmin_true: float = 0.0
        self.zmax_true: float = 0.0
        self.zmin_scaled: float = 0.0
        self.zmax_scaled: float = 0.0

        # Figure handle
        self.fig: go.Figure | None = None

    # ---------- Geometry helpers ----------

    @staticmethod
    def _meters_per_degree(lat_deg: float) -> Tuple[float, float]:
        """Approximate meters per degree lon/lat at the given latitude."""
        lat = np.deg2rad(lat_deg)
        m_per_deg_lat = 111_132.92 - 559.82 * np.cos(2 * lat) + 1.175 * np.cos(4 * lat)
        m_per_deg_lon = 111_412.84 * np.cos(lat) - 93.5 * np.cos(3 * lat)
        return float(m_per_deg_lon), float(m_per_deg_lat)

    def _global_frame_from_adcps(self) -> Tuple[float, float, float, float]:
        """Return lon0, lat0, m_per_deg_lon, m_per_deg_lat for the ADCP set."""
        lon = np.concatenate(
            [np.asarray(a.position.x, float).ravel() for a in self.adcps if np.size(a.position.x)]
        )
        lat = np.concatenate(
            [np.asarray(a.position.y, float).ravel() for a in self.adcps if np.size(a.position.y)]
        )
        if lon.size == 0 or lat.size == 0:
            raise ValueError("No positions found in ADCP datasets.")

        lon0 = float(np.nanmedian(lon))
        lat0 = float(np.nanmedian(lat))
        m_per_deg_lon, m_per_deg_lat = self._meters_per_degree(lat0)
        return lon0, lat0, m_per_deg_lon, m_per_deg_lat

    @staticmethod
    def _font_color_for_bg(bg_color: str) -> str:
        """Choose white text for dark bg, else black."""
        c = (bg_color or "").strip().lower().replace(" ", "")
        return "#ffffff" if c in ("black", "#000", "#000000", "rgb(0,0,0)") else "#000000"

    @staticmethod
    def _format_field_label(field: str) -> str:
        """Readable colorbar title with units."""
        mapping = {
            "absolute_backscatter": "Absolute Backscatter (dB)",
            "echo_intensity": "Echo Intensity (Counts)",
            "correlation_magnitude": "Correlation Magnitude (Counts)",
            "suspended_solids_concentration": "Suspended Solids Concentration (mg/L)",
        }
        return mapping.get(field, field.replace("_", " ").title())

    @staticmethod
    def _time_bounds(adcp: ADCPDataset) -> Tuple[str, str]:
        """Start/end timestamps from adcp.time.ensemble_datetimes."""
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

    # ---------- Build core surfaces ----------

    def _build_curtain_surfaces(self) -> go.Figure:
        """
        Build the surface traces for each ADCP transect and configure
        the base layout (no axes ranges yet). Stores frame and z-ranges.
        """
        field = self.cfg.get("field_name", "absolute_backscatter")
        cmap = self.cfg.get("cmap", "jet")
        vmin = self.cfg.get("vmin", None)
        vmax = self.cfg.get("vmax", None)
        zscale = float(self.cfg.get("zscale", 1.0))
        bg_color = self.cfg.get("bgcolor", "black")
        hover_fontsize = self.cfg.get("hover_fontsize", None)

        lon0, lat0, m_per_deg_lon, m_per_deg_lat = self._global_frame_from_adcps()
        self.frame = dict(
            lon0=lon0,
            lat0=lat0,
            m_per_deg_lon=m_per_deg_lon,
            m_per_deg_lat=m_per_deg_lat,
        )

        traces: List[go.Surface] = []
        pool_vals: List[np.ndarray] = []
        z_true_all: List[np.ndarray] = []
        z_scaled_all: List[np.ndarray] = []

        for adcp in self.adcps:
            lon = np.asarray(adcp.position.x, float).ravel()
            lat = np.asarray(adcp.position.y, float).ravel()
            relz = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, float)  # (t,b,beam)
            vals = np.asarray(adcp.get_beam_data(field_name=field, mask=True), float)  # (t,b,beam)

            if relz.shape != vals.shape:
                raise ValueError(
                    f"{getattr(adcp, 'name', 'ADCP')}: relz {relz.shape} != values {vals.shape}"
                )

            n = min(lon.size, lat.size, vals.shape[0])
            lon, lat, relz, vals = lon[:n], lat[:n], relz[:n], vals[:n]

            v_mean = np.nanmean(vals, axis=2)      # (t,b)
            z_true = np.nanmean(relz, axis=2)      # (t,b), meters, negative down
            z_plot = z_true * zscale                # scaled for vertical exaggeration

            nb = v_mean.shape[1]
            x_m = (lon - lon0) * m_per_deg_lon
            y_m = (lat - lat0) * m_per_deg_lat

            X = np.tile(x_m, (nb, 1))              # (b,t)
            Y = np.tile(y_m, (nb, 1))              # (b,t)
            C = v_mean.T                            # (b,t)
            ZZ_plot = z_plot.T                      # (b,t)
            ZZ_true = z_true.T                      # (b,t)

            # Mask NaNs by color field
            mask = ~np.isfinite(C)
            C = C.astype(float)
            ZZ_plot = ZZ_plot.astype(float)
            ZZ_true = ZZ_true.astype(float)
            C[mask] = np.nan
            ZZ_plot[mask] = np.nan
            ZZ_true[mask] = np.nan

            # Hover: survey, transect name, time bounds, lon, lat
            Lon_deg = (X / m_per_deg_lon) + lon0
            Lat_deg = (Y / m_per_deg_lat) + lat0
            custom = np.stack([Lon_deg, Lat_deg], axis=-1)  # (b,t,2)

            start_str, end_str = self._time_bounds(adcp)
            tr_name = str(getattr(adcp, "name", "transect"))
            svy_name = str(self.survey_by_name.get(tr_name, "n/a"))

            traces.append(
                go.Surface(
                    x=X,
                    y=Y,
                    z=ZZ_plot,            # plot-scaled geometry
                    surfacecolor=C,
                    customdata=custom,
                    colorscale=cmap,
                    opacity=0.95,
                    showscale=False,
                    name=tr_name,
                    meta=dict(
                        transect=tr_name,
                        start=start_str,
                        end=end_str,
                        survey=svy_name,
                    ),
                    hovertemplate=(
                        "<b>%{meta.transect}</b><br>"
                        "survey: %{meta.survey}<br>"
                        "start: %{meta.start}<br>"
                        "end: %{meta.end}<br>"
                        "lon = %{customdata[0]:.5f}°<br>"
                        "lat = %{customdata[1]:.5f}°"
                        "<extra></extra>"
                    ),
                )
            )

            valid = C[~np.isnan(C)]
            if valid.size:
                pool_vals.append(valid)
            z_true_all.append(ZZ_true[~np.isnan(ZZ_true)])
            z_scaled_all.append(ZZ_plot[~np.isnan(ZZ_plot)])

        # Color limits
        if vmin is None or vmax is None:
            if pool_vals:
                pool_flat = np.concatenate(pool_vals)
                cmin, cmax = float(np.nanmin(pool_flat)), float(np.nanmax(pool_flat))
            else:
                cmin, cmax = 0.0, 1.0
        else:
            cmin, cmax = float(vmin), float(vmax)

        # Apply common colorbar to first trace
        label_text = self._format_field_label(field)
        font_col = self._font_color_for_bg(bg_color)

        for i, tr in enumerate(traces):
            tr.update(cmin=cmin, cmax=cmax, showscale=(i == 0))
            if i == 0:
                tr.update(
                    colorbar=dict(
                        title=dict(text=label_text, side="right", font=dict(color=font_col)),
                        thickness=15,
                        len=0.33,
                        x=1.02,
                        xanchor="left",
                        y=0.02,
                        yanchor="bottom",
                        bgcolor=bg_color,
                        outlinecolor="#777",
                        tickcolor=font_col,
                        tickfont=dict(color=font_col),
                        ticklen=4,
                        tickwidth=1,
                    )
                )

        # Ranges
        z_true_all = np.concatenate(z_true_all) if z_true_all else np.array([0.0])
        z_scaled_all = np.concatenate(z_scaled_all) if z_scaled_all else np.array([0.0])
        self.zmin_true = min(float(np.nanmin(z_true_all)), 0.0)
        self.zmax_true = max(float(np.nanmax(z_true_all)), 0.0)
        self.zmin_scaled = min(float(np.nanmin(z_scaled_all)), 0.0)
        self.zmax_scaled = max(float(np.nanmax(z_scaled_all)), 0.0)

        # Base figure and layout (ranges set later)
        if hover_fontsize is None:
            hover_fontsize = max(7, int(self.cfg.get("tick_fontsize", 10) * 0.9))

        hover_font_color = font_col
        hover_bg = "rgba(0,0,0,0.7)" if font_col == "#ffffff" else "rgba(255,255,255,0.9)"

        fig = go.Figure(data=traces)
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    title=dict(text="Longitude (°)", font=dict(color=font_col)),
                    backgroundcolor=bg_color,
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(color=font_col),
                ),
                yaxis=dict(
                    title=dict(text="Latitude (°)", font=dict(color=font_col)),
                    backgroundcolor=bg_color,
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(color=font_col),
                ),
                zaxis=dict(
                    title=dict(text="Depth (m)", font=dict(color=font_col)),
                    backgroundcolor=bg_color,
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    tickfont=dict(color=font_col),
                ),
            ),
            hoverlabel=dict(font=dict(size=hover_fontsize, color=hover_font_color), bgcolor=hover_bg),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            margin=dict(l=0, r=0, t=30, b=0),
            template=None,
        )

        return fig

    # ---------- Shapefile overlays ----------

    def _add_shapefiles(self, fig: go.Figure) -> go.Figure:
        """
        Add shapefile layers at z = 0.
        Supports "auto", "line", "polygon", "point" types with per-layer styling.
        """
        shp_inputs = self.cfg.get("shp", [])
        if not shp_inputs:
            return fig

        # Lazy imports to keep module load light
        import geopandas as gpd
        from shapely.geometry import (
            LineString,
            MultiLineString,
            Polygon,
            MultiPolygon,
            Point,
            MultiPoint,
        )

        lon0 = self.frame["lon0"]
        lat0 = self.frame["lat0"]
        m_per_deg_lon = self.frame["m_per_deg_lon"]
        m_per_deg_lat = self.frame["m_per_deg_lat"]

        def to_cfg(item: Any) -> Dict[str, Any]:
            if isinstance(item, str):
                return dict(
                    path=item,
                    type="auto",
                    color="#00FFAA",
                    width=2,
                    label=None,
                    label_fontsize=12,
                    label_color="#ffffff",
                    markersize=6,
                    text_attr=None,
                )
            base = dict(
                type="auto",
                color="#00FFAA",
                width=2,
                label=None,
                label_fontsize=12,
                label_color="#ffffff",
                markersize=6,
                text_attr=None,
            )
            base.update(item)
            return base

        def add_linestring(xs: Iterable[float], ys: Iterable[float], color: str, width: int) -> None:
            xs = np.asarray(xs, float)
            ys = np.asarray(ys, float)
            x_m = (xs - lon0) * m_per_deg_lon
            y_m = (ys - lat0) * m_per_deg_lat
            fig.add_trace(
                go.Scatter3d(
                    x=x_m,
                    y=y_m,
                    z=np.zeros_like(x_m),
                    mode="lines",
                    line=dict(color=color, width=int(width)),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        def add_points(
            xs: Iterable[float],
            ys: Iterable[float],
            color: str,
            size: float,
            texts: List[str] | None,
            tcolor: str,
            tsize: int,
        ) -> None:
            xs = np.asarray(xs, float)
            ys = np.asarray(ys, float)
            x_m = (xs - lon0) * m_per_deg_lon
            y_m = (ys - lat0) * m_per_deg_lat
            kwargs: Dict[str, Any] = dict(
                x=x_m,
                y=y_m,
                z=np.zeros_like(x_m),
                mode="markers+text" if texts is not None else "markers",
                marker=dict(size=float(size), color=color),
                showlegend=False,
                hoverinfo="skip",
            )
            if texts is not None:
                kwargs["text"] = texts
                kwargs["textfont"] = dict(size=int(tsize), color=tcolor)
            fig.add_trace(go.Scatter3d(**kwargs))

        for item in shp_inputs:
            cfg = to_cfg(item)

            path = cfg["path"]
            layer_type = str(cfg.get("type", "auto")).lower()
            color = cfg.get("color", "#00FFAA")
            width = int(cfg.get("width", 2))
            label = cfg.get("label")
            lab_size = int(cfg.get("label_fontsize", 12))
            lab_color = cfg.get("label_color", "#ffffff")
            markersize = cfg.get("markersize", 6)
            text_attr = cfg.get("text_attr")

            gdf = gpd.read_file(path)
            if gdf.crs is None:
                raise ValueError(f"{path}: CRS undefined. Reproject to EPSG:4326.")
            gdf = gdf.to_crs("EPSG:4326")

            # Auto-detect geometry type
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
                        xs, ys = geom.xy
                        add_linestring(xs, ys, color, width)
                    elif isinstance(geom, MultiLineString):
                        for part in geom.geoms:
                            xs, ys = part.xy
                            add_linestring(xs, ys, color, width)
                    elif isinstance(geom, Polygon):
                        xs, ys = geom.exterior.xy
                        add_linestring(xs, ys, color, width)
                    elif isinstance(geom, MultiPolygon):
                        for pg in geom.geoms:
                            xs, ys = pg.exterior.xy
                            add_linestring(xs, ys, color, width)

                # Optional label at layer bbox center
                if label:
                    minx, miny, maxx, maxy = gdf.total_bounds
                    cx, cy = 0.5 * (minx + maxx), 0.5 * (miny + maxy)
                    add_points([cx], [cy], color, 0, [label], lab_color, lab_size)

            elif layer_type == "point":
                x_all: List[float] = []
                y_all: List[float] = []
                texts: List[str] = []
                has_text = False

                for idx, geom in enumerate(gdf.geometry):
                    if geom is None or geom.is_empty:
                        continue

                    coords: List[Tuple[float, float]] = []
                    if isinstance(geom, Point):
                        coords = [(geom.x, geom.y)]
                    elif isinstance(geom, MultiPoint):
                        coords = [(p.x, p.y) for p in geom.geoms]
                    else:
                        continue

                    # Per-point text
                    if text_attr and text_attr in gdf.columns:
                        txt_val = str(gdf.iloc[idx][text_attr])
                        texts.extend([txt_val] * len(coords))
                        has_text = True
                    elif label:
                        texts.extend([str(label)] * len(coords))
                        has_text = True
                    else:
                        texts.extend([None] * len(coords))

                    for x, y in coords:
                        x_all.append(x)
                        y_all.append(y)

                texts_array = np.array(texts, dtype=object)
                if not has_text:
                    texts_array = None
                add_points(x_all, y_all, color, markersize, texts_array, lab_color, lab_size)

            else:
                raise ValueError(f"Unsupported layer type: {layer_type}")

        return fig

    # ---------- Graticule ----------

    def _add_graticule_equal(
        self,
        fig: go.Figure,
        lon_min_deg: float,
        lon_max_deg: float,
        lat_min_deg: float,
        lat_max_deg: float,
        xr_m: tuple[float, float],
        yr_m: tuple[float, float],
        color: str = "#333",
        width: int = 1,
        opacity: float = 0.35,
        n_lines: int = 9,
    ) -> go.Figure:
        lon0 = self.frame["lon0"]; lat0 = self.frame["lat0"]
        m_per_deg_lon = self.frame["m_per_deg_lon"]; m_per_deg_lat = self.frame["m_per_deg_lat"]
    
        lon_vals = np.linspace(lon_min_deg, lon_max_deg, n_lines)
        lat_vals = np.linspace(lat_min_deg, lat_max_deg, n_lines)
        z0 = 0.0
    
        y0_m, y1_m = yr_m
        for LON in lon_vals:
            x_m = (LON - lon0) * m_per_deg_lon
            fig.add_trace(go.Scatter3d(
                x=[x_m, x_m], y=[y0_m, y1_m], z=[z0, z0],
                mode="lines",
                line=dict(color=color, width=int(width)),
                opacity=float(opacity),
                showlegend=False, hoverinfo="skip",
            ))
    
        x0_m, x1_m = xr_m
        for LAT in lat_vals:
            y_m = (LAT - lat0) * m_per_deg_lat
            fig.add_trace(go.Scatter3d(
                x=[x0_m, x1_m], y=[y_m, y_m], z=[z0, z0],
                mode="lines",
                line=dict(color=color, width=int(width)),
                opacity=float(opacity),
                showlegend=False, hoverinfo="skip",
            ))
        return fig


    # ---------- Camera and layout ranges ----------

    def _apply_axes_camera_and_grids(self, fig: go.Figure) -> go.Figure:
        """Set axis ranges, ticks, aspect, camera, and add graticules."""
        pad_deg = float(self.cfg.get("pad_deg", 0.05))
        grid_lines = int(self.cfg.get("grid_lines", 9))
        bgcolor = self.cfg.get("bgcolor", "black")

        # XY limits from all ADCP positions with pad (degrees)
        lon_all = np.concatenate(
            [np.asarray(a.position.x, float).ravel() for a in self.adcps if np.size(a.position.x)]
        )
        lat_all = np.concatenate(
            [np.asarray(a.position.y, float).ravel() for a in self.adcps if np.size(a.position.y)]
        )
        lon_min_deg = float(np.nanmin(lon_all)) - pad_deg
        lon_max_deg = float(np.nanmax(lon_all)) + pad_deg
        lat_min_deg = float(np.nanmin(lat_all)) - pad_deg
        lat_max_deg = float(np.nanmax(lat_all)) + pad_deg

        lon0 = self.frame["lon0"]
        lat0 = self.frame["lat0"]
        m_per_deg_lon = self.frame["m_per_deg_lon"]
        m_per_deg_lat = self.frame["m_per_deg_lat"]

        xr = np.array(
            [(lon_min_deg - lon0) * m_per_deg_lon, (lon_max_deg - lon0) * m_per_deg_lon],
            float,
        )
        yr = np.array(
            [(lat_min_deg - lat0) * m_per_deg_lat, (lat_max_deg - lat0) * m_per_deg_lat],
            float,
        )

        # Aspect ratio: x=y=1, z relative to scaled span
        dx = float(xr[1] - xr[0])
        dy = float(yr[1] - yr[0])
        span_xy = max(dx, dy) if max(dx, dy) > 0 else 1.0
        dz_scaled = float(self.zmax_scaled - self.zmin_scaled)
        z_ratio = dz_scaled / span_xy if span_xy > 0 else 1.0

        # Degree ticks and formatting
        nt = max(2, int(self.cfg.get("axis_ticks", 7)))
        x_tickvals = np.linspace(xr[0], xr[1], nt)
        y_tickvals = np.linspace(yr[0], yr[1], nt)
        dec = int(self.cfg.get("tick_decimals", 4))
        x_ticktext = [
            f"{lon_min_deg + (lon_max_deg - lon_min_deg) * i / (nt - 1):.{dec}f}" for i in range(nt)
        ]
        y_ticktext = [
            f"{lat_min_deg + (lat_max_deg - lat_min_deg) * i / (nt - 1):.{dec}f}" for i in range(nt)
        ]

        font_col = self._font_color_for_bg(bgcolor)
        axis_label_color = self.cfg.get("axis_label_color", font_col)
        axis_label_fontsize = int(self.cfg.get("axis_label_fontsize", 12))
        tick_fontsize = int(self.cfg.get("tick_fontsize", 10))

        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    range=[xr[0], xr[1]],
                    tickmode="array",
                    tickvals=x_tickvals.tolist(),
                    ticktext=x_ticktext,
                    title=dict(text="Longitude (°)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                    tickfont=dict(color=font_col, size=tick_fontsize),
                    backgroundcolor=bgcolor,
                    showgrid=False,
                    zeroline=False,
                ),
                yaxis=dict(
                    range=[yr[0], yr[1]],
                    tickmode="array",
                    tickvals=y_tickvals.tolist(),
                    ticktext=y_ticktext,
                    title=dict(text="Latitude (°)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                    tickfont=dict(color=font_col, size=tick_fontsize),
                    backgroundcolor=bgcolor,
                    showgrid=False,
                    zeroline=False,
                ),
                zaxis=dict(
                    range=[self.zmin_scaled, self.zmax_scaled],
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    title=dict(text="Depth (m)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                    tickfont=dict(color=font_col, size=tick_fontsize),
                    backgroundcolor=bgcolor,
                ),
                aspectmode="manual",
                aspectratio=dict(x=1, y=1, z=z_ratio),
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=0.0, y=-0.45, z=0.22),  # look north by default
                ),
            ),
            paper_bgcolor=bgcolor,
            plot_bgcolor=bgcolor,
            uirevision="lock_ranges",
        )

        grid_opacity = float(self.cfg.get("grid_opacity", 0.35))
        grid_color   = self.cfg.get("grid_color", "#333")
        grid_width   = int(self.cfg.get("grid_width", 1))
        
        fig = self._add_graticule_equal(
            fig,
            lon_min_deg, lon_max_deg, lat_min_deg, lat_max_deg,
            xr_m=(xr[0], xr[1]), yr_m=(yr[0], yr[1]),
            color=grid_color, width=grid_width, opacity=grid_opacity,
            n_lines=int(self.cfg.get("grid_lines", 9)),
        )

        return fig

    # ---------- Public API ----------

    def render(self) -> go.Figure:
        """
        Build figure with surfaces, shapefiles, axes, camera,
        graticules, and return a ready-to-show Plotly Figure.
        """
        fig = self._build_curtain_surfaces()
        fig = self._add_shapefiles(fig)
        fig = self._apply_axes_camera_and_grids(fig)
        self.fig = fig
        return fig

    def save_html(self, path: str | None = None, auto_open: bool = False) -> str:
        if self.fig is None:
            raise RuntimeError("Call render() before save_html().")
    
        out_path = path or self.cfg.get("out", None)
        if not out_path:
            raise ValueError("Provide `path` or set `out` in the inputs.")
    
        html = self.fig.to_html(include_plotlyjs="cdn", full_html=True, div_id="plotly-div")
        inj = self._north_arrow_js()
        low = html.lower()
        if "</body>" in low:
            i = low.rfind("</body>")
            html = html[:i] + inj + html[i:]
        else:
            html = html + inj + "</body>"
    
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
    
        if auto_open:
            import webbrowser, pathlib
            webbrowser.open(pathlib.Path(out_path).absolute().as_uri())
    
        return out_path


    # ---------- North arrow overlay ----------

    @staticmethod
    def _north_arrow_js() -> str:
        return r"""
    <script>
    (function(){
      const pad = 75;
      const wrap = document.createElement('div');
      wrap.style.position='fixed';
      wrap.style.top= pad + 'px';
      wrap.style.right= pad + 'px';
      wrap.style.width='56px';
      wrap.style.height='56px';
      wrap.style.zIndex=10000;
      wrap.style.pointerEvents='none';
      wrap.innerHTML = `
        <svg id="northArrow" viewBox="0 0 100 100" width="56" height="56" style="opacity:0.95">
          <g id="arrow" transform="translate(50,50)">
            <polygon points="0,-30 9,10 0,5 -9,10" fill="#ffffff"/>
            <text x="0" y="-34" text-anchor="middle" fill="#ffffff" font-size="14" font-family="Arial">N</text>
          </g>
        </svg>`;
      document.body.appendChild(wrap);
    
      function norm(v){ const n=Math.hypot(v.x||0,v.y||0,v.z||0); return n?{x:(v.x||0)/n,y:(v.y||0)/n,z:(v.z||0)/n}:{x:0,y:0,z:0}; }
      function cross(a,b){ return {x:a.y*b.z-a.z*b.y, y:a.z*b.x-a.x*b.z, z:a.x*b.y-a.y*b.x}; }
      function dot(a,b){ return (a.x*b.x + a.y*b.y + a.z*b.z); }
    
      // Rotate opposite camera roll so arrow always points to world +Y (north = +lat).
      function updateArrow(cam){
        if(!cam || !cam.eye) return;
        const eye = cam.eye, up = cam.up || {x:0,y:0,z:1};
        const v = norm({x:-eye.x, y:-eye.y, z:-eye.z}); // view dir
        const r = norm(cross(v, up));                    // screen-right
        const u = norm(cross(r, v));                     // screen-up
        const Y = {x:0,y:1,z:0};                         // world north
        const px = dot(Y, r);
        const py = dot(Y, u);
        const deg = Math.atan2(px, py) * 180/Math.PI;    // counter-rotate
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



# ---------------- Example ----------------
if __name__ == "__main__":
    inputs = {
        "xml": r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj",
        "surveys": ["Survey 1", "Survey 2"],
        "shp": [
            {
                "path": r"C:/Users/anba/Downloads/v20250509/v20250509/RD7550_CEx_SG_v20250509.shp",
                "type": "line",
                "color": "limegreen",
                "width": 2,
            },
            {
                "path": r"C:/Users/anba/Downloads/v20250509/v20250509/points_labels.shp",
                "type": "point",
                "color": "#FFD166",
                "markersize": 6,
                "label": "Source Location",
                "label_fontsize": 11,
                "label_color": "pink",
            },
        ],
        "cmap": "jet",
        "field_name": "absolute_backscatter",
        "vmin": None,
        "vmax": None,
        "pad_deg": 0.03,
        "grid_lines": 10,
        "grid_opacity": 0.35,
        "grid_color": "#333",
        "grid_width": 1,
        "bgcolor": "black",
        "axis_ticks": 5,
        "tick_fontsize": 10,
        "tick_decimals": 4,
        "axis_label_fontsize": 12,
        "axis_label_color": "#cccccc",
        "hover_fontsize": 9,
        
        "out": r"C:\Users\anba\OneDrive - DHI\Desktop\Documents\GitHub\PlumeTrack\backend\adcp_curtains.html",
        "zscale": 3.0,          # vertical exaggeration
        
    }

    viewer = TransectViewer3D(inputs)
    fig = viewer.render()
    # Save HTML with north arrow overlay
    viewer.save_html(auto_open=False)
    # Or just show in a browser tab:
    # fig.show()
