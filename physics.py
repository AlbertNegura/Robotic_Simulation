"""
Physics script with Physics-based interactions (i.e. collisions).
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
    wall_angle = np.radians(angle + 90)
    angle = np.radians(angle)
    radius_along_orientation = [np.cos(angle)*R,np.sin(angle)*R]
    position = [P[0]-radius_along_orientation[0],P[1]-radius_along_orientation[1]]

    # determine new position after current frame
    new_position = [P[0] + F * np.cos(angle), P[1] + F * np.sin(angle)]


    # if line is inside of circle, stop circle

    # DCD if speed under (empirically-determined) speed -> above this, tunneling is too pronounced so need to do CCD
    if F*np.cos(angle) < (R + tolerance) and F*np.sin(angle) < (R + tolerance):
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

    # CCD
    # check and resolve frontal collision
    collision_point = utils.intersection([np.subtract(wall_init,radius_along_orientation), np.subtract(wall_end,radius_along_orientation)], [position,new_position])
    if collision_point is not None:
        print("here")
        movement_before_collision = [collision_point[0] - P[0] + R*np.cos(angle),collision_point[1] - P[1] + R*np.sin(angle)]
        norm_movement_before_collision = np.linalg.norm(movement_before_collision)
        norm_movement = np.linalg.norm([new_position[0]-P[0],new_position[1]-P[1]])
        percentile_movement = norm_movement_before_collision / norm_movement
        new_P = [P[0] + F*np.cos(angle)*percentile_movement + 0.1*np.cos(angle),P[1] + F*np.sin(angle)*percentile_movement + 0.1*np.sin(angle)]


        # wall vector
        wall_v = [wall_end[0] - wall_init[0],wall_end[1] - wall_init[1]]
        # wall unit vector
        unit_v = wall_v/np.linalg.norm(wall_v)
        # relative circle position to wall_init point
        circle_rel = [new_P[0] - wall_init[0], new_P[1] - wall_init[1]]
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
        dist_v = [new_P[0] - closest_p[0],new_P[1]-closest_p[1]]
        # displacement vector to closest point
        norm_dist_v = np.linalg.norm(dist_v)
        if norm_dist_v <= R: # if closer than the radius of the circle => collision => resolve it using the radius
            return True, new_P+(dist_v / norm_dist_v * (R - norm_dist_v))
        else: # no collision
            return False, new_position



        collision_point_without_orientation = [collision_point[0]-R*np.cos(angle)+F*np.cos(wall_angle),collision_point[1]-R*np.sin(angle)+F*np.sin(wall_angle)]

        # if collided with wall, resolve collision position
        # dx = collision_point_without_orientation[0] - P[0]
        # dy = collision_point_without_orientation[1] - P[1]
        #
        # ang1 = np.arctan2(dy,dx)
        # ang2 = ang1 + np.radians(90)
        # angle_of_rotation = ang2 - angle
        # point_of_rotation = [np.cos(angle_of_rotation) * new_position[0],np.cos(angle_of_rotation) * new_position[1]]

        return True, collision_point_without_orientation


    return False, new_position