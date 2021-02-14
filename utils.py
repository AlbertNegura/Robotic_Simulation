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
    ry = y + np.sin(angle_of_rotation) * (dx-x) + np.cos(angle_of_rotation) * (dy - y)

    return np.array([rx, ry])

def rotate_line(origin, radius, angle_of_rotation):
    x = origin[0]
    y = origin[1]
    new_x = x+radius
    return rotate(origin, [new_x, y], angle_of_rotation)


def distance_between(a,b):
    """
    Returns the absolute distance between two points.
    :param a: the first point as a [x,y] numpy array
    :param b: the second point as a [x,y] numpy array
    :return: the absolute distance between the two points
    """
    return np.linalg.norm(a-b)

def intersection(line1, line2):
    """

    :param line1: A 2d numpy array representing a line with a start point and an end point.
    :param line2: A 2d numpy array representing a line with a start point and an end point.
    :return: The point where the two lines intersect, if they intersect
    """

    [[x1, y1], [x2, y2]] = line1
    [[x3, y3], [x4, y4]] = line2

    v1 = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    v2 = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
    u = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if u == 0:
        u = 1e-7

    m = v1/u
    n = -v2/u

    if not (0.0<=m<=1.0):
        return None
    if not (0.0<=n<=1.0):
        return None

    x = x1 + m * (x2-x1)
    y = y1 + m * (y2-y1)

    return [x,y]

def clip(a, a_min, a_max, robot):
    """
    Perfect inelastic collision (sets corresponding velocity component to 0). Meant only for boundary box collisions, not walls.
    :param a:
    :param a_min:
    :param a_max:
    :param robot:
    :return:
    """
    x = a[0]
    y = a[1]
    if x<a_min[0]:
        robot.position[0]=a_min[0]
        robot.velocity[0]=0
    if y<a_min[1]:
        robot.position[1]=a_min[1]
        robot.velocity[1]=0
    if x>a_max[0]:
        robot.position[0]=a_max[0]
        robot.velocity[0]=0
    if y>a_max[1]:
        robot.position[1]=a_max[1]
        robot.velocity[1]=0

def wall_collision(wall_init=(2,0), wall_end=(2,3), robot_position = [1,2], robot_orientation = 0, robot_velocity = 12, robot_radius=20):
    return None
