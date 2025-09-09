# utils_shapefile.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple, Union
import os
from pathlib import Path
import geopandas as gpd
import matplotlib.axes as maxes
from shapely.geometry import Polygon, MultiPolygon

# from utils_crs import CRSHelper


@dataclass
class ShapefileLayer:
    """
    Minimal shapefile wrapper with explicit styling and a single layer-wide label.
    - Reads on init
    - Reprojects to project CRS on init via CRSHelper
    - Stores error string if anything fails
    """

    # required
    path: str
    kind: str                    # 'point' | 'line' | 'polygon'
    crs_helper: "CRSHelper"

    # style
    point_color: Optional[str] = None
    point_marker: Optional[str] = None
    point_markersize: Optional[float] = None
    line_color: Optional[str] = None
    line_width: Optional[float] = None
    poly_edgecolor: Optional[str] = None
    poly_linewidth: Optional[float] = None
    poly_facecolor: Optional[str] = None
    alpha: Optional[float] = None
    zorder: Optional[int] = None

    # layer-wide label (applied at feature representative point)
    label_text: Optional[str] = None
    label_fontsize: Optional[float] = None
    label_color: Optional[str] = None
    label_ha: Optional[str] = None
    label_va: Optional[str] = None
    label_zorder: Optional[int] = None

    # internals
    error: Optional[str] = field(default=None, init=False, repr=False)
    _gdf_proj: Optional[gpd.GeoDataFrame] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        # sanitize path (UNC with forward slashes)
        p = str(Path(self.path))
        if p.startswith("//"):
            p = "\\\\" + p.lstrip("/")
        p = p.replace("/", "\\")
        self.path = p

        kd = str(self.kind).lower().strip()
        if kd not in {"point", "line", "polygon"}:
            self.error = "kind must be 'point', 'line', or 'polygon'."
            return

        if not os.path.exists(self.path):
            self.error = f"Vector file not found: {self.path}"
            return

        try:
            gdf = gpd.read_file(self.path)
        except Exception as e:
            self.error = f"Failed to read vector file: {self.path} :: {e}"
            return

        if getattr(gdf, "crs", None) is None:
            self.error = f"Input dataset has no CRS: {self.path}"
            return

        try:
            self._gdf_proj = self.crs_helper.to_project_gdf(gdf)
        except Exception as e:
            self.error = f"Reprojection failed to {self.crs_helper.project_crs}: {e}"

    # -------- queries --------
    def is_ok(self) -> bool:
        return self.error is None and self._gdf_proj is not None

    def as_gdf(self) -> Union[gpd.GeoDataFrame, str]:
        if not self.is_ok():
            return self.error or "Layer not loaded."
        return self._gdf_proj

    def bounds(self) -> Union[Tuple[float, float, float, float], str]:
        """Return (xmin, xmax, ymin, ymax) in project CRS."""
        g = self.as_gdf()
        if isinstance(g, str):
            return g
        xmin, ymin, xmax, ymax = g.total_bounds
        return float(xmin), float(xmax), float(ymin), float(ymax)

    # -------- plotting --------
    def plot(self, ax: maxes.Axes) -> Union[None, str]:
        """Plot layer. Labels placed at representative points (handles Multi*)."""
        g = self.as_gdf()
        if isinstance(g, str):
            return g
        kd = self.kind.lower()

        if kd == "polygon":
            edgecolor = self.poly_edgecolor or "k"
            linewidth = self.poly_linewidth or 0.8
            facecolor = self.poly_facecolor or "none"
            alpha = self.alpha if self.alpha is not None else 1.0
            zorder = self.zorder if self.zorder is not None else 10
            g.plot(ax=ax, edgecolor=edgecolor, linewidth=linewidth,
                   facecolor=facecolor, alpha=alpha, zorder=zorder)

        elif kd == "line":
            color = self.line_color or "k"
            linewidth = self.line_width or 1.0
            alpha = self.alpha if self.alpha is not None else 1.0
            zorder = self.zorder if self.zorder is not None else 12
            g.plot(ax=ax, color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)

        else:  # point
            color = self.point_color or "k"
            marker = self.point_marker or "o"
            markersize = self.point_markersize or 12
            alpha = self.alpha if self.alpha is not None else 1.0
            zorder = self.zorder if self.zorder is not None else 14
            g.plot(ax=ax, color=color, marker=marker, markersize=markersize,
                   alpha=alpha, zorder=zorder)

        # Labels for any geometry type
        if self.label_text:
            fontsize = self.label_fontsize or 8
            color = self.label_color or "k"
            ha = self.label_ha or "left"
            va = self.label_va or "center"
            lz = self.label_zorder or ((self.zorder or 15) + 1)
            for _, row in g.iterrows():
                geom = row.geometry
                if geom is None or geom.is_empty:
                    continue
                # representative_point handles MultiPoint/Line/MultiLine/Polygon/MultiPolygon
                if kd == "point" and getattr(geom, "geom_type", "") == "Point":
                    x, y = geom.x, geom.y
                else:
                    x, y = geom.representative_point().coords[0]
                ax.text(x, y, self.label_text, fontsize=fontsize,
                        color=color, ha=ha, va=va, zorder=lz)
        return None

    # -------- geometry helper --------
    def polygon_mask(self) -> Union[Polygon, MultiPolygon, None, str]:
        """Dissolved polygon in project CRS if kind='polygon'."""
        g = self.as_gdf()
        if isinstance(g, str):
            return g
        if self.kind.lower() != "polygon" or g.empty:
            return None
        return g.unary_union


# ---------------- test shell ----------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from utils_crs import CRSHelper

    helper = CRSHelper("EPSG:4326")

    # Polygon layer
    coast = ShapefileLayer(
        path=r"\\usden1-stor.dhi.dk\Projects\61803553-05\GIS\SG Coastline\RD7550_CEx_SG_v20250509.shp",
        kind="polygon",
        crs_helper=helper,
        poly_edgecolor="black",
        poly_linewidth=0.6,
        poly_facecolor="none",
        alpha=1.0,
        zorder=10,
        label_text=None,
        label_fontsize=8,
        label_color="black",
    )
    if coast.error:
        raise SystemExit(coast.error)

    fig, ax = plt.subplots(figsize=(6, 4))
    err = coast.plot(ax)
    if isinstance(err, str):
        raise SystemExit(err)
    ax.set_aspect("equal")
    ax.set_xlabel(helper.axis_labels()[0])
    ax.set_ylabel(helper.axis_labels()[1])
    plt.show()

    # line layer
    coast_lines = ShapefileLayer(
        path=r"\\usden1-stor.dhi.dk\Projects\61803553-05\GIS\SG Coastline\RD7550_CEx_SG_v20250509.shp",
        kind="line",
        crs_helper=helper,
        line_color="black",
        line_width=0.8,
        alpha=1.0,
        zorder=12,
        label_text="Coastline",
        label_fontsize=8,
        label_color="black",
        label_ha="left",
        label_va="center",
    )
    if coast_lines.error:
        raise SystemExit(coast_lines.error)

    fig, ax = plt.subplots(figsize=(6, 4))
    err = coast_lines.plot(ax)
    if isinstance(err, str):
        raise SystemExit(err)

    ax.set_aspect("equal")
    ax.set_xlabel(helper.axis_labels()[0])
    ax.set_ylabel(helper.axis_labels()[1])
    plt.show()
    
    
    # Point layer
    pts = ShapefileLayer(
        path=r"\\usden1-stor.dhi.dk\Projects\61803553-05\GIS\F3\example point layer\points_labels.shp",
        kind="point",
        crs_helper=helper,
        point_color="black",
        point_marker="o",
        point_markersize=10,
        alpha=1.0,
        zorder=14,
        label_text="Example Label",
        label_fontsize=8,
        label_color="black",
        label_ha="left",
        label_va="center",
    )
    if pts.error:
        raise SystemExit(pts.error)

    fig, ax = plt.subplots(figsize=(6, 4))
    err = pts.plot(ax)
    if isinstance(err, str):
        raise SystemExit(err)
    ax.set_aspect("equal")
    ax.set_xlabel(helper.axis_labels()[0])
    ax.set_ylabel(helper.axis_labels()[1])
    plt.show()
