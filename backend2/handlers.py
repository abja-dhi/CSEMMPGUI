import numpy as np
import warnings

class ErrorHandler:
    @staticmethod
    def x_y_xy_check(x, y, xy) -> tuple[int, str]:
        """
        Check if x, y, or xy is provided and return the appropriate values.
        
        Args:
            x (np.ndarray): X coordinates.
            y (np.ndarray): Y coordinates.
            xy (np.ndarray): Combined X and Y coordinates.
        
        Returns:
            Error code = 0 if checks are successful, -1 if checks fail.
        """
        if xy is not None:
            if isinstance(xy, list):
                xy = np.array(xy)
            if len(xy.shape) != 2:
                code = -1
                error = "xy must be a 2D array with shape (n_points, 2)."
                return code, error
            if xy.shape[1] != 2:
                code = -1
                error = "xy must have two columns for x and y coordinates."
                return code, error
            if x is not None or y is not None:
                warnings.warn(
                    "Both x, y and xy provided; using xy coordinates.",
                    RuntimeWarning,
                    stacklevel=2,
                )
        else:
            if x is None or y is None:
                code = -1
                error = "Either xy must be provided or both x and y must be provided."
                return code, error
            if isinstance(x, list):
                x = np.array(x)
            if isinstance(y, list):
                y = np.array(y)
            if x.shape != y.shape:
                code = -1
                error = "x and y must have the same shape."
                return code, error
            if len(x.shape) > 1 and x.shape[1] != 1:
                code = -1
                error = "x must be 1D arrays or 2D arrays with a single column."
                return code, error
            if len(y.shape) > 1 and y.shape[1] != 1:
                code = -1
                error = "y must be 1D arrays or 2D arrays with a single column."
                return code, error
            if x.size == 0 or y.size == 0:
                code = -1
                error = "x and y cannot be empty."
                return code, error
        return 0, "No error"