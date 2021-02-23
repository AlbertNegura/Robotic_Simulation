"""
Robotic Simulation Software Physics script with Physics-based interactions (i.e. collisions).
Authors:
Albert Negura
Sergi Nogues Farres
"""

import numpy as np
import utils

def resolve_wall_collision(wall_init, wall_end, P, F, R, angle, tolerance=0.):
    """
    :param wall_init: starting point of the wall (x,y)
    :param wall_end: end point of the wall (x,y)
    :param P: origin of the circle (x,y)
    :param F: force applied to the circle
    :param R: Radius of the circle
    :param angle: the angle of orientation of the circle
    :param tolerance: (optional) the radial tolerance for collision (acting as a corrective force on the robot)
    :return: Given a circle (P,R) and a line (wall_init, wall_end), returns the new position of the circle tangent to the line (if there is collision) and the point of rotation about which the circle should rotate to resolve the collision
    """

    # work in radians
    angle = np.radians(angle)
    radius_along_orientation = [np.cos(angle)*R,np.sin(angle)*R]
    position = [P[0]-radius_along_orientation[0],P[1]-radius_along_orientation[1]]

    # determine new position after current frame
    new_position = [P[0] + F * np.cos(angle), P[1] + F * np.sin(angle)]



    # DCD if speed under (empirically-determined) speed -> above this, tunneling is too pronounced so need to do CCD
    # wall vector
    wall_v = [wall_end[0] - wall_init[0],wall_end[1] - wall_init[1]]
    # wall unit vector
    unit_v = wall_v/np.linalg.norm(wall_v)
    # relative circle position to wall_init point
    circle_rel = [P[0] - wall_init[0], P[1] - wall_init[1]]
    # projection of circle's relative position to wall_init point onto the wall vector
    proj = np.array(circle_rel).dot(np.array(unit_v))
    if proj <= 0: # if closest point is wall_init, then set it to wall_init
        closest_p = wall_init
    elif proj >= np.linalg.norm(wall_v): # if closest point is wall_end, then set it to wall_end
        closest_p = wall_end
    else: # else calculate projection vector and determine actual closest point
        proj_v = (np.array(unit_v)) * proj
        closest_p = wall_init + proj_v

    # distance of circle to closest point
    dist_v = [P[0] - closest_p[0],P[1]-closest_p[1]]
    # displacement vector to closest point
    norm_dist_v = np.linalg.norm(dist_v)
    if norm_dist_v <= R: # if closer than the radius of the circle => collision => resolve it using the radius
        return True, P+(dist_v / norm_dist_v * (R - norm_dist_v))
    else: # no collision
        return False, new_position

def resolve_past_collision(walls, collisions, old_position, new_position, R, F, angle, tolerance=0.):
    """
    Resolve all collisions in a continuous collision detection manner in a narrow phase way. This assumes all broad phase continuous collisions were already calculated and passed as a variable of this function.
    :param walls: All walls that were collided with
    :param collisions: All points at which collisions were registered
    :param old_position: The old position of the robot
    :param new_position: The new position of the robot before the collision response kicks in
    :param R: The radius of the robot
    :param F: The force / speed of the robot
    :param angle: The angle at which the robot travels
    :param tolerance: (optional) tolerance parameter
    :return: new position after collisions are resolved
    """
    if len(collisions) == 0: # if no collisions, skip this expensive function
        return new_position
    # work in radians
    angle = np.radians(angle)
    distances = []
    # calculate the distance of the robot's edge in its direction of travel to the collision
    for collision in collisions:
        distances.append(utils.distance_between([old_position[0]+R*np.cos(angle), old_position[1]+R*np.sin(angle)],collision))
    indices = np.argsort(distances) # sort by distance to each of the collisions
    if len(indices) > 0:
        i = indices[0] # handle closest collision first; TODO: handle all collisions
        collision_handled = collisions[i]
        # the wall which was collided with - currently unused, but potentially useful (?)
        wall_collided_with = walls[i]
        distance = distances[i]
        travelled = np.linalg.norm([new_position[0]-old_position[0],new_position[1]-old_position[1]])
        percentile = distance/travelled # the distance to the collision relative to the total distance between the old position and new position with no collisions being handled

        # use the collision point as the closest point and handle it as a regular discrete collision is handled
        v1 = np.array(old_position)
        v2 = np.array(collision_handled)
        v3 = v2 - v1
        nv3 = np.linalg.norm(v3)

        # determine new position after collision
        new_position = v1+(v3/nv3 * (R - nv3))
        # claculate movement trying to add the paralel component to the velocity
        new_position += np.array([np.sin(angle),np.cos(angle)])*F*(1-percentile)

        # new_position = [old_position[0]+F*np.cos(angle)*percentile_barely_avoid_collision + F * np.cos(angle+np.pi) * (1-percentile_barely_avoid_collision),old_position[1]+F*np.sin(angle)*percentile_barely_avoid_collision + F * np.sin(angle+np.pi) * (1-percentile_barely_avoid_collision)]

        return new_position
    else:
        # basically skipped for now
        for i in indices:
            return new_position
    # basically will not happen if it reaches this point
    return new_position