# -*- coding: utf-8 -*-
"""A set of functions that make it easy to play with soft inforamtion"""

import numpy as np
from numpy import pi, exp, sqrt, log


def normal(x, mean, std):
    """
    Normal distribution

    Args:
        x: input value
        mean: the mean of the distribution
        std: standard deviation 
    """
    return 1/(std*sqrt(2*pi))*exp(-(x-mean)**2/(2*std**2))


def dist(xa, ya, xb, yb):
    """Return the distance between a and b"""
    a = np.array((xa, ya))
    b = np.array((xb, yb))
    return np.linalg.norm(a-b)


def log_normal(x, mean, std):
    """
    Natural logarithm of a normal distribution

    Args:
        x: input value
        mean: the mean of the distribution
        std: standard deviation 
    """
    return -log(std) - (log(2) + log(pi))/2 - (x-mean)**2/(2*std**2)


def logprob_distance(xa, ya, xb, yb, measured_dist, std):
    """
    Logprob that a and b are in (xa, ya), (xb, yb) under the measured distance.

    Args:
        xa: abscissa of point a
        ya: ordinate of point a
        xb: abscissa of point b
        yb: ordinate of point b
        measured_dist: measured distance between a and b
        std: standard deviation of the measurement
    """
    points_dist = dist(xa, ya, xb, yb)
    return log_normal(points_dist, measured_dist, std)


def make_logprob_distance(idx_a, idx_b, measured_dist, std):
    """
    Make the function that return the logprob of positions under the measured distance

    Args:
        idx_a: index of point a
        idx_b: index of point b
        measured_dist: measured distance between a and b
        std: standard deviation of the measurement
    """
    def func(points):
        """
        Return the logprob of positions under the measured distance

        Args:
            points: estimated positions ([[x0, y0, h0], [x1, y1, h1], ...])
        """
        xa, ya = points[idx_a]
        xb, yb = points[idx_b]
        return logprob_distance(xa, ya, xb, yb, measured_dist, std)

    return func


def make_logprob_position(idx, measured_x, measured_y, std):
    """
    Returns the soft position information function that can be applied to the estimated positions

    Args:
        idx: index of point
        measured_x: measured abscissa
        measured_y: measured ordinate
        std: standard deviation of the measurement

    Returns:
        (function): the logSI function that takes the estimated positions of the points as input.
    """
    def func(points):
        """
        Returns log-prob of the estimated positions under the measured position.

        Args:
            points: estimated positions ([[x0, y0, h0], [x1, y1, h1], ...])
        """
        estimated_x, estimated_y = points[idx]
        return logprob_distance(estimated_x, estimated_y, measured_x, measured_y, 0, std)

    return func
