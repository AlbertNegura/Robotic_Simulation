"""
Various mathematical helper functions.
"""
import numpy as np

def angle(v1,v2):
    """
    Returns the angle between two vectors.
    :param v1: first vector as a numpy array
    :param v2: second vector as a numpy array
    :return: the angle between vectors
    """
    return np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))

def rotate(origin, point_of_rotation, angle_of_rotation):
    """
    Returns the coordinates of a 2D vector after it has been rotated.
    :param origin: point of origin
    :param point_of_rotation: point about which to rotate the object - can be point of origin to make object spin in place
    :param angle_of_rotation: angle about which to rotate the object
    :return: the new point
    """
    pass