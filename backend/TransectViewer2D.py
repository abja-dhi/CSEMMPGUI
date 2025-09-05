# -*- coding: utf-8 -*-
"""
TransectViewer2D: Bird's-eye ADCP transect viewer in Plotly.

- XY aspect = 1:1 in meters; ticks labeled in degrees.
- Domain clipped to ADCP lon/lat extent with ±pad_deg.
- Equal-spacing graticule across the full padded domain.
- Transects colored by vertically-aggregated series via ADCP.get_beam_series.
- Hover: survey, transect, start/end times, lon, lat.
- Shapefile overlays: line/polygon/point with styling and labels.
- Static north arrow overlay (points up).
- Colorbar bottom-right, compact, contrast-aware text.

New inputs
----------
- transect_line_width: float (default 3)
- vertical_agg: dict controlling get_beam_series:
    {
      "method": "mean" | "bin" | "range" | "hab",
      "target": int|float|(min,max),      # required except for method="mean"
      "beam": "mean" | int | [int,...],   # default "mean" (1-based)
      "agg": "mean" | float               # "mean" or percentile 0..100
    }

Other inputs mirror your 3D tool (surveys, shp, cmap, field_name, vmin/vmax,
pad_deg, grid_lines, grid_opacity, grid_color, grid_width, bgcolor, axis_ticks,
tick_fontsize, tick_decimals, axis_label_fontsize, axis_label_color, hover_fontsize, out).
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.colors import sample_colorscale

# Project imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils_xml import XMLUtils          
from adcp import ADCP as ADCPDataset   

pio.renderers.default = "browser"


class TransectViewer2D:
    """2D ADCP transect viewer."""

    def __init__(self, inputs: Dict[str, Any]) -> None:
        self.cfg = dict(inputs)

        xml_path = self.cfg["xml"]
        surveys = self.cfg.get("surveys", [])
        if not surveys:
            raise ValueError("`surveys` must be a non-empty list of survey names.")

        project = XMLUtils(xml_path)

        adcp_entries: List[Tuple[str, Dict[str, Any]]] = []
        for svy in surveys:
            for acfg in project.get_survey_adcp_cfgs(svy):
                adcp_entries.append((svy, acfg))

        self.adcps: List[ADCPDataset] = []
        self.survey_by_name: Dict[str, str] = {}
        for svy, acfg in adcp_entries:
            adcp = ADCPDataset(acfg, name=acfg["name"])
            self.adcps.append(adcp)
            self.survey_by_name[str(adcp.name)] = svy

        self.frame: Dict[str, float] = {}
        self.fig: go.Figure | None = None
        self.cmin: float = 0.0
        self.cmax: float = 1.0

    # --------- helpers ---------
    @staticmethod
    def _meters_per_degree(lat_deg: float) -> Tuple[float, float]:
        lat = np.deg2rad(lat_deg)
        m_per_deg_lat = 111_132.92 - 559.82*np.cos(2*lat) + 1.175*np.cos(4*lat)
        m_per_deg_lon = 111_412.84*np.cos(lat) - 93.5*np.cos(3*lat)
        return float(m_per_deg_lon), float(m_per_deg_lat)

    def _global_frame_from_adcps(self) -> Tuple[float, float, float, float]:
        lon = np.concatenate([np.asarray(a.position.x, float).ravel()
                              for a in self.adcps if np.size(a.position.x)])
        lat = np.concatenate([np.asarray(a.position.y, float).ravel()
                              for a in self.adcps if np.size(a.position.y)])
        if lon.size == 0 or lat.size == 0:
            raise ValueError("No positions found in ADCP datasets.")
        lon0 = float(np.nanmedian(lon))
        lat0 = float(np.nanmedian(lat))
        m_per_deg_lon, m_per_deg_lat = self._meters_per_degree(lat0)
        return lon0, lat0, m_per_deg_lon, m_per_deg_lat

    @staticmethod
    def _font_color_for_bg(bg_color: str) -> str:
        c = (bg_color or "").strip().lower().replace(" ", "")
        return "#ffffff" if c in ("black", "#000", "#000000", "rgb(0,0,0)") else "#000000"

    @staticmethod
    def _format_field_label(field: str) -> str:
        mapping = {
            "absolute_backscatter": "Absolute Backscatter (dB)",
            "echo_intensity": "Echo Intensity (Counts)",
            "correlation_magnitude": "Correlation Magnitude (Counts)",
            "suspended_solids_concentration": "Suspended Solids Concentration (mg/L)",
        }
        return mapping.get(field, field.replace("_", " ").title())

    @staticmethod
    def _time_bounds(adcp: ADCPDataset) -> Tuple[str, str]:
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

    # --------- series + coloring ---------
    def _series_for(self, adcp: ADCPDataset, field: str, vcfg: Dict[str, Any]) -> np.ndarray:
        method = str(vcfg.get("method", "mean")).lower()
        beam = vcfg.get("beam", "mean")
        agg = vcfg.get("agg", "mean")
        if method == "mean":
            # Mean across all bins, beams.
            relz = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, float)
            n_bins = relz.shape[1]
            return np.asarray(
                adcp.get_beam_series(field_name=field, mode="bin", target=(1, n_bins),
                                     beam="mean", agg="mean"),
                float
            )
        elif method in {"bin", "range", "hab"}:
            if "target" not in vcfg:
                raise ValueError(f"vertical_agg.target required for method='{method}'.")
            return np.asarray(
                adcp.get_beam_series(field_name=field, mode=method, target=vcfg["target"],
                                     beam=beam, agg=agg),
                float
            )
        else:
            raise ValueError(f"Unsupported vertical_agg.method: {method}")

    @staticmethod
    def _color_for(value: float, cmin: float, cmax: float, cmap: str) -> str:
        if not np.isfinite(value):
            return "rgba(0,0,0,0)"
        if cmax <= cmin:
            t = 0.5
        else:
            t = (value - cmin) / (cmax - cmin)
        t = float(np.clip(t, 0.0, 1.0))
        return sample_colorscale(cmap, [t])[0]

    # --------- shapefiles ---------
    def _add_shapefiles(self, fig: go.Figure) -> go.Figure:
        shp_inputs = self.cfg.get("shp", [])
        if not shp_inputs:
            return fig

        import geopandas as gpd
        from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon, Point, MultiPoint

        lon0 = self.frame["lon0"]; lat0 = self.frame["lat0"]
        m_per_deg_lon = self.frame["m_per_deg_lon"]; m_per_deg_lat = self.frame["m_per_deg_lat"]

        def to_cfg(item: Any) -> Dict[str, Any]:
            if isinstance(item, str):
                return dict(path=item, type="auto", color="#00FFAA", width=2,
                            label=None, label_fontsize=12, label_color="#ffffff",
                            markersize=6, text_attr=None)
            base = dict(type="auto", color="#00FFAA", width=2,
                        label=None, label_fontsize=12, label_color="#ffffff",
                        markersize=6, text_attr=None)
            base.update(item)
            return base

        def add_line(xs: Iterable[float], ys: Iterable[float], color: str, width: int) -> None:
            xs = np.asarray(xs, float); ys = np.asarray(ys, float)
            x_m = (xs - lon0) * m_per_deg_lon; y_m = (ys - lat0) * m_per_deg_lat
            fig.add_trace(go.Scatter(
                x=x_m, y=y_m, mode="lines",
                line=dict(color=color, width=int(width)),
                showlegend=False, hoverinfo="skip"
            ))

        def add_points(xs: Iterable[float], ys: Iterable[float],
                       color: str, size: float,
                       texts: List[str] | None, tcolor: str, tsize: int) -> None:
            xs = np.asarray(xs, float); ys = np.asarray(ys, float)
            x_m = (xs - lon0) * m_per_deg_lon; y_m = (ys - lat0) * m_per_deg_lat
            kwargs: Dict[str, Any] = dict(
                x=x_m, y=y_m, mode="markers+text" if texts is not None else "markers",
                marker=dict(size=float(size), color=color),
                showlegend=False, hoverinfo="skip"
            )
            if texts is not None:
                kwargs["text"] = texts
                kwargs["textfont"] = dict(size=int(tsize), color=tcolor)
                kwargs["textposition"] = "top center"
            fig.add_trace(go.Scatter(**kwargs))

        for item in shp_inputs:
            cfg = to_cfg(item)
            path = cfg["path"]
            layer_type = str(cfg.get("type", "auto")).lower()
            color = cfg.get("color", "#00FFAA"); width = int(cfg.get("width", 2))
            label = cfg.get("label"); lab_size = int(cfg.get("label_fontsize", 12))
            lab_color = cfg.get("label_color", "#ffffff")
            markersize = cfg.get("markersize", 6); text_attr = cfg.get("text_attr")

            gdf = gpd.read_file(path)
            if gdf.crs is None:
                raise ValueError(f"{path}: CRS undefined. Reproject to EPSG:4326.")
            gdf = gdf.to_crs("EPSG:4326")

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
                    if geom is None or geom.is_empty: continue
                    if isinstance(geom, LineString):
                        xs, ys = geom.xy; add_line(xs, ys, color, width)
                    elif isinstance(geom, MultiLineString):
                        for part in geom.geoms:
                            xs, ys = part.xy; add_line(xs, ys, color, width)
                    elif isinstance(geom, Polygon):
                        xs, ys = geom.exterior.xy; add_line(xs, ys, color, width)
                    elif isinstance(geom, MultiPolygon):
                        for pg in geom.geoms:
                            xs, ys = pg.exterior.xy; add_line(xs, ys, color, width)
                if label:
                    minx, miny, maxx, maxy = gdf.total_bounds
                    cx, cy = 0.5*(minx+maxx), 0.5*(miny+maxy)
                    add_points([cx], [cy], color, 0, [label], lab_color, lab_size)

            elif layer_type == "point":
                xs_all: List[float] = []; ys_all: List[float] = []; texts: List[str] = []; has_text = False
                for idx, geom in enumerate(gdf.geometry):
                    if geom is None or geom.is_empty: continue
                    coords: List[Tuple[float, float]] = []
                    if isinstance(geom, Point): coords = [(geom.x, geom.y)]
                    elif isinstance(geom, MultiPoint): coords = [(p.x, p.y) for p in geom.geoms]
                    else: continue
                    if text_attr and text_attr in gdf.columns:
                        txt = str(gdf.iloc[idx][text_attr]); texts.extend([txt]*len(coords)); has_text = True
                    elif label:
                        texts.extend([str(label)]*len(coords)); has_text = True
                    else:
                        texts.extend([None]*len(coords))
                    for x, y in coords:
                        xs_all.append(x); ys_all.append(y)
                add_points(xs_all, ys_all, color, markersize,
                           np.array(texts, dtype=object) if has_text else None,
                           lab_color, lab_size)
            else:
                raise ValueError(f"Unsupported layer type: {layer_type}")

        return fig

    # --------- graticule ---------
    def _add_graticule_equal(self, fig: go.Figure,
                             lon_min_deg: float, lon_max_deg: float,
                             lat_min_deg: float, lat_max_deg: float,
                             xr_m: Tuple[float, float], yr_m: Tuple[float, float]) -> go.Figure:
        lon0 = self.frame["lon0"]; lat0 = self.frame["lat0"]
        m_per_deg_lon = self.frame["m_per_deg_lon"]; m_per_deg_lat = self.frame["m_per_deg_lat"]

        color = self.cfg.get("grid_color", "#333")
        width = int(self.cfg.get("grid_width", 1))
        opacity = float(self.cfg.get("grid_opacity", 0.35))
        n_lines = int(self.cfg.get("grid_lines", 9))

        lon_vals = np.linspace(lon_min_deg, lon_max_deg, n_lines)
        lat_vals = np.linspace(lat_min_deg, lat_max_deg, n_lines)

        # lon lines
        y0_m, y1_m = yr_m
        for LON in lon_vals:
            x_m = (LON - lon0) * m_per_deg_lon
            fig.add_trace(go.Scatter(
                x=[x_m, x_m], y=[y0_m, y1_m], mode="lines",
                line=dict(color=color, width=width), opacity=opacity,
                showlegend=False, hoverinfo="skip"
            ))
        # lat lines
        x0_m, x1_m = xr_m
        for LAT in lat_vals:
            y_m = (LAT - lat0) * m_per_deg_lat
            fig.add_trace(go.Scatter(
                x=[x0_m, x1_m], y=[y_m, y_m], mode="lines",
                line=dict(color=color, width=width), opacity=opacity,
                showlegend=False, hoverinfo="skip"
            ))
        return fig

    # --------- build transect lines ---------
    def _build_transect_lines(self, fig: go.Figure) -> Tuple[go.Figure, float, float]:
        field = self.cfg.get("field_name", "absolute_backscatter")
        cmap = self.cfg.get("cmap", "jet")
        vmin = self.cfg.get("vmin", None)
        vmax = self.cfg.get("vmax", None)
        lw = float(self.cfg.get("transect_line_width", 3.0))
        vcfg = dict(self.cfg.get("vertical_agg", {"method": "mean"}))
    
        lon0, lat0, m_per_deg_lon, m_per_deg_lat = self._global_frame_from_adcps()
        self.frame = dict(lon0=lon0, lat0=lat0,
                          m_per_deg_lon=m_per_deg_lon, m_per_deg_lat=m_per_deg_lat)
    
        all_vals: List[np.ndarray] = []
        for adcp in self.adcps:
            try:
                series = self._series_for(adcp, field, vcfg)
                all_vals.append(series[np.isfinite(series)])
            except Exception:
                continue
        if vmin is None or vmax is None:
            if all_vals:
                pool = np.concatenate(all_vals)
                cmin = float(np.nanmin(pool)); cmax = float(np.nanmax(pool))
                if not np.isfinite(cmin) or not np.isfinite(cmax) or cmax == cmin:
                    cmin, cmax = 0.0, 1.0
            else:
                cmin, cmax = 0.0, 1.0
        else:
            cmin, cmax = float(vmin), float(vmax)
        self.cmin, self.cmax = cmin, cmax
    
        for adcp in self.adcps:
            lon = np.asarray(adcp.position.x, float).ravel()
            lat = np.asarray(adcp.position.y, float).ravel()
            n_pos = min(lon.size, lat.size)
            if n_pos < 2:
                continue
            try:
                series = self._series_for(adcp, field, vcfg).ravel()
            except Exception:
                continue
            n = min(n_pos, series.size)
            lon = lon[:n]; lat = lat[:n]; series = series[:n]
    
            x_m = (lon - lon0) * m_per_deg_lon
            y_m = (lat - lat0) * m_per_deg_lat
    
            start_str, end_str = self._time_bounds(adcp)
            tr_name = str(getattr(adcp, "name", "transect"))
            svy_name = str(self.survey_by_name.get(tr_name, "n/a"))
    
            for i in range(n - 1):
                if not (np.isfinite(series[i]) and np.isfinite(series[i+1])): continue
                if not (np.isfinite(x_m[i]) and np.isfinite(x_m[i+1]) and
                        np.isfinite(y_m[i]) and np.isfinite(y_m[i+1])): continue
    
                # segment value at the hover point ≈ midpoint value
                cval_mid = 0.5 * (series[i] + series[i+1])
                color = self._color_for(cval_mid, cmin, cmax, cmap)
    
                lon_mid = 0.5 * (lon[i] + lon[i+1])
                lat_mid = 0.5 * (lat[i] + lat[i+1])
                custom = np.array([[lon_mid, lat_mid, cval_mid], [lon_mid, lat_mid, cval_mid]])
    
                fig.add_trace(go.Scatter(
                    x=[x_m[i], x_m[i+1]],
                    y=[y_m[i], y_m[i+1]],
                    mode="lines",
                    line=dict(color=color, width=lw),
                    showlegend=False,
                    name=tr_name,
                    customdata=custom,
                    meta=dict(transect=tr_name, start=start_str, end=end_str, survey=svy_name),
                    hovertemplate=(
                "<b>%{meta.transect}</b><br>"
                "survey: %{meta.survey}<br>"
                "start: %{meta.start}<br>"
                "end: %{meta.end}<br>"
                "lon = %{customdata[0]:.5f}°<br>"
                "lat = %{customdata[1]:.5f}°<br>"
                "value = %{customdata[2]:.3f}"
                "<extra></extra>"
            )

                ))
    
        font_col = self._font_color_for_bg(self.cfg.get("bgcolor", "black"))
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(
                colorscale=self.cfg.get("cmap", "jet"),
                cmin=cmin, cmax=cmax, color=[cmin], showscale=True,
                colorbar=dict(
                    title=dict(text=self._format_field_label(field), side="right", font=dict(color=font_col)),
                    thickness=15, len=0.33, x=1.02, xanchor="left", y=0.02, yanchor="bottom",
                    bgcolor=self.cfg.get("bgcolor", "black"),
                    outlinecolor="#777", tickcolor=font_col, tickfont=dict(color=font_col),
                    ticklen=4, tickwidth=1
                )
            ),
            hoverinfo="skip", showlegend=False
        ))
        return fig, cmin, cmax



    # --------- axes, ticks, camera (2D) ---------
    def _apply_axes_and_grids(self, fig: go.Figure) -> go.Figure:
        pad_deg = float(self.cfg.get("pad_deg", 0.05))
        bgcolor = self.cfg.get("bgcolor", "black")
        font_col = self._font_color_for_bg(bgcolor)
        axis_label_color = self.cfg.get("axis_label_color", font_col)
        axis_label_fontsize = int(self.cfg.get("axis_label_fontsize", 12))
        tick_fontsize = int(self.cfg.get("tick_fontsize", 10))
        nt = max(2, int(self.cfg.get("axis_ticks", 7)))
        decimals = int(self.cfg.get("tick_decimals", 4))
    
        # Gather lon/lat and padded degree extents
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
    
        # Convert padded degree extents to meters (plot coords)
        lon0 = self.frame["lon0"]; lat0 = self.frame["lat0"]
        m_per_deg_lon = self.frame["m_per_deg_lon"]; m_per_deg_lat = self.frame["m_per_deg_lat"]
        xr = np.array([(lon_min_deg - lon0) * m_per_deg_lon,
                       (lon_max_deg - lon0) * m_per_deg_lon], dtype=float)
        yr = np.array([(lat_min_deg - lat0) * m_per_deg_lat,
                       (lat_max_deg - lat0) * m_per_deg_lat], dtype=float)
    
        # Tick positions in meters with labels in degrees
        x_tickvals = np.linspace(xr[0], xr[1], nt)
        y_tickvals = np.linspace(yr[0], yr[1], nt)
        x_ticktext = [f"{lon_min_deg + (lon_max_deg - lon_min_deg)*i/(nt-1):.{decimals}f}" for i in range(nt)]
        y_ticktext = [f"{lat_min_deg + (lat_max_deg - lat_min_deg)*i/(nt-1):.{decimals}f}" for i in range(nt)]
    
        # Hover label styling
        hover_fontsize = int(self.cfg.get("hover_fontsize", max(7, int(tick_fontsize * 0.9))))
        hover_bg = "rgba(0,0,0,0.7)" if font_col == "#ffffff" else "rgba(255,255,255,0.9)"
    
        # Layout with equal XY aspect
        margins = self.cfg.get("margins", {"l": 80, "r": 120, "t": 40, "b": 70})
        fig.update_layout(
            xaxis=dict(
                range=[xr[0], xr[1]],
                tickmode="array", tickvals=x_tickvals.tolist(), ticktext=x_ticktext,
                title=dict(text="Longitude (°)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                tickfont=dict(color=font_col, size=tick_fontsize),
                automargin=True, showgrid=False, zeroline=False,
                scaleanchor="y", scaleratio=1  # enforce XY = 1:1
            ),
            yaxis=dict(
                range=[yr[0], yr[1]],
                tickmode="array", tickvals=y_tickvals.tolist(), ticktext=y_ticktext,
                title=dict(text="Latitude (°)", font=dict(color=axis_label_color, size=axis_label_fontsize)),
                tickfont=dict(color=font_col, size=tick_fontsize),
                automargin=True, showgrid=False, zeroline=False,
            ),
            dragmode="pan",
            paper_bgcolor=bgcolor,
            plot_bgcolor=bgcolor,
            hoverlabel=dict(font=dict(size=hover_fontsize, color=font_col), bgcolor=hover_bg),
            margin=margins,
            template=None,
            showlegend=False
        )
    
        # Graticule across full domain (at z=0 conceptually)
        fig = self._add_graticule_equal(
            fig,
            lon_min_deg, lon_max_deg, lat_min_deg, lat_max_deg,
            xr_m=(xr[0], xr[1]), yr_m=(yr[0], yr[1])
        )
        return fig



    # --------- public ---------
    def render(self) -> go.Figure:
        fig = go.Figure()
        fig, _, _ = self._build_transect_lines(fig)
        fig = self._add_shapefiles(fig)
        fig = self._apply_axes_and_grids(fig)
        self.fig = fig
        return fig

    def save_html(self, path: str | None = None, auto_open: bool = False) -> str:
        if self.fig is None:
            raise RuntimeError("Call render() before save_html().")
        out_path = path or self.cfg.get("out", None)
        if not out_path:
            raise ValueError("Provide `path` or set `out` in inputs.")
    
        config = self.cfg.get("plotly_config", {
            "scrollZoom": True,      # mouse wheel zoom
            "doubleClick": "reset",
            "displaylogo": False,
            "responsive": True
        })
    
        html = self.fig.to_html(include_plotlyjs="cdn", full_html=True,
                                div_id="plotly-div", config=config)
        html = html.replace("</body>", self._north_arrow_js_2d() + "\n</body>")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        if auto_open:
            import webbrowser, pathlib
            webbrowser.open(pathlib.Path(out_path).absolute().as_uri())
        return out_path


    @staticmethod
    def _north_arrow_js_2d() -> str:
        return r"""
<script>
(function(){
  const pad = 24;
  const wrap = document.createElement('div');
  wrap.style.position='fixed';
  wrap.style.top= pad + 'px';
  wrap.style.right= pad + 'px';
  wrap.style.width='56px';
  wrap.style.height='56px';
  wrap.style.zIndex=10000;
  wrap.style.pointerEvents='none';
  wrap.innerHTML = `
    <svg viewBox="0 0 100 100" width="56" height="56" style="opacity:0.95">
      <g transform="translate(50,50)">
        <polygon points="0,-30 9,10 0,5 -9,10" fill="#ffffff"/>
        <text x="0" y="-34" text-anchor="middle" fill="#ffffff" font-size="14" font-family="Arial">N</text>
      </g>
    </svg>`;
  document.body.appendChild(wrap);
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
<<<<<<< Updated upstream
                "type": "line", "color": "limegreen", "width": 1,
                "label": "Channel", "label_fontsize": 11, "label_color": "#cccccc",
=======
                "type": "line",
                "color": "limegreen",
                "width": 0.5,
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        "vmax": -60,
        "pad_deg": 0.03,
        "grid_lines": 10,
        "grid_opacity": 0.35,
        "grid_color": "#333",
        "grid_width": 1,
        "bgcolor": "black",
        "axis_ticks": 7,
        "tick_fontsize": 10,
        "tick_decimals": 4,
        "axis_label_fontsize": 12,
        "axis_label_color": "#cccccc",
        "hover_fontsize": 9,
        "transect_line_width": 3.5,
        "vertical_agg": {
        "method": "mean",  # or "bin"
        "target": 5, # targed bin
        "beam": 'mean', # beam 1-4 or "mean
            
        },
=======
        "vmax": None,
        "pad_deg": 0.03,        # Pad on the bounding box on all the transects. Defines the margin to the edges of the figure.
        "grid_lines": 10,       # Number of grid lines in each direction (lon, lat).
        "grid_opacity": 0.35,   # Opacity of the grid lines.
        "grid_color": "#333",   # Color of the grid lines.
        "grid_width": 1,        # Width of the grid lines.
        "bgcolor": "black",     # Background color of the plot.
        "axis_ticks": 7,        # Number of ticks on each axis.
        "tick_fontsize": 10,    # Font size of the axis ticks.
        "tick_decimals": 4,   # Number of decimals for the axis tick labels.
        "axis_label_fontsize": 12,  # Font size of the axis labels.
        "axis_label_color": "#cccccc",  # Color of the axis labels.
        "hover_fontsize": 9,    # Font size of the hover labels.
        "transect_line_width": 3.0, # Width of the transect lines. (Max = 4)
        "vertical_agg": {
                "method": "mean",  # or "bin"/"range(depth)/hab", plus target/beam/agg as needed
                "target": 5, # targed bin,range or hab
                "beam": "mean", # beam 1-4 or "mean"
            },
>>>>>>> Stashed changes
        "out": r"C:\Users\anba\OneDrive - DHI\Desktop\Documents\GitHub\PlumeTrack\backend\adcp_transects_2d.html",
    }

    viewer = TransectViewer2D(inputs)
    fig = viewer.render()
    viewer.save_html(auto_open=False)
