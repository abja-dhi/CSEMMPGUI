# -*- coding: utf-8 -*-
# 2D-only DFSU utilities with fast Delaunay locator (SciPy). mikecore-only I/O.

from mikecore.DfsuFile import DfsuFile
import numpy as np
from scipy.spatial import cKDTree



class DfsuUtils2D:
    """2D triangular DFSU utilities. ROI by bbox(xq,yq). Nearest-element via centroids."""

    def __init__(self, fname: str) -> None:
        self.fname = fname
        self.dfsu = DfsuFile.Open(self.fname)

        # enforce 2D
        if int(getattr(self.dfsu, "NumberOfLayers", 0) or 0) != 0:
            raise ValueError("2D DFSU required (NumberOfLayers == 0).")

        # geometry
        self._x = np.asarray(self.dfsu.X, float)
        self._y = np.asarray(self.dfsu.Y, float)
        self._et = (np.stack(self.dfsu.ElementTable, axis=1).T - 1).astype(int)  # (ne,3)
        if self._et.shape[1] != 3:
            raise ValueError("Mesh must be triangular.")

        # time
        self._mt = np.asarray(self.dfsu.GetDateTimes()).astype("datetime64[ns]")

    # ---- basic props
    @property
    def n_items(self) -> int: return len(self.dfsu.ItemInfo)
    @property
    def n_timesteps(self) -> int: return int(self.dfsu.NumberOfTimeSteps)
    @property
    def n_elements(self) -> int: return int(self.dfsu.NumberOfElements)
    @property
    def model_times(self) -> np.ndarray: return self._mt
    @property
    def et(self) -> np.ndarray: return self._et

    # ---- internals
    @staticmethod
    def _bbox_from_points(xq, yq, pad):
        xq = np.asarray(xq, float).ravel(); yq = np.asarray(yq, float).ravel()
        return float(np.nanmin(xq)-pad), float(np.nanmax(xq)+pad), float(np.nanmin(yq)-pad), float(np.nanmax(yq)+pad)

    def _select_elements_in_bbox_centroid(self, xmin, xmax, ymin, ymax) -> np.ndarray:
        X = self._x[self._et]; Y = self._y[self._et]
        cx = X.mean(axis=1); cy = Y.mean(axis=1)
        keep = (cx >= xmin) & (cx <= xmax) & (cy >= ymin) & (cy <= ymax)
        idx = np.nonzero(keep)[0]
        if idx.size == 0:
            raise ValueError("No elements in bbox.")
        return idx

    def _roi_centroids(self, elem_idx):
        tri = self._et[elem_idx]
        cx = self._x[tri].mean(axis=1)
        cy = self._y[tri].mean(axis=1)
        return np.column_stack([cx, cy])  # (n_roi,2)

    def _nearest_elements_by_centroid(self, xq, yq, elem_idx):
        pts = np.column_stack([np.asarray(xq, float).ravel(), np.asarray(yq, float).ravel()])
        C = self._roi_centroids(elem_idx)
        tree = cKDTree(C)
        j = tree.query(pts, k=1, workers=-1)[1]        # indices into ROI arrays
        return np.asarray(elem_idx, int)[j]            # original element ids

    def _bracket_times(self, t):
        mt = self._mt
        t = np.asarray(t, dtype="datetime64[ns]").ravel()
        after = np.searchsorted(mt, t, side="right")
        before = np.clip(after - 1, 0, mt.size - 1)
        after = np.clip(after, 0, mt.size - 1)
        return before, after

    # ---- public
    def locate_elements(self, xq, yq, pad: float = 0.01):
        """Return nearest-element (by centroid) for each (xq,yq)."""
        xmin, xmax, ymin, ymax = self._bbox_from_points(xq, yq, pad)
        elems = self._select_elements_in_bbox_centroid(xmin, xmax, ymin, ymax)
        return self._nearest_elements_by_centroid(xq, yq, elems)

    def extract_transect(self, xq, yq, t, item_number: int, pad: float = 0.01):
        """
        ROI from bbox(xq,yq) → nearest centroid element → linear time interpolation.
        Returns: data (n,), times (n,), elem_idx (n,)
        """
        if not (1 <= item_number <= self.n_items):
            raise ValueError(f"item_number must be 1..{self.n_items}")
        xq = np.asarray(xq, float).ravel()
        yq = np.asarray(yq, float).ravel()
        t = np.asarray(t, dtype="datetime64[ns]").ravel()
        if not (xq.size == yq.size == t.size):
            raise ValueError("xq, yq, t must have equal length.")

        # map points → nearest centroid element within ROI
        xmin, xmax, ymin, ymax = self._bbox_from_points(xq, yq, pad)
        elems = self._select_elements_in_bbox_centroid(xmin, xmax, ymin, ymax)
        elem_idx = self._nearest_elements_by_centroid(xq, yq, elems)

        # minimal I/O: unique timesteps and elements
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
                             pad: float = 0.01):
        """
        Inverse-distance weighted interpolation at each (xq,yq).
        - ROI from bbox(xq,yq) via centroid selection
        - k nearest element centroids per point
        - Linear time interpolation per element, then IDW blend
    
        Returns
        -------
        data_idw : (n_points,) float
        times    : datetime64[ns]
        elem_nn  : (n_points, k) int   # neighbor element ids used
        weights  : (n_points, k) float # normalized IDW weights
        """
        import numpy as np
        from scipy.spatial import cKDTree
    
        if not (1 <= item_number <= self.n_items):
            raise ValueError(f"item_number must be 1..{self.n_items}")
    
        xq = np.asarray(xq, float).ravel()
        yq = np.asarray(yq, float).ravel()
        t   = np.asarray(t,  dtype="datetime64[ns]").ravel()
        if not (xq.size == yq.size == t.size):
            raise ValueError("xq, yq, t must have equal length.")
        n = xq.size
    
        # --- ROI by bbox on centroids
        def _bbox_from_points(xq, yq, pad):
            return float(np.nanmin(xq)-pad), float(np.nanmax(xq)+pad), float(np.nanmin(yq)-pad), float(np.nanmax(yq)+pad)
        xmin,xmax,ymin,ymax = _bbox_from_points(xq,yq,pad)
    
        Xtri = self._x[self._et]             # (ne,3)
        Ytri = self._y[self._et]
        Cx   = Xtri.mean(axis=1)              # centroids
        Cy   = Ytri.mean(axis=1)
        keep = (Cx>=xmin)&(Cx<=xmax)&(Cy>=ymin)&(Cy<=ymax)
        elems_roi = np.nonzero(keep)[0]
        if elems_roi.size == 0:
            raise ValueError("No elements in ROI bbox.")
    
        # --- KDTree on ROI centroids
        C_roi = np.column_stack([Cx[elems_roi], Cy[elems_roi]])
        tree  = cKDTree(C_roi)
        k_eff = min(k, elems_roi.size)
        d, j = tree.query(np.column_stack([xq,yq]), k=k_eff, workers=-1)  # d:(n,k_eff), j:(n,k_eff)
        if k_eff == 1:
            d = d[:,None]; j = j[:,None]
        elem_nn = elems_roi[j]  # (n, k_eff) original element ids
    
        # --- IDW weights (handle zero-distance hits)
        with np.errstate(divide='ignore', invalid='ignore'):
            w = 1.0 / np.maximum(d, 1e-12)**p
        zero_hit = (d <= 1e-12)
        if np.any(zero_hit):
            # if a query coincides with a centroid, make that neighbor weight=1 and others 0
            w[zero_hit] = 0.0
            rows, cols = np.where(zero_hit)
            w[rows, cols] = 1.0
        w_sum = w.sum(axis=1, keepdims=True)
        w = np.divide(w, w_sum, out=np.zeros_like(w), where=w_sum>0)  # normalize
    
        # --- time bracketing
        mt = self._mt
        after  = np.searchsorted(mt, t, side='right')
        before = np.clip(after-1, 0, mt.size-1)
        after  = np.clip(after,   0, mt.size-1)
        need_t = np.unique(np.concatenate([before, after]))
    
        # --- minimal I/O over unique elements (neighbors only)
        uniq_elems, inv_cols = np.unique(elem_nn.ravel(), return_inverse=True)  # columns for slab
        slab = np.empty((need_t.size, uniq_elems.size), float)
        for r, it in enumerate(need_t):
            vals = np.asarray(self.dfsu.ReadItemTimeStep(item_number, int(it)).Data, float)
            slab[r, :] = vals[uniq_elems]
    
        # map neighbor element ids -> slab column indices
        col_map = {e:i for i,e in enumerate(uniq_elems)}
        col_idx = np.vectorize(col_map.get, otypes=[int])(elem_nn)  # (n, k_eff)
    
        # gather before/after values for each point and neighbor
        kb = np.searchsorted(need_t, before)  # (n,)
        ka = np.searchsorted(need_t, after)   # (n,)
    
        v0 = slab[kb[:,None], col_idx]  # (n, k_eff)
        v1 = slab[ka[:,None], col_idx]  # (n, k_eff)
    
        # blend in time, then IDW across neighbors
        dt = (mt[after] - mt[before]) / np.timedelta64(1, 's')
        dt = np.where(dt == 0, 1.0, dt)
        w1t = (t - mt[before]) / np.timedelta64(1, 's') / dt
        w0t = 1.0 - w1t
        vt = w0t[:,None]*v0 + w1t[:,None]*v1           # (n, k_eff)
        data_idw = np.sum(w * vt, axis=1)              # (n,)
    
        return data_idw, t, elem_nn, w
    
        
        
    def rasterize_idw_bbox(
        self,
        xq,
        yq,
        t,
        item_number: int,
        pad: float = 0.01,          # degrees
        pixel_size_m: float = 10.0, # meters per pixel
        k: int = 8,
        p: float = 2.0,
        debug: bool = False,
    ):
        """
        IDW raster over a *square* bbox around points (xq,yq). Temporal mean over [min(t), max(t)].
        Inputs X,Y are degrees. Grid resolution is meters. Output grid stays in degrees.
        """
        import numpy as np
        from scipy.spatial import cKDTree
    
        if not (1 <= item_number <= self.n_items):
            raise ValueError(f"item_number must be 1..{self.n_items}")
    
        xq = np.asarray(xq, float).ravel()
        yq = np.asarray(yq, float).ravel()
        if not (xq.size > 0 and xq.size == yq.size):
            raise ValueError("xq and yq must be equal-length and non-empty.")
        t = np.asarray(t, dtype="datetime64[ns]").ravel()
        if t.size == 0:
            raise ValueError("t must be non-empty.")
    
        # ---- 1) initial bbox in degrees (with pad), then force to PERFECT SQUARE about center
        xmin = float(np.nanmin(xq) - pad)
        xmax = float(np.nanmax(xq) + pad)
        ymin = float(np.nanmin(yq) - pad)
        ymax = float(np.nanmax(yq) + pad)
    
        cx = 0.5 * (xmin + xmax)
        cy = 0.5 * (ymin + ymax)
        width_deg  = xmax - xmin
        height_deg = ymax - ymin
        L = max(width_deg, height_deg)                       # square side in degrees
        half = 0.5 * L
        xmin, xmax = cx - half, cx + half
        ymin, ymax = cy - half, cy + half
        extent = (xmin, xmax, ymin, ymax)
    
        # meters-per-degree at mean latitude
        lat0 = 0.5 * (ymin + ymax)
        φ = np.deg2rad(lat0)
        m_per_deg_lat = 111132.92 - 559.82*np.cos(2*φ) + 1.175*np.cos(4*φ) - 0.0023*np.cos(6*φ)
        m_per_deg_lon = 111412.84*np.cos(φ) - 93.5*np.cos(3*φ) + 0.118*np.cos(5*φ)
    
        width_deg  = xmax - xmin                # == height_deg == L
        height_deg = ymax - ymin
        width_m    = max(0.0, width_deg  * m_per_deg_lon)
        height_m   = max(0.0, height_deg * m_per_deg_lat)
    
        # ---- 2) select elements (any-vertex-in-bbox) and expand *square* if needed
        tri = self._et
        Xv = self._x[tri]
        Yv = self._y[tri]
        inside = ((Xv >= xmin) & (Xv <= xmax) & (Yv >= ymin) & (Yv <= ymax)).any(axis=1)
        elems_roi = np.nonzero(inside)[0]
    
        def _expand_square(x0, x1, y0, y1, scale):
            # expand about center, keeping square in degrees
            cx = 0.5*(x0+x1); cy = 0.5*(y0+y1)
            L  = max(x1-x0, y1-y0) * scale
            h  = 0.5*L
            return cx-h, cx+h, cy-h, cy+h
    
        target_min = max(10, k)
        tries = 0
        while elems_roi.size < target_min and tries < 6:
            xmin, xmax, ymin, ymax = _expand_square(xmin, xmax, ymin, ymax, 1.6)
            extent = (xmin, xmax, ymin, ymax)
    
            lat0 = 0.5*(ymin+ymax); φ = np.deg2rad(lat0)
            m_per_deg_lat = 111132.92 - 559.82*np.cos(2*φ) + 1.175*np.cos(4*φ) - 0.0023*np.cos(6*φ)
            m_per_deg_lon = 111412.84*np.cos(φ) - 93.5*np.cos(3*φ) + 0.118*np.cos(5*φ)
    
            width_deg  = xmax - xmin
            height_deg = ymax - ymin
            width_m    = max(0.0, width_deg  * m_per_deg_lon)
            height_m   = max(0.0, height_deg * m_per_deg_lat)
    
            inside = ((Xv >= xmin) & (Xv <= xmax) & (Yv >= ymin) & (Yv <= ymax)).any(axis=1)
            elems_roi = np.nonzero(inside)[0]
            tries += 1
    
        if elems_roi.size == 0:
            raise ValueError("No elements in bbox after expansion.")
    
        tri_roi = tri[elems_roi]
        cx_e = self._x[tri_roi].mean(axis=1)
        cy_e = self._y[tri_roi].mean(axis=1)
    
        # ---- 3) time window from t (independent length)
        mt = self._mt
        tmin = t.min()
        tmax = t.max()
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
    
        # ---- 4) grid in degrees sized by requested METERS
        # Note: bbox is square in degrees; meters per degree differ in x/y, so nx,ny may differ.
        nx = max(2, int(np.ceil(width_m  / pixel_size_m))) if width_m  > 0 else 2
        ny = max(2, int(np.ceil(height_m / pixel_size_m))) if height_m > 0 else 2
        dx_deg = (xmax - xmin) / nx if nx > 0 else 0.0
        dy_deg = (ymax - ymin) / ny if ny > 0 else 0.0
        gx = xmin + (np.arange(nx) + 0.5) * dx_deg
        gy = ymin + (np.arange(ny) + 0.5) * dy_deg
        X, Y = np.meshgrid(gx, gy)  # (ny, nx) in degrees
    
        # ---- 5) IDW in space
        tree  = cKDTree(np.column_stack([cx_e, cy_e]))
        k_eff = min(k, elems_roi.size)
        d, j  = tree.query(np.column_stack([X.ravel(), Y.ravel()]), k=k_eff, workers=-1)
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
    
        Z = np.sum(w * elem_mean[j], axis=1).reshape(Y.shape)
    
        if debug:
            print(f"[bbox° square] xmin={xmin:.6f} xmax={xmax:.6f} ymin={ymin:.6f} ymax={ymax:.6f} side°={xmax-xmin:.6f}")
            print(f"[grid] nx={nx} ny={ny} dx°={dx_deg:.6g} dy°={dy_deg:.6g} pixel_size_m={pixel_size_m}")
            print(f"[roi] elements={elems_roi.size} k_eff={k_eff}")
            print(f"[time] tmin={tmin} tmax={tmax} steps={tidx.size}")
            print(f"[elem_mean] std={float(np.nanstd(elem_mean)):.6g} min={float(np.nanmin(elem_mean)):.6g} max={float(np.nanmax(elem_mean)):.6g}")
    
        return X, Y, Z, extent
    
            
    def rasterize_bbox_timeseries(
        self,
        item_number: int,
        bbox: tuple[float, float, float, float],  # (lon_min, lon_max, lat_min, lat_max)
        pixel_size_m: float = 25.0,
        k: int = 12,
        p: float = 2.0,
        times=None,
        pad: float = 0.0,
        as_stack: bool = True,
    ):
        """
        Rasterize a fixed lon/lat bounding box for every model timestep.
    
        Parameters
        ----------
        item_number : int
            DFSU item index to extract.
        bbox : tuple[float, float, float, float]
            (lon_min, lon_max, lat_min, lat_max) in degrees.
        pixel_size_m : float, optional
            Target pixel size used by IDW rasterizer (meters).
        k : int, optional
            k-nearest elements for IDW.
        p : int, optional
            IDW power.
        times : array-like of datetime-like, optional
            Times to extract. If None, uses model times if available.
        pad : float, optional
            Extra padding added to bbox in degrees.
        as_stack : bool, optional
            If True, return frames as a 3D ndarray (t, ny, nx). Else a list.
    
        Returns
        -------
        out : dict
            {
              "X": 2D ndarray of longitudes,
              "Y": 2D ndarray of latitudes,
              "extent": (xmin, xmax, ymin, ymax) in degrees,
              "times": ndarray of numpy.datetime64[ns],
              "frames": 3D ndarray (t, ny, nx) in mg/L if as_stack else list of 2D arrays,
              "units": "mg/L"
            }
        """
        import numpy as np
    
        lon_min, lon_max, lat_min, lat_max = map(float, bbox)
    
        # ---- Resolve times ----
        if times is None:
            # Common attributes/methods on DFSU helpers
            for attr in ("times", "time", "datetimes", "t"):
                if hasattr(self, attr):
                    times = getattr(self, attr)
                    break
            if times is None and hasattr(self, "get_times"):
                times = self.get_times()
            if times is None:
                raise ValueError("No times provided and model has no time sequence.")
        times = np.asarray(times)
        if np.issubdtype(times.dtype, np.datetime64):
            t_ns = times.astype("datetime64[ns]")
        else:
            t_ns = np.asarray(times, dtype="datetime64[ns]")
        if t_ns.size == 0:
            raise ValueError("Empty time sequence.")
    
        # Minimal query points define bbox; pad keeps exact bbox if 0
        xq = np.array([lon_min, lon_max], dtype=float)
        yq = np.array([lat_min, lat_max], dtype=float)
    
        frames = []
        X = Y = extent = None
    
        # ---- Rasterize per timestep ----
        for ti in t_ns:
            Xg, Yg, Zg, ext = self.rasterize_idw_bbox(
                xq=xq,
                yq=yq,
                t=np.asarray([ti], dtype="datetime64[ns]"),  # keep API consistent
                item_number=item_number,
                pad=pad,
                pixel_size_m=pixel_size_m,
                k=k,
                p=p,
                debug=False,
            )
            if X is None:
                X, Y, extent = Xg, Yg, ext
            frames.append(np.asarray(Zg, float))  # kg/m^3 -> mg/L
    
        frames = np.stack(frames, axis=0) if as_stack else frames
    
        return {
            "X": X,
            "Y": Y,
            "extent": extent,
            "times": t_ns,
            "frames": frames,
        }
        
        
    
if __name__ == "__main__":
    
    model_fpath = r'//usden1-stor.dhi.dk/Projects/61803553-05/Models/F3/2024/10. October/MT/MTD20241002.dfs2'
    mt_model = DfsuUtils2D(model_fpath)  # provides extract_transect_idw(...)

    
