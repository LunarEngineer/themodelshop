"""Tools for monitoring convergence of arrays

The following tools are used to estimate convergence in arrays.
TODO: Does this need to be here? This was part of a project that I wound up *not* using.
"""
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html

import numpy as np
import pandas as pd

from scipy.linalg import lstsq
from typing import Union

def check_for_convergence(
    x: Union[pd.Series,np.ndarray],
    buffer_size: Union[int,float] = .05
):
    """Checks for convergence in one-dimensional array x.

    The way that this checks for convergence is by using a
    probabilistic model to track the residuals of a moving target.
    The residuals will define the size of the distribution
    surrounding the point estimate and convergence will be satisfied
    when the point estimate and the size of the probability envelope
    are stabilized.

    TODO: Add in PyArrow
    """
    ################################################################
    # Bookkeeping
    ################################################################
    # 1) Check for assumptions
    if not isinstance(x, (pd.Series,np.ndarray)):
        # Is X one of the types we can work with?
        errmsg = "Convergence check only valid for Numpy Array / Pandas Series"
        raise TypeError(errmsg)
    if not isinstance(buffer_size, (int,float)):
        errmsg = "Buffer size type mismatch. Expecting integer or float."
        raise TypeError(errmsg)
    # 2) Check for shape
    if x.ndim > 1:
        if (x.shape[1] > 1) or x.ndim > 2:
            # Make a new shape exception
            raise Exception("Expecting a one-dimensional array.")
    # 3) Define the buffer size
    if isinstance(buffer_size, float):
        buffer_size = round(buffer_size*x.shape[0])
    # 4) Sanity check for buffer size
    if buffer_size > x.shape[0]:
        raise Exception("Buffer size must be smaller than array size")
    # 5) Calculate the smoothed gradient of the array
    d_1 = pd.Series(
        np.abs(
            np.gradient(x)
        )
    ).ewm(
        span=buffer_size,
        min_periods=0,
        adjust=False
    ).mean()
    # We also have d_2, a smoothed estimate of the second derivative.
    d_2 = pd.Series(
        np.abs(
            np.gradient(d_1)
        )
    ).ewm(
        span=buffer_size,
        min_periods=0,
        adjust=False
    ).mean()
    # Now we're going to fit a first order least squares
    #   curve to the last buffer elements of d_1 and d_2.
    # These can be used to calculate a running estiamte.
    M = np.arange(buffer_size).reshape(-1,1)**[0, 1]
    p_1, res_1, _, _ = lstsq(M, d_1.tail(buffer_size))
    p_2, res_2, _, _ = lstsq(M, d_2.tail(buffer_size))
    # This is a short term fix.
    return abs(p_1[1]) <= .00001 and abs(p_2[1]) <= .00001
