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

