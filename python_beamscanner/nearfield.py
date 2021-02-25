#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports should be grouped into:
# Standard library imports
# Related third party imports
# Local application / relative imports
# in that order

# Standard library
from typing import Tuple

# Third party
import numpy as np
from scipy.interpolate import griddata


# Relative


class ScanData(object):
    """
    This object holds basic data from a single polarization scan.

    Parameters
    ----------
    N/A

    Attributes
    ----------
    s21: ndarray
        Array of complex transmission values in the 2d scan.
    cal_data: ndarray
        Array of calibration values for the 2d scan points.
    """

    def __init__(self):
        self.__x_limits = None
        self.__y_limits = None
        self.__x_points = None
        self.__y_points = None
        self.__x_step = None
        self.__y_step = None
        self.s21 = None
        self.cal_data = None

    @staticmethod
    def kaiser_smooth(x, beta, window_len):
        """Apply Kaiser window smoothing to x.

        Uses the numpy Kaiser window function.
            See: https://numpy.org/doc/stable/reference/generated/numpy.kaiser.html

        Parameters
        ----------
        x: ndarray
            input data
        beta: float
            shape parameter for Kaiser window.
        window_len: int
            size of the window to apply.

        Returns
        -------
        y : array
            Array of data smoothed by the Kaiser window"""

        # extending the data at beginning and at the end
        # to apply the window at the borders
        s = np.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
        w = np.kaiser(window_len, beta)
        y = np.convolve(w / w.sum(), s, mode='same')
        return y[window_len - 1:-window_len + 1]

    def load_csv_data(self, file_like, cal_table=True, cal_smooth=None):
        """
        Load scan data from a CSV file, similar to that output by the
        current (02/22/2021) beamscanner application.

        Data in the file is assumed to consist of columns of points with the following
        rows:
        | x_position | y_position | re(trans) | im(trans) | re(ref) | im(ref) |

        The x,y,s21 points are grid interpolated to account for raster scanning etc.

        If table is True:
            The fifth and sixth columns of the file are read as reference values taken
            throughout thescan process, once per y value

        Parameters
        ----------
        file_like: file
            CSV file_like object containing the scan data
        cal_table: bool
            Flag whether the file contains reference measurements
        cal_smooth: int
            Window over which to smooth the reference data
        """
        data = np.loadtxt(file_like, delimiter=",")

        # get the set of unique x and y values.  We assume that the control system is
        # reliable enough that x and y positions from the motion stage are repeatable,
        # so that the number of unique x and y values is equal to the number of x and y
        # positions in a rectangular scan grid. Note that this isn't the same as
        # assuming that the grid is regularly spaced.
        x_in_vals = np.unique(data[:, 0])
        y_in_vals = np.unique(data[:, 1])

        self.__x_points = len(x_in_vals)
        self.__y_points = len(y_in_vals)
        self.__x_step = np.ptp(x_in_vals) / (self.__x_points - 1)
        self.__y_step = np.ptp(y_in_vals) / (self.__y_points - 1)
        self.__x_limits = [np.amin(x_in_vals), np.amax(x_in_vals)]
        self.__y_limits = [np.amin(y_in_vals), np.amax(y_in_vals)]

        # get the input complex transmission
        s_in_vals = data[:, 2] + complex(0, 1) * data[:, 3]

        x_in_grid, y_in_grid = np.meshgrid(x_in_vals, y_in_vals)
        x_grid, y_grid = self.xy_grids

        s_in_grid = np.reshape(s_in_vals, x_in_grid.shape)

        if cal_table:
            if cal_smooth:
                cal_vals_re = self.kaiser_smooth(data[:, 4], 1.0, cal_smooth)
                cal_vals_im = self.kaiser_smooth(data[:, 5], 1.0, cal_smooth)
            else:
                cal_vals_re = data[:, 4]
                cal_vals_im = data[:, 5]
            cal_in_vals = cal_vals_re + complex(0, 1) * cal_vals_im

            cal_in_grid = np.reshape(cal_in_vals, x_in_grid.shape)

            self.cal_data = griddata((x_in_grid.flatten(), y_in_grid.flatten()),
                                     cal_in_grid.flatten(),
                                     (x_grid, y_grid), method="linear")

        self.s21 = griddata((x_in_grid.flatten(), y_in_grid.flatten()),
                            s_in_grid.flatten(),
                            (x_grid, y_grid), method="linear")

    @property
    def x_limits(self) -> Tuple[float]:
        """
        x_limits: tuple of floats
            The x limit values stored in a tuple in (min_x, max_x)
            order.
        """
        return self.__x_limits

    @property
    def y_limits(self) -> Tuple[float]:
        """
        y_limits: tuple of floats
            The y limit values stored in a tuple in (min_y, max_y)
            order.
        """
        return self.__y_limits

    @property
    def x_points(self) -> int:
        """
        x_points: int
            The number of x values.
        """
        return self.__x_points

    @property
    def y_points(self) -> int:
        """
        y_points: int
            The number of y values.
        """
        return self.__y_points

    @property
    def x_step(self) -> float:
        """
        x_step: float
            The step between adjacent x values.
        """
        return self.__x_step

    @property
    def y_step(self) -> float:
        """
        x_step: float
            The step between adjacent y values.
        """
        return self.__y_step

    @property
    def x_values(self) -> np.ndarray:
        """
        x_values: ndarray
            The x values of the points in the scan
        """
        return np.linspace(self.__x_limits[0], self.__x_limits[1], self.__x_points)

    @property
    def y_values(self) -> np.ndarray:
        """
        y_values: ndarray
            The y values of the points in the scan
        """
        return np.linspace(self.__y_limits[0], self.__y_limits[1], self.__y_points)

    @property
    def xy_grids(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        xy_grids: Tuple of ndarrays
            meshgrid grids of the x and y values
        """
        return np.meshgrid(self.x_values, self.y_values)


class Nearfield(object):
    """
    This object holds the nearfield data from a single beamscanner run. It loads
    beamscanner data from a variety of formats, and contains the necessary code to
    convert to farfield patterns and to plot the nearfield and farfield scan data

    Parameters
    ----------
    N/A

    Attributes
    ----------
    cross_pol: bool
        flag for the availability of cross-polarization data, to be used in processing
        and plotting. Set when cross-polarization data is loaded.
    """

    # Static methods are available to the user regardless of if they have initialized
    # an instance of the class. They are useful when you have small portions of code
    # that while relevant to the class may not depend on entire class state.
    # In this case, this function isn't incredibly valuable outside of the usage of
    # this class and therefore we use the "Python" standard of prefixing the method
    # with an underscore.
    @staticmethod
    def spherical_to_cartesian(r, theta, phi):
        """
        Converts spherical coordinates to cartesian coordinates.

        Parameters
        ----------
        r: float or ndarray
            The radius/norm of the coordinates
        theta: float or ndarray
            The angle :math:`\\theta`
        phi: float or ndarray
            The angle :math:`\\phi`

        Returns
        -------
        x: float or array
            .. math:: x = r \\sin{\\theta}\\cos{\\phi}
        y: float or array
            .. math:: y = r \\sin{\\theta}\\sin{\\phi}
        z: float or array
            .. math:: z = r \\cos{\\theta}
        """
        return (
            r * np.sin(theta) * np.cos(phi),
            r * np.sin(theta) * np.sin(phi),
            r * np.cos(theta)
        )

    def __init__(self):
        self.cross_pol = False

    # Representation's (reprs) are useful when using interactive Python sessions or
    # when you log an object. They are the shorthand of the object state. In this case,
    # our string method provides a good representation.
    def __repr__(self):
        return str(self)
