import json
import os
import numpy as np

from scipy.optimize import minimize
from .utils import make_logprob_distance, make_logprob_position


def parse_scenario(file_name):
    with open(file_name, 'r') as file:
        si_list = json.load(file)
    return si_list


def json_parser(si_list):
    """Convert SI into function that return the likelyhood of a estimation"""
    si_list_func = []

    for si_dict in si_list:
        SI_type = si_dict["SI_type"]
        features = si_dict["features"]
        if SI_type == 'distance':
            maker = make_logprob_distance
        elif SI_type == 'position':
            maker = make_logprob_position
        logprob_func = maker(**features)
        si_list_func.append(logprob_func)

    return si_list_func


def compute_positions(si_list, nb_points):
    """
    Return the most likely position considering the si_list and the global logprob function

    Args:
        si_list(list of dict): the soft information
        nb_points: number of points

    """
    si_list_func = json_parser(si_list)

    def global_logprob(points):
        """Returns the logprob of a given set of points under all SI"""
        return np.sum([
            si_func(points) for si_func in si_list_func])

    points = np.random.rand(nb_points, 2)
    x0 = np.ravel(points)

    # since we use 'minimize', we have to take the opposite
    # of the logprob (I called it unlogprob)
    def unlogprob(x):
        # x shape is (3*nb_points,)
        points = x.reshape(nb_points, 2)
        return -global_logprob(points)

    # Finds the minima of the func 'unlogprob'
    # which is the most likely distribution of points
    estimated_x = minimize(unlogprob, x0, method='CG').x

    positions = estimated_x.reshape(nb_points, 2)

    return positions, global_logprob
