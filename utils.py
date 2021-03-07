"""
Robotic Simulation Software Various mathematical helper functions.
Authors:
Julien Havel
Kamil Inglot
Albert Negura
Sergi Nogues Farres
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
    return np.linalg.norm(np.subtract(a,b))

def intersection(line1, line2):
    """

    :param line1: A 2d numpy array representing a line with a start point and an end point.
    :param line2: A 2d numpy array representing a line with a start point and an end point.
    :return: The point where the two lines intersect, if they intersect
    """

    [[x1, y1], [x2, y2]] = line1
    [[x3, y3], [x4, y4]] = line2[:2][:]

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
        robot.position[0]=float(a_min[0])
    if y<a_min[1]:
        robot.position[1]=float(a_min[1])
    if x>a_max[0]:
        robot.position[0]=float(a_max[0])
    if y>a_max[1]:
        robot.position[1]=float(a_max[1])


def clip_value(a, a_min, a_max):
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
    retx = x
    rety = y
    if x<a_min[0]:
        retx=a_min[0]
    if y<a_min[1]:
        rety=a_min[1]
    if x>a_max[0]:
        retx=a_max[0]
    if y>a_max[1]:
        rety=a_max[1]
    return [retx,rety]


def circle_line_tangent_point(wall_init, wall_end, P, R, tol=1e-9):
    """
    :param wall_init: starting point of the wall (x,y)
    :param wall_end: end point of the wall (x,y)
    :param P: origin of the circle (x,y)
    :param R: radius of the circle
    :return: returns the intersection point between the wall and the perpendicular line to the wall that passes through P
    """

    (p1x,p1y) = wall_init
    (p2x,p2y) = wall_end
    (cx,cy) = P

    (x1,y1) = (p1x-cx, p1y-cy)
    (x2,y2) = (p2x-cx, p2y-cy)

    dx,dy = (x2-x1), (y2-y1)
    dr = (dx**2+dy**2)**.5
    big_d = x1*y2-x2*y1
    disc = R**2*dr**2-big_d**2

    if disc < 0:
        return None

    else:
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * disc**.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * disc**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
        intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(disc) <= tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections


def circle_intersect(line1, line2, radius, angle):
    intersection_point = intersection(line1, line2)
    if intersection_point is None:
        # work in radians
        angle = np.radians(angle)
        x = line2[0][0] + np.sin(angle) * radius
        y = line2[0][1] + np.cos(angle) * radius
        x2 = line2[1][0] + np.sin(angle) * radius
        y2 = line2[1][1] + np.cos(angle) * radius
        intersection_point = intersection(line1,[[x,y],[x2,y2]])
        if intersection_point is None:
            x = line2[0][0] - np.sin(angle) * radius
            y = line2[0][1] - np.cos(angle) * radius
            x2 = line2[1][0] - np.sin(angle) * radius
            y2 = line2[1][1] - np.cos(angle) * radius
            intersection_point = intersection(line1,[[x,y],[x2,y2]])
    return intersection_point


def sigmoid(z):
    return 1/(1 + np.exp(-z))

def tanh(z):
    ez_poz = np.exp(z)
    ez_neg = np.exp(-z)
    ez = (ez_poz - ez_neg)/(ez_poz + ez_neg)
    return ez
