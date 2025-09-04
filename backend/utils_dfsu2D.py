# -*- coding: utf-8 -*-
# DFSU utils: triangles, quads, mixed. CRS-aware (geographic or projected).
# Inputs may be mesh CRS (default) or any CRS via input_crs (e.g., "EPSG:4326").
# Rasterizer uses meters per pixel. Degrees↔meters conversion only if mesh CRS is geographic.

import numpy as np
from scipy.spatial import cKDTree
from mikecore.DfsuFile import DfsuFile
from pyproj import CRS, Transformer


def crs_from_mike_token(s: str, hemisphere: str = "north") -> CRS:
    """Map MIKE projection tokens or WKT to a pyproj CRS."""
    t = s.strip().upper()
    if t in ("LONG/LAT", "LAT/LONG", "GEOGRAPHIC", "WGS84"):
        return CRS.from_epsg(4326)
    if t.startswith("UTM-"):
        zone = int(t.split("-")[1])
        epsg = (32600 + zone) if hemisphere.lower().startswith("n") else (32700 + zone)
        return CRS.from_epsg(epsg)
    if t.startswith("EPSG:"):
        return CRS.from_user_input(t)
    return CRS.from_wkt(s)  # expects genuine WKT


class DfsuUtils2D:
    """2D DFSU utilities. ROI by bbox(xq,yq). Nearest-element via centroids. CRS-aware."""

    def __init__(self, fname: str) -> None:
        self.fname = fname
        self.dfsu = DfsuFile.Open(self.fname)

        # enforce 2D
        if int(getattr(self.dfsu, "NumberOfLayers", 0) or 0) != 0:
            raise ValueError("2D DFSU required (NumberOfLayers == 0).")

        # nodes
        self._x = np.asarray(self.dfsu.X, float)
        self._y = np.asarray(self.dfsu.Y, float)

        # elements ragged (0-based)
        self._elt_nodes = [np.asarray(e, int) - 1 for e in self.dfsu.ElementTable]
        self._nverts = np.fromiter((len(e) for e in self._elt_nodes), dtype=int)
        self.is_triangular = bool(np.all(self._nverts == 3))
        self.is_quadrilateral = bool(np.all(self._nverts == 4))
        self.is_mixed = not (self.is_triangular or self.is_quadrilateral)

        # centroids and AABBs
        ne = len(self._elt_nodes)
        cx = np.empty(ne, float); cy = np.empty(ne, float)
        xmin = np.empty(ne, float); xmax = np.empty(ne, float)
        ymin = np.empty(ne, float); ymax = np.empty(ne, float)
        for i, en in enumerate(self._elt_nodes):
            xi = self._x[en]; yi = self._y[en]
            cx[i] = xi.mean(); cy[i] = yi.mean()
            xmin[i] = xi.min(); xmax[i] = xi.max()
            ymin[i] = yi.min(); ymax[i] = yi.max()
        self._centroids = np.column_stack([cx, cy])
        self._emin_x, self._emax_x = xmin, xmax
        self._emin_y, self._emax_y = ymin, ymax
        self._cent_tree = cKDTree(self._centroids)

        # time
        self._mt = np.asarray(self.dfsu.GetDateTimes()).astype("datetime64[ns]")

        # CRS (use MIKE token/WKT → pyproj CRS). Hemisphere set explicitly.
        proj_token = self.dfsu.Projection.WKTString
        self._mesh_crs = crs_from_mike_token(proj_token, hemisphere="south")
        self._is_geographic = self._mesh_crs.is_geographic


    # ---------- props ----------
    @property
    def n_items(self) -> int: return len(self.dfsu.ItemInfo)
    @property
    def n_timesteps(self) -> int: return int(self.dfsu.NumberOfTimeSteps)
    @property
    def n_elements(self) -> int: return int(self.dfsu.NumberOfElements)
    @property
    def model_times(self) -> np.ndarray: return self._mt
    @property
    def mesh_crs(self): return self._mesh_crs
    @property
    def is_geographic(self) -> bool: return self._is_geographic

    @property
    def et(self) -> np.ndarray | None:
        """(ne,3) tri connectivity if triangular else None."""
        if self.is_triangular:
            return np.stack(self._elt_nodes, axis=0)
        return None

    def elements_nodes(self):
        """(list_of_arrays_0based, nverts_per_element)."""
        return self._elt_nodes, self._nverts

    # ---------- CRS helpers ----------
    def _make_transformer(self, from_crs: str | CRS, to_mesh: bool):
        src = CRS.from_user_input(from_crs) if to_mesh else self._mesh_crs
        dst = self._mesh_crs if to_mesh else CRS.from_user_input(from_crs)
        return Transformer.from_crs(src, dst, always_xy=True)

    def _to_mesh_xy(self, x, y, input_crs: str | None):
        if input_crs is None:
            return np.asarray(x, float), np.asarray(y, float)
        tr = self._make_transformer(input_crs, to_mesh=True)
        X, Y = tr.transform(np.asarray(x, float), np.asarray(y, float))
        return X, Y

    def _from_mesh_xy(self, x, y, output_crs: str | None):
        if output_crs is None:
            return np.asarray(x, float), np.asarray(y, float)
        tr = self._make_transformer(output_crs, to_mesh=False)
        X, Y = tr.transform(np.asarray(x, float), np.asarray(y, float))
        return X, Y

    # ---------- internals ----------
    @staticmethod
    def _bbox_from_points(xq, yq, pad):
        xq = np.asarray(xq, float).ravel(); yq = np.asarray(yq, float).ravel()
        return float(np.nanmin(xq)-pad), float(np.nanmax(xq)+pad), float(np.nanmin(yq)-pad), float(np.nanmax(yq)+pad)

    def _select_elements_in_bbox_centroid(self, xmin, xmax, ymin, ymax) -> np.ndarray:
        cx, cy = self._centroids[:, 0], self._centroids[:, 1]
        keep = (cx >= xmin) & (cx <= xmax) & (cy >= ymin) & (cy <= ymax)
        idx = np.nonzero(keep)[0]
        if idx.size == 0:
            raise ValueError("No elements in bbox.")
        return idx

    def _roi_centroids(self, elem_idx):
        return self._centroids[np.asarray(elem_idx, int)]

    def _nearest_elements_by_centroid(self, xq, yq, elem_idx):
        pts = np.column_stack([np.asarray(xq, float).ravel(), np.asarray(yq, float).ravel()])
        C = self._centroids[np.asarray(elem_idx, int)]
        tree = cKDTree(C)
        j = tree.query(pts, k=1, workers=-1)[1]
        return np.asarray(elem_idx, int)[j]

    def _bracket_times(self, t):
        mt = self._mt
        t = np.asarray(t, dtype="datetime64[ns]").ravel()
        after = np.searchsorted(mt, t, side="right")
        before = np.clip(after - 1, 0, mt.size - 1)
        after = np.clip(after, 0, mt.size - 1)
        return before, after

    # ---------- public ----------
    def locate_elements(self, xq, yq, pad: float = 0.01, *, input_crs: str | None = None):
        """Return nearest-element id for each (xq,yq). pad in units of input_crs or mesh CRS."""
        Xq, Yq = self._to_mesh_xy(xq, yq, input_crs)
        xmin, xmax, ymin, ymax = self._bbox_from_points(Xq, Yq, pad)
        elems = self._select_elements_in_bbox_centroid(xmin, xmax, ymin, ymax)
        return self._nearest_elements_by_centroid(Xq, Yq, elems)

    def extract_transect(self, xq, yq, t, item_number: int, pad: float = 0.01, *, input_crs: str | None = None):
        """Nearest centroid element → linear time interpolation. Returns (data, times, elem_idx)."""
        if not (1 <= item_number <= self.n_items):
            raise ValueError(f"item_number must be 1..{self.n_items}")

        Xq, Yq = self._to_mesh_xy(xq, yq, input_crs)
        t = np.asarray(t, dtype="datetime64[ns]").ravel()
        if Xq.size != Yq.size or Xq.size != t.size:
            raise ValueError("xq, yq, t must have equal length.")

        xmin, xmax, ymin, ymax = self._bbox_from_points(Xq, Yq, pad)
        elems = self._select_elements_in_bbox_centroid(xmin, xmax, ymin, ymax)
        elem_idx = self._nearest_elements_by_centroid(Xq, Yq, elems)

        before, after = self._bracket_times(t)
        need_t = np.unique(np.concatenate([before, after]))
        uniq_elems, inv_e = np.unique(elem_idx, return_inverse=True)

        slab = np.empty((need_t.size, uniq_elems.size), float)
        for k, it in enumerate(need_t):
            vals = np.asarray(self.dfsu.ReadItemTimeStep(item_number, int(it)).Data, float)
            slab[k, :] = vals[uniq_elems]

        kb = np.searchsorted(need_t, before)
        ka = np.searchsorted(need_t, after)
        v0 = slab[kb, inv_e]; v1 = slab[ka, inv_e]

        mt = self._mt
        dt = (mt[after] - mt[before]) / np.timedelta64(1, "s")
        dt = np.where(dt == 0, 1.0, dt)
        w1 = (t - mt[before]) / np.timedelta64(1, "s") / dt
        data = (1.0 - w1) * v0 + w1 * v1
        return data, t, elem_idx

    def extract_transect_idw(self, xq, yq, t, item_number: int, k: int = 6, p: float = 2.0,
                             pad: float = 0.01, *, input_crs: str | None = None):
        """IDW at (xq,yq). Time-linear per element then spatial IDW."""
        if not (1 <= item_number <= self.n_items):
            raise ValueError(f"item_number must be 1..{self.n_items}")

        Xq, Yq = self._to_mesh_xy(xq, yq, input_crs)
        t = np.asarray(t, dtype="datetime64[ns]").ravel()
        if not (Xq.size == Yq.size == t.size):
            raise ValueError("xq, yq, t must have equal length.")

        xmin, xmax, ymin, ymax = self._bbox_from_points(Xq, Yq, pad)
        cx, cy = self._centroids[:, 0], self._centroids[:, 1]
        keep = (cx >= xmin) & (cx <= xmax) & (cy >= ymin) & (cy <= ymax)
        elems_roi = np.nonzero(keep)[0]
        if elems_roi.size == 0:
            raise ValueError("No elements in ROI bbox.")

        C_roi = self._centroids[elems_roi]
        tree = cKDTree(C_roi)
        k_eff = min(k, elems_roi.size)
        d, j = tree.query(np.column_stack([Xq, Yq]), k=k_eff, workers=-1)
        if k_eff == 1:
            d = d[:, None]; j = j[:, None]
        elem_nn = elems_roi[j]

        with np.errstate(divide='ignore', invalid='ignore'):
            w = 1.0 / np.maximum(d, 1e-12) ** p
        zero = d <= 1e-12
        if np.any(zero):
            w[zero] = 0.0
            rr, cc = np.where(zero)
            w[rr, cc] = 1.0
        wsum = w.sum(axis=1, keepdims=True)
        w = np.divide(w, wsum, out=np.zeros_like(w), where=wsum > 0)

        mt = self._mt
        after = np.searchsorted(mt, t, side='right')
        before = np.clip(after - 1, 0, mt.size - 1)
        after = np.clip(after, 0, mt.size - 1)
        need_t = np.unique(np.concatenate([before, after]))

        uniq_elems, _ = np.unique(elem_nn.ravel(), return_inverse=True)
        slab = np.empty((need_t.size, uniq_elems.size), float)
        for r, it in enumerate(need_t):
            vals = np.asarray(self.dfsu.ReadItemTimeStep(item_number, int(it)).Data, float)
            slab[r, :] = vals[uniq_elems]

        col_map = {e: i for i, e in enumerate(uniq_elems)}
        col_idx = np.vectorize(col_map.get, otypes=[int])(elem_nn)

        kb = np.searchsorted(need_t, before); ka = np.searchsorted(need_t, after)
        v0 = slab[kb[:, None], col_idx]; v1 = slab[ka[:, None], col_idx]

        dt = (mt[after] - mt[before]) / np.timedelta64(1, 's')
        dt = np.where(dt == 0, 1.0, dt)
        w1t = (t - mt[before]) / np.timedelta64(1, 's') / dt
        vt = (1.0 - w1t)[:, None] * v0 + w1t[:, None] * v1

        data_idw = np.sum(w * vt, axis=1)
        return data_idw, t, elem_nn, w

    def rasterize_idw_bbox(
        self,
        xq,
        yq,
        t,
        item_number: int,
        pad: float = 0.0,           # units of input_crs or mesh CRS
        pixel_size_m: float = 10.0, # meters per pixel
        k: int = 8,
        p: float = 2.0,
        debug: bool = False,
        *,
        input_crs: str | None = None,
        output_crs: str | None = None,
    ):
        """IDW raster over a square bbox around (xq,yq). Temporal mean over [min(t), max(t)]."""
        if not (1 <= item_number <= self.n_items):
            raise ValueError(f"item_number must be 1..{self.n_items}")

        Xq, Yq = self._to_mesh_xy(xq, yq, input_crs)
        if not (np.size(Xq) > 0 and np.size(Xq) == np.size(Yq)):
            raise ValueError("xq and yq must be equal-length and non-empty.")
        t = np.asarray(t, dtype="datetime64[ns]").ravel()
        if t.size == 0:
            raise ValueError("t must be non-empty.")

        # bbox in mesh CRS, forced square
        xmin = float(np.nanmin(Xq) - pad); xmax = float(np.nanmax(Xq) + pad)
        ymin = float(np.nanmin(Yq) - pad); ymax = float(np.nanmax(Yq) + pad)
        cx = 0.5 * (xmin + xmax); cy = 0.5 * (ymin + ymax)
        L = max(xmax - xmin, ymax - ymin); h = 0.5 * L
        xmin, xmax, ymin, ymax = cx - h, cx + h, cy - h, cy + h

        # width/height in meters
        if self._is_geographic:
            lat0 = 0.5 * (ymin + ymax)
            phi = np.deg2rad(lat0)
            m_per_deg_lat = 111132.92 - 559.82*np.cos(2*phi) + 1.175*np.cos(4*phi) - 0.0023*np.cos(6*phi)
            m_per_deg_lon = 111412.84*np.cos(phi) - 93.5*np.cos(3*phi) + 0.118*np.cos(5*phi)
            width_m = max(0.0, (xmax - xmin) * m_per_deg_lon)
            height_m = max(0.0, (ymax - ymin) * m_per_deg_lat)
        else:
            width_m = max(0.0, xmax - xmin)
            height_m = max(0.0, ymax - ymin)

        # select ROI elements (AABB intersection), expand if too few
        def _expand_square(x0, x1, y0, y1, scale):
            cx0 = 0.5*(x0+x1); cy0 = 0.5*(y0+y1)
            Ls = max(x1-x0, y1-y0) * scale; hh = 0.5*Ls
            return cx0-hh, cx0+hh, cy0-hh, cy0+hh

        tries = 0
        target_min = max(10, k)
        while True:
            intersects = (
                (self._emax_x >= xmin) & (self._emin_x <= xmax) &
                (self._emax_y >= ymin) & (self._emin_y <= ymax)
            )
            elems_roi = np.nonzero(intersects)[0]
            if elems_roi.size >= target_min or tries >= 6:
                break
            xmin, xmax, ymin, ymax = _expand_square(xmin, xmax, ymin, ymax, 1.6)
            if self._is_geographic:
                lat0 = 0.5 * (ymin + ymax)
                phi = np.deg2rad(lat0)
                m_per_deg_lat = 111132.92 - 559.82*np.cos(2*phi) + 1.175*np.cos(4*phi) - 0.0023*np.cos(6*phi)
                m_per_deg_lon = 111412.84*np.cos(phi) - 93.5*np.cos(3*phi) + 0.118*np.cos(5*phi)
                width_m = max(0.0, (xmax - xmin) * m_per_deg_lon)
                height_m = max(0.0, (ymax - ymin) * m_per_deg_lat)
            else:
                width_m = max(0.0, xmax - xmin)
                height_m = max(0.0, ymax - ymin)
            tries += 1
        if elems_roi.size == 0:
            raise ValueError("No elements in bbox after expansion.")

        # time window
        mt = self._mt
        tmin = t.min(); tmax = t.max()
        tidx = np.where((mt >= tmin) & (mt <= tmax))[0]
        if tidx.size == 0:
            before, after = self._bracket_times(t)
            tidx = np.unique(np.concatenate([before, after]))
        if tidx.size == 0:
            raise ValueError("No model timesteps intersect the provided time range.")

        vals = np.empty((tidx.size, elems_roi.size), float)
        for r, it in enumerate(tidx):
            all_e = np.asarray(self.dfsu.ReadItemTimeStep(item_number, int(it)).Data, float)
            vals[r, :] = all_e[elems_roi]
        elem_mean = np.nanmean(vals, axis=0)

        # grid in mesh CRS
        nx_pix = max(2, int(np.ceil(width_m / pixel_size_m))) if width_m > 0 else 2
        ny_pix = max(2, int(np.ceil(height_m / pixel_size_m))) if height_m > 0 else 2
        dx = (xmax - xmin) / nx_pix if nx_pix > 0 else 0.0
        dy = (ymax - ymin) / ny_pix if ny_pix > 0 else 0.0
        gx = xmin + (np.arange(nx_pix) + 0.5) * dx
        gy = ymin + (np.arange(ny_pix) + 0.5) * dy
        Xm, Ym = np.meshgrid(gx, gy)

        # IDW in space (centroids in mesh CRS)
        C = self._centroids[elems_roi]
        tree = cKDTree(C)
        k_eff = min(k, elems_roi.size)
        d, j = tree.query(np.column_stack([Xm.ravel(), Ym.ravel()]), k=k_eff, workers=-1)
        if k_eff == 1:
            d = d[:, None]; j = j[:, None]
        with np.errstate(divide="ignore", invalid="ignore"):
            w = 1.0 / np.maximum(d, 1e-12) ** p
        zero = d <= 1e-12
        if np.any(zero):
            w[zero] = 0.0
            rr, cc = np.where(zero)
            w[rr, cc] = 1.0
        wsum = w.sum(axis=1, keepdims=True)
        w = np.divide(w, wsum, out=np.zeros_like(w), where=wsum > 0)

        Z = np.sum(w * elem_mean[j], axis=1).reshape(Ym.shape)

        # transform grid back if requested
        if output_crs is None:
            output_crs = input_crs
        if output_crs is not None:
            Xo, Yo = self._from_mesh_xy(Xm, Ym, output_crs)
        else:
            Xo, Yo = Xm, Ym

        if debug:
            print(f"[mesh CRS {'geographic' if self._is_geographic else 'projected'}]")
            print(f"[grid] nx={nx_pix} ny={ny_pix}")

        extent_mesh = (xmin, xmax, ymin, ymax)
        return Xo, Yo, Z, extent_mesh

    def rasterize_bbox_timeseries(
        self,
        item_number: int,
        bbox: tuple[float, float, float, float],
        pixel_size_m: float = 25.0,
        k: int = 12,
        p: float = 2.0,
        times=None,
        pad: float = 0.0,
        as_stack: bool = True,
        *,
        input_crs: str | None = None,
        output_crs: str | None = None,
    ):
        """Rasterize fixed bbox for every timestep. bbox in input_crs or mesh CRS."""
        x0, x1, y0, y1 = map(float, bbox)
        xq = np.array([x0, x1], float)
        yq = np.array([y0, y1], float)

        t_ns = np.asarray(self._mt if times is None else times, dtype="datetime64[ns]")
        if t_ns.size == 0:
            raise ValueError("Empty time sequence.")

        frames = []
        X = Y = extent = None
        for ti in t_ns:
            Xg, Yg, Zg, ext = self.rasterize_idw_bbox(
                xq=xq,
                yq=yq,
                t=np.asarray([ti], dtype="datetime64[ns]"),
                item_number=item_number,
                pad=pad,
                pixel_size_m=pixel_size_m,
                k=k,
                p=p,
                debug=False,
                input_crs=input_crs,
                output_crs=output_crs,
            )
            if X is None:
                X, Y, extent = Xg, Yg, ext
            frames.append(np.asarray(Zg, float))

        frames = np.stack(frames, axis=0) if as_stack else frames
        return {"X": X, "Y": Y, "extent": extent, "times": t_ns, "frames": frames}

        
    
if __name__ == "__main__":
    
    model_fpath = r"C:/Users/anba/OneDrive - DHI/Desktop/Documents/GitHub/PlumeTrack/tests/Model Files/MT20241002.dfsu"
    fm_model = DfsuUtils2D(model_fpath)  # provides extract_transect_idw(...)

    
    model_fpath = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/test2.dfsu'
    fm_model = DfsuUtils2D(model_fpath)  # provides extract_transect_idw(...)

