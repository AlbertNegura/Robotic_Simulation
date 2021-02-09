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
    :param origin: point of origin as a [x,y] numpy array
    :param point_of_rotation: point about which to rotate the object as a [x,y] numpy array - can be point of origin to make object spin in place
    :param angle_of_rotation: angle about which to rotate the object
    :return: the new point as a numpy array
    """
    x = origin[0]
    y = origin[1]

    dx = point_of_rotation[0]
    dy = point_of_rotation[1]

    rx = x + np.cos(angle_of_rotation) * (dx-x) - np.sin(angle_of_rotation) * (dy - y)
    ry = x + np.sin(angle_of_rotation) * (dx-x) + np.cos(angle_of_rotation) * (dy - y)

    return np.array([rx, ry])

def distance_between(a,b):
    """
    Returns the absolute distance between two points.
    :param a: the first point as a [x,y] numpy array
    :param b: the second point as a [x,y] numpy array
    :return: the absolute distance between the two points
    """
    return np.linalg.norm(a-b)
