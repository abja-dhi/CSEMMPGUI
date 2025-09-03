# -*- coding: utf-8 -*-
"""
3D ADCP curtain plots with optional shapefile overlay at z=0.
- XY aspect fixed 1:1 (manual).
- Scene clipped to ADCP lon/lat extent ±0.1°.
- North-up camera, closer zoom, initial view from south toward north.
- Equal-spacing lat/lon graticule over the current view.
- Surface hover shows transect name, lon, lat, depth.
- North arrow overlay (bottom-right) that tracks camera yaw; north = +latitude.
- Config via `inputs` dict at bottom.
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
        raise ValueError("No positions found in adcps.")
    lon0 = float(np.nanmedian(lon))
    lat0 = float(np.nanmedian(lat))
    m_per_deg_lon, m_per_deg_lat = meters_per_degree(lat0)
    return lon0, lat0, m_per_deg_lon, m_per_deg_lat, lon, lat

def make_ticks(vals_m, deg0, m_per_deg, n=6):
    lo, hi = float(np.nanmin(vals_m)), float(np.nanmax(vals_m))
    t = np.linspace(lo, hi, n)
    lbl = [f"{deg0 + v/m_per_deg:.5f}" for v in t]
    return t.tolist(), lbl

def extent_xy(xm, ym, pad=0.02):
    xmin, xmax = float(np.nanmin(xm)), float(np.nanmax(xm))
    ymin, ymax = float(np.nanmin(ym)), float(np.nanmax(ym))
    dx = (xmax - xmin) or 1.0
    dy = (ymax - ymin) or 1.0
    return (xmin - pad*dx, xmax + pad*dx), (ymin - pad*dy, ymax + pad*dy)

# ------------- curtains -------------
def build_curtain_figure(adcps, field="absolute_backscatter",
                         colorscale="turbo", vmin=None, vmax=None, zscale=1.0):
    lon0, lat0, m_per_deg_lon, m_per_deg_lat, lon_all, lat_all = global_frame_from_adcps(adcps)

    traces = []
    pool = []
    x_all_m = []; y_all_m = []; z_all = []

    for adcp in adcps:
        lon = np.asarray(adcp.position.x, float).ravel()
        lat = np.asarray(adcp.position.y, float).ravel()
        relz = np.asarray(adcp.geometry.relative_beam_midpoint_positions.z, float)   # (t,b,beam)
        vals = np.asarray(adcp.get_beam_data(field_name=field, mask=True), float)    # (t,b,beam)
        if relz.shape != vals.shape:
            raise ValueError(f"{adcp.name}: relz {relz.shape} != values {vals.shape}")

        n = min(lon.size, lat.size, vals.shape[0])
        lon, lat, relz, vals = lon[:n], lat[:n], relz[:n], vals[:n]

        V = np.nanmean(vals, axis=2)          # (t,b)
        Z = np.nanmean(relz, axis=2) * zscale # (t,b)

        nb = V.shape[1]
        x_m = (lon - lon0) * m_per_deg_lon
        y_m = (lat - lat0) * m_per_deg_lat
        X = np.tile(x_m, (nb, 1))             # (b,t)
        Y = np.tile(y_m, (nb, 1))             # (b,t)
        C = V.T                               # (b,t)
        ZZ = Z.T                              # (b,t)

        # NaNs transparent
        mask = ~np.isfinite(C)
        C = C.astype(float); ZZ = ZZ.astype(float)
        C[mask] = np.nan; ZZ[mask] = np.nan

        # hover in degrees and meters + transect name
        Lon_deg = (X / m_per_deg_lon) + lon0
        Lat_deg = (Y / m_per_deg_lat) + lat0
        custom = np.stack([Lon_deg, Lat_deg, ZZ], axis=-1)  # (b,t,3)
        tr_name = str(getattr(adcp, "name", "transect"))

        traces.append(go.Surface(
            x=X, y=Y, z=ZZ, surfacecolor=C,
            customdata=custom,
            colorscale=colorscale,
            opacity=0.95,
            showscale=False,
            name=tr_name,
            meta=dict(transect=tr_name),
            hovertemplate=(
                "<b>%{meta.transect}</b><br>"
                "lon = %{customdata[0]:.5f}°<br>"
                "lat = %{customdata[1]:.5f}°<br>"
                "depth = %{customdata[2]:.2f} m"
                "<extra></extra>"
            )
        ))
        pool.append(C)
        x_all_m.append(x_m); y_all_m.append(y_m); z_all.append(ZZ)

    # color scale
    if vmin is None or vmax is None:
        pool_vals = np.concatenate([p[~np.isnan(p)] for p in pool]) if pool else np.array([])
        cmin, cmax = (0.0, 1.0) if pool_vals.size == 0 else (float(np.nanmin(pool_vals)), float(np.nanmax(pool_vals)))
    else:
        cmin, cmax = float(vmin), float(vmax)

    for i, tr in enumerate(traces):
        tr.update(cmin=cmin, cmax=cmax, showscale=(i == 0), colorbar_title=field.replace("_", " "))

    x_all_m = np.concatenate(x_all_m); y_all_m = np.concatenate(y_all_m); z_all = np.concatenate([z.ravel() for z in z_all])
    (axr0, axr1), (ayr0, ayr1) = extent_xy(x_all_m, y_all_m)
    zmin, zmax = float(np.nanmin(z_all)), float(np.nanmax(z_all))
    zmin, zmax = min(zmin, 0.0), max(zmax, 0.0)  # force z=0 visible

    # optional ticks in degrees
    xt, xtlbl = make_ticks(x_all_m, lon0, m_per_deg_lon)
    yt, ytlbl = make_ticks(y_all_m, lat0, m_per_deg_lat)

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Longitude (°)", tickmode="array", tickvals=xt, ticktext=xtlbl,
                       backgroundcolor="black", gridcolor="#333", zerolinecolor="#333"),
            yaxis=dict(title="Latitude (°)",  tickmode="array", tickvals=yt, ticktext=ytlbl,
                       backgroundcolor="black", gridcolor="#333", zerolinecolor="#333"),
            zaxis=dict(title="Depth (m)", backgroundcolor="black", gridcolor="#333", zerolinecolor="#333"),
        ),
        paper_bgcolor="black",
        plot_bgcolor="black",
        margin=dict(l=0, r=0, t=30, b=0),
        template=None
    )
    frame = dict(lon0=lon0, lat0=lat0,
                 m_per_deg_lon=m_per_deg_lon, m_per_deg_lat=m_per_deg_lat)
    return fig, frame, ((axr0, axr1), (ayr0, ayr1)), (zmin, zmax)

# ------------- shapefile overlay -------------
def add_shapefiles_z0(fig, shp_paths, frame, color="#00FFAA", width=2):
    lon0 = frame["lon0"]; lat0 = frame["lat0"]
    m_per_deg_lon = frame["m_per_deg_lon"]; m_per_deg_lat = frame["m_per_deg_lat"]

    for shp_path in shp_paths:
        gdf = gpd.read_file(shp_path)
        if gdf.crs is None:
            raise ValueError(f"{shp_path}: CRS undefined. Reproject to EPSG:4326.")
        gdf = gdf.to_crs("EPSG:4326")

        def add_lines(xs, ys):
            xs = np.asarray(xs, float); ys = np.asarray(ys, float)
            x_m = (xs - lon0) * m_per_deg_lon
            y_m = (ys - lat0) * m_per_deg_lat
            fig.add_trace(go.Scatter3d(
                x=x_m, y=y_m, z=np.zeros_like(x_m),
                mode="lines",
                line=dict(color=color, width=width),
                showlegend=False,
                hoverinfo="skip"
            ))

        for geom in gdf.geometry:
            if geom is None or geom.is_empty:
                continue
            if isinstance(geom, LineString):
                xs, ys = geom.xy; add_lines(xs, ys)
            elif isinstance(geom, MultiLineString):
                for part in geom.geoms: xs, ys = part.xy; add_lines(xs, ys)
            elif isinstance(geom, Polygon):
                xs, ys = geom.exterior.xy; add_lines(xs, ys)
            elif isinstance(geom, MultiPolygon):
                for pg in geom.geoms: xs, ys = pg.exterior.xy; add_lines(xs, ys)
    return fig

# ------------- graticule -------------
def add_graticule(fig, frame, xr, yr, color="#444", width=1, n_lines=9):
    """
    Equal-spacing lat/lon graticule over CURRENT view.
    Exactly spans the shown domain with the same number of lines per axis.
    """
    lon0, lat0 = frame["lon0"], frame["lat0"]
    m_per_deg_lon, m_per_deg_lat = frame["m_per_deg_lon"], frame["m_per_deg_lat"]

    # Convert current meter ranges back to degrees
    lon_min = lon0 + xr[0] / m_per_deg_lon
    lon_max = lon0 + xr[1] / m_per_deg_lon
    lat_min = lat0 + yr[0] / m_per_deg_lat
    lat_max = lat0 + yr[1] / m_per_deg_lat

    lon_vals = np.linspace(lon_min, lon_max, n_lines)
    lat_vals = np.linspace(lat_min, lat_max, n_lines)

    z0 = 0.0

    # Constant-longitude lines (varying latitude)
    y_edge_m = (np.array([lat_min, lat_max]) - lat0) * m_per_deg_lat
    for LON in lon_vals:
        x_m = (LON - lon0) * m_per_deg_lon
        fig.add_trace(go.Scatter3d(
            x=[x_m, x_m], y=[y_edge_m[0], y_edge_m[1]], z=[z0, z0],
            mode="lines", line=dict(color=color, width=width),
            showlegend=False, hoverinfo="skip"
        ))

    # Constant-latitude lines (varying longitude)
    x_edge_m = (np.array([lon_min, lon_max]) - lon0) * m_per_deg_lon
    for LAT in lat_vals:
        y_m = (LAT - lat0) * m_per_deg_lat
        fig.add_trace(go.Scatter3d(
            x=[x_edge_m[0], x_edge_m[1]], y=[y_m, y_m], z=[z0, z0],
            mode="lines", line=dict(color=color, width=width),
            showlegend=False, hoverinfo="skip"
        ))
    return fig

# ------------- run with input dict -------------
if __name__ == "__main__":
    inputs = {
        "xml": r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Real Project.mtproj",
        "survey": "Survey 1",
        "shp": [r"C:/Users/anba/Downloads/v20250509/v20250509/RD7550_CEx_SG_v20250509.shp"],
        "colorscale": "turbo",
        "vmin": None,
        "vmax": None,
        "zscale": 1.0,
        "out": r"C:\Users\anba\OneDrive - DHI\Desktop\Documents\GitHub\PlumeTrack\backend\test_w_shapefile.html"
    }

    # Load ADCPs
    project = XMLUtils(inputs["xml"])
    adcp_cfgs = project.get_survey_adcp_cfgs(inputs["survey"])
    adcps = [ADCPDataset(cfg, name=cfg['name']) for cfg in adcp_cfgs]

    # Build curtains
    fig, frame, _, (zmin, zmax) = build_curtain_figure(
        adcps,
        field="absolute_backscatter",
        colorscale=inputs["colorscale"],
        vmin=inputs["vmin"], vmax=inputs["vmax"],
        zscale=inputs["zscale"]
    )

    # Overlays
    if inputs["shp"]:
        fig = add_shapefiles_z0(fig, inputs["shp"], frame)

    # Clip scene to ADCP lon/lat ±0.1°
    lon_all = np.concatenate([np.asarray(a.position.x, float).ravel() for a in adcps if np.size(a.position.x)])
    lat_all = np.concatenate([np.asarray(a.position.y, float).ravel() for a in adcps if np.size(a.position.y)])
    lon_min, lon_max = float(np.nanmin(lon_all)), float(np.nanmax(lon_all))
    lat_min, lat_max = float(np.nanmin(lat_all)), float(np.nanmax(lat_all))
    pad_deg = 0.1

    lon0, lat0 = frame["lon0"], frame["lat0"]
    m_per_deg_lon, m_per_deg_lat = frame["m_per_deg_lon"], frame["m_per_deg_lat"]

    xr0 = ((lon_min - pad_deg) - lon0) * m_per_deg_lon
    xr1 = ((lon_max + pad_deg) - lon0) * m_per_deg_lon
    yr0 = ((lat_min - pad_deg) - lat0) * m_per_deg_lat
    yr1 = ((lat_max + pad_deg) - lat0) * m_per_deg_lat

    z0min, z0max = min(zmin, 0.0), max(zmax, 0.0)

    # Fixed XY aspect ratio = 1:1; north-up; initial view from south → north; closer zoom
    dx = xr1 - xr0; dy = yr1 - yr0
    span_xy = max(dx, dy) if max(dx, dy) > 0 else 1.0
    dz = z0max - z0min
    z_ratio = dz / span_xy if span_xy > 0 else 1.0

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[xr0, xr1]),
            yaxis=dict(range=[yr0, yr1]),
            zaxis=dict(range=[z0min, z0max]),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=z_ratio),
            camera=dict(
                up=dict(x=0, y=0, z=1),          # Z vertical
                center=dict(x=0, y=0, z=0),
                eye=dict(x=0.0, y=-0.35, z=0.18) # due south looking north; higher zoom
            )
        )
    )

    # Graticule over clipped extent (equal spacing)
    fig = add_graticule(fig, frame, (xr0, xr1), (yr0, yr1), color="#333", width=1, n_lines=9)

    # North arrow overlay (bottom-right), north = +Y (latitude+), follows camera yaw
    out_path = inputs["out"]
    html = fig.to_html(include_plotlyjs="cdn", full_html=True, div_id="plotly-div")

    north_js = r"""
<script>
(function(){
  const wrap = document.createElement('div');
  wrap.style.position='absolute';
  wrap.style.bottom='10px';
  wrap.style.right='10px';
  wrap.style.width='48px';
  wrap.style.height='48px';
  wrap.style.zIndex=1000;
  wrap.style.pointerEvents='none';
  wrap.innerHTML = `
    <svg id="northArrow" viewBox="0 0 100 100" width="48" height="48" style="opacity:0.9">
      <circle cx="50" cy="50" r="48" fill="rgba(0,0,0,0.35)" stroke="#aaa" stroke-width="2"/>
      <g id="arrow" transform="translate(50,50)">
        <polygon points="0,-30 8,10 0,5 -8,10" fill="#ffffff"/>
        <text x="0" y="-38" text-anchor="middle" fill="#ffffff" font-size="14" font-family="Arial">N</text>
      </g>
    </svg>`;
  document.body.appendChild(wrap);

  function norm(v){ const n=Math.hypot(v.x||0,v.y||0,v.z||0); return n?{x:(v.x||0)/n,y:(v.y||0)/n,z:(v.z||0)/n}:{x:0,y:0,z:0}; }
  function cross(a,b){ return {x:a.y*b.z-a.z*b.y, y:a.z*b.x-a.x*b.z, z:a.x*b.y-a.y*b.x}; }
  function dot(a,b){ return (a.x*b.x + a.y*b.y + a.z*b.z); }

  // Rotate arrow so it shows the screen direction of WORLD +Y (north = lat+)
  function updateArrow(cam){
    if(!cam || !cam.eye) return;
    const eye = cam.eye, up = cam.up || {x:0,y:0,z:1};
    const v = norm({x:-eye.x, y:-eye.y, z:-eye.z}); // view direction
    const r = norm(cross(v, up));                    // screen-right
    const u = norm(cross(r, v));                     // screen-up

    const Y = {x:0,y:1,z:0};                         // world north = +lat
    const px = dot(Y, r);
    const py = dot(Y, u);
    const deg = -Math.atan2(px, py) * 180/Math.PI;   // angle from screen-up to north

    const g = document.getElementById('arrow');
    if (g) g.setAttribute('transform', `translate(50,50) rotate(${deg})`);
  }

  const gd = document.getElementById('plotly-div');

  function currentCam(){
    const L = gd && gd.layout && gd.layout.scene && gd.layout.scene.camera ? gd.layout.scene.camera : {};
    const eye = L.eye || {x:0.0,y:-0.35,z:0.18};
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
