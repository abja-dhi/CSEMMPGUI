
# -*- coding: utf-8 -*-
"""
CRS utilities 
- define single project CRS
-  helpers for coordinate transforms.
- Works with scalars, arrays/series, and bounding boxes.
- Shapefile/GeoDataFrame reprojection helpers.
- Local UTM CRS lookup for meter-based calculations.
- Axis label helpers based on CRS type.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Sequence, Optional, Union

import numpy as np
from pyproj import CRS, Transformer
import geopandas as gpd


ArrayLike = Union[Sequence[float], np.ndarray]
BBox = Tuple[float, float, float, float]  # (xmin, ymin, xmax, ymax)


def _as_np(a: ArrayLike) -> np.ndarray:
    """Convert scalars/sequences to 1D numpy array of float64."""
    arr = np.asarray(a, dtype=float)
    return arr if arr.ndim > 0 else np.array([float(arr)])


def _transform_xy(x: ArrayLike, y: ArrayLike, src: CRS, dst: CRS) -> Tuple[np.ndarray, np.ndarray]:
    """Transform XY coordinates with always_xy=True (lon=x, lat=y)."""
    tx = Transformer.from_crs(src, dst, always_xy=True)
    X = _as_np(x)
    Y = _as_np(y)
    xo, yo = tx.transform(X, Y)
    return np.asarray(xo, dtype=float), np.asarray(yo, dtype=float)


@dataclass(frozen=True)
class CRSHelper:
    """
    Lightweight CRS helper bound to a single project CRS.

    Parameters
    ----------
    project_crs : str | int | pyproj.CRS
        Anything accepted by pyproj.CRS.from_user_input, e.g. 'EPSG:4326' or 4326.
    """
    project_crs: CRS

    def __init__(self, project_crs: Union[str, int, CRS]) -> None:
        object.__setattr__(self, "project_crs", CRS.from_user_input(project_crs))

    # -------------------------
    # Introspection / labels
    # -------------------------
    @property
    def is_geographic(self) -> bool:
        return self.project_crs.is_geographic

    def axis_labels(self) -> Tuple[str, str]:
        """
        Heuristic axis labels for plotting in the project CRS.
        Returns (xlabel, ylabel).
        """
        if self.is_geographic:
            return "Longitude [°E]", "Latitude [°N]"
        return "Easting [m]", "Northing [m]"

    # -------------------------
    # Coordinate transforms
    # -------------------------
    def to_project(
        self,
        x: ArrayLike,
        y: ArrayLike,
        from_crs: Union[str, int, CRS],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transform coordinates into the project CRS.
        Accepts scalars, lists, numpy arrays, pandas Series.
        """
        src = CRS.from_user_input(from_crs)
        return _transform_xy(x, y, src, self.project_crs)

    def from_project(
        self,
        x: ArrayLike,
        y: ArrayLike,
        to_crs: Union[str, int, CRS],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transform coordinates from the project CRS into another CRS.
        """
        dst = CRS.from_user_input(to_crs)
        return _transform_xy(x, y, self.project_crs, dst)

    # -------------------------
    # Bounding-box transforms
    # -------------------------
    def bbox_to_project(
        self,
        bbox: BBox,
        from_crs: Union[str, int, CRS],
        densify: int = 16,
    ) -> BBox:
        """
        Transform a bbox from from_crs into project CRS.
        Densifies edges to reduce distortion artifacts, then re-envelops.

        bbox: (xmin, ymin, xmax, ymax)
        """
        xmin, ymin, xmax, ymax = map(float, bbox)
        src = CRS.from_user_input(from_crs)

        xs = np.linspace(xmin, xmax, densify)
        ys = np.linspace(ymin, ymax, densify)

        ring_x = np.concatenate([xs, np.full_like(ys, xmax), xs[::-1], np.full_like(ys, xmin)])
        ring_y = np.concatenate([np.full_like(xs, ymin), ys, np.full_like(xs, ymax), ys[::-1]])

        xr, yr = _transform_xy(ring_x, ring_y, src, self.project_crs)
        return float(np.min(xr)), float(np.min(yr)), float(np.max(xr)), float(np.max(yr))

    def bbox_from_project(
        self,
        bbox: BBox,
        to_crs: Union[str, int, CRS],
        densify: int = 16,
    ) -> BBox:
        """
        Transform a bbox from project CRS into another CRS.
        """
        xmin, ymin, xmax, ymax = map(float, bbox)
        dst = CRS.from_user_input(to_crs)

        xs = np.linspace(xmin, xmax, densify)
        ys = np.linspace(ymin, ymax, densify)

        ring_x = np.concatenate([xs, np.full_like(ys, xmax), xs[::-1], np.full_like(ys, xmin)])
        ring_y = np.concatenate([np.full_like(xs, ymin), ys, np.full_like(xs, ymax), ys[::-1]])

        xr, yr = _transform_xy(ring_x, ring_y, self.project_crs, dst)
        return float(np.min(xr)), float(np.min(yr)), float(np.max(xr)), float(np.max(yr))

    # -------------------------
    # Local UTM helpers
    # -------------------------
    @staticmethod
    def utm_crs_from_lonlat(lon: float, lat: float) -> CRS:
        """
        Derive the UTM CRS for a lon/lat coordinate in WGS84.
        Works across hemispheres. Returns pyproj.CRS.
        """
        zone = int(np.floor((float(lon) + 180.0) / 6.0) + 1)
        north = float(lat) >= 0.0
        epsg = 32600 + zone if north else 32700 + zone
        return CRS.from_epsg(epsg)

    def to_local_utm(
        self,
        x: ArrayLike,
        y: ArrayLike,
        from_crs: Union[str, int, CRS],
        lonlat_hint: Optional[Tuple[float, float]] = None,
    ) -> Tuple[np.ndarray, np.ndarray, CRS]:
        """
        Transform coordinates to a *local UTM* CRS chosen from a lon/lat hint.

        If from_crs is geographic (WGS84 or similar) and lonlat_hint is None,
        the first (x, y) pair is used as (lon, lat) to pick the UTM zone.
        If from_crs is projected, you must pass lonlat_hint (lon, lat).
        Returns (xe, yn, utm_crs).
        """
        src = CRS.from_user_input(from_crs)

        if src.is_geographic and lonlat_hint is None:
            X = _as_np(x)
            Y = _as_np(y)
            lon = float(X[0])
            lat = float(Y[0])
        else:
            if lonlat_hint is None:
                return "lonlat_hint required when from_crs is not geographic."
            lon, lat = float(lonlat_hint[0]), float(lonlat_hint[1])

        utm = self.utm_crs_from_lonlat(lon, lat)

        if src == utm:
            xe, yn = _as_np(x), _as_np(y)
        else:
            xe, yn = _transform_xy(x, y, src, utm)

        return xe, yn, utm

    # -------------------------
    # Shapefile / GeoDataFrame
    # -------------------------
    def read_to_project(self, path: str) -> gpd.GeoDataFrame:
        """
        Read a vector dataset (any driver supported by fiona) and reproject to project CRS.
        """
        gdf = gpd.read_file(path)
        if gdf.crs is None:
             return f"Input dataset has no CRS: {path}"
        if gdf.crs == self.project_crs:
            return gdf
        return gdf.to_crs(self.project_crs)

    def to_project_gdf(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Reproject a GeoDataFrame to project CRS. Returns a copy if reprojection is needed.
        """
        if gdf.crs is None:
            return "GeoDataFrame has no CRS."
        if gdf.crs == self.project_crs:
            return gdf
        return gdf.to_crs(self.project_crs)

    def reproject_and_save(
        self,
        input_path: str,
        output_path: str,
        driver: Optional[str] = None,
        layer: Optional[str] = None,
    ) -> None:
        """
        Read → reproject to project CRS → save.

        driver: optional GDAL/OGR driver name (e.g., 'ESRI Shapefile', 'GPKG').
        layer: for multi-layer formats (e.g., GeoPackage), name of the output layer.
        """
        gdf = self.read_to_project(input_path)
        save_kwargs = {}
        if driver is not None:
            save_kwargs["driver"] = driver
        if layer is not None:
            save_kwargs["layer"] = layer
        gdf.to_file(output_path, **save_kwargs)

    # -------------------------
    # Convenience wrappers
    # -------------------------
    def to_project_xy_series(
        self,
        x: ArrayLike,
        y: ArrayLike,
        from_crs: Union[str, int, CRS],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Alias for to_project with a more explicit name."""
        return self.to_project(x, y, from_crs)

    def from_project_xy_series(
        self,
        x: ArrayLike,
        y: ArrayLike,
        to_crs: Union[str, int, CRS],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Alias for from_project with a more explicit name."""
        return self.from_project(x, y, to_crs)


if __name__ == '__main__':

    crs_helper = CRSHelper(project_crs = 4326)
    crs_helper = CRSHelper(project_crs = 32611)
    