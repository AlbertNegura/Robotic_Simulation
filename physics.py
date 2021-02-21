"""
Physics script with Physics-based interactions (i.e. collisions).
"""
import numpy as np
import utils

def point_in_circle(x,y,px,py,r):
    return (x - px)**2 + (y-py)**2 <= r

def circle_on_edge(w1, w2, p, r):
    a1 = point_in_circle(w1[0],w1[1],p[0],p[1],r)
    a2 = point_in_circle(w2[0],w2[1],p[0],p[1],r)
    return a1 or a2, w1 if a1 else w2

def closest_point(w1,w2,px,py):
    p = np.array(px,py)

    d1 = np.linalg.norm(p-w1)
    d2 = np.linalg.norm(p-w2)
    line = np.linalg.norm(np.array(w1)-np.array(w2))
    tol = 0.

    return (d1+d2 >= line-tol and d1+d2 <= line+tol)

def circle_segment_collision(w1,w2,p,r):
    a1, a2 = circle_on_edge(w1,w2,p,r)
    if a1:
        return a1, a2

    distX = w1[0] - w2[0]
    distY = w1[1] - w2[1]
    line = np.linalg.norm([distX,distY])
    prod = (((p[0]-w1[0])*(w2[0]-w1[0])) + ((p[1]-w1[1])*(w2[1]-w1[1]))) / line**2
    px = w1[0] + (prod*(w2[0]-w1[0]))
    py = w1[1] + (prod*(w2[1]-w1[1]))

    if not closest_point(w1,w2,px,py):
        return False, [0,0]
    dX = px - p[0]
    dY = py - p[1]
    d = np.linalg.norm([dX,dY])
    return d <= r, [px,py]

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

    # DCD
    if F*np.cos(angle) < (R + tolerance)/7 and F*np.sin(angle) < (R + tolerance)/7:

        wall_v = [wall_end[0] - wall_init[0],wall_end[1] - wall_init[1]]
        unit_v = wall_v/np.linalg.norm(wall_v)
        circle_rel = [P[0] - wall_init[0], P[1] - wall_init[1]]
        proj = np.array(circle_rel).dot(np.array(unit_v))
        if proj <= 0:
            closest_p = wall_init
        elif proj >= np.linalg.norm(wall_v):
            closest_p = wall_end
        else:
            proj_v = (np.array(unit_v)) * proj
            closest_p = wall_init + proj_v

        dist_v = [P[0] - closest_p[0],P[1]-closest_p[1]]
        norm_dist_v = np.linalg.norm(dist_v)
        if norm_dist_v <= R:
            return True, P+(dist_v / norm_dist_v * (R - norm_dist_v))

        else:
            return False, new_position

        # a1, a2 = circle_segment_collision(wall_init,wall_end,P,R)
        # return a1, [a2[0]-R*np.cos(angle),a2[1]-R*np.sin(angle)]

        # coll_check = [P[0] + 1.98 * F * np.cos(angle), P[1] + 1.98 * F * np.sin(angle)]
        # discrete_new_position = new_position
        # collision_point = utils.intersection(
        #     [np.subtract(wall_init, radius_along_orientation), np.subtract(wall_end, radius_along_orientation)],
        #     [position, coll_check])
        #
        # if collision_point is not None:
        #     collision_point = utils.circle_line_tangent_point(wall_init,wall_end,P,R)
        #     if collision_point is not None:
        #         collision_point = collision_point[0]
        #         v = [P[0] - collision_point[0],P[1] - collision_point[1]]
        #         v2 = np.sqrt((v[0])**2 + (v[1])**2)
        #         u = R*(v/v2)
        #
        #         discrete_new_position = np.add(collision_point,u) - np.array([F*np.cos(angle), F*np.sin(angle)])
        #         print(discrete_new_position)
        #     return True, discrete_new_position
        # return False, discrete_new_position


    # CCD
    # check and resolve frontal collision
    collision_point = utils.intersection([np.subtract(wall_init,radius_along_orientation), np.subtract(wall_end,radius_along_orientation)], [position,new_position])
    if collision_point is not None:

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
    #
    #
    # unit_vector_along_velocity = [Velocity[0]*np.cos(np.radians(angle)),Velocity[1]*np.sin(np.radians(angle))]
    # unit_vector_along_velocity = unit_vector_along_velocity/np.linalg.norm(unit_vector_along_velocity) if np.linalg.norm(unit_vector_along_velocity) != 0 else unit_vector_along_velocity
    # new_velocity = Velocity
    # new_position = [P[0]+unit_vector_along_velocity[0]*np.linalg.norm(Velocity),P[1]+unit_vector_along_velocity[1]*np.linalg.norm(Velocity)]
    # ccd_intersection_point =
    # # currently resolving collisions based on the center of the circle colliding with a wall that is R closer to the circle in the opposite direction of movement - need to instead of the whole circle
    # tolerance = np.linalg.norm(Velocity)*2 if tolerance == 0 and np.linalg.norm(Velocity) >= 1. else Velocity[0] + Velocity[1]
    # if ccd_intersection_point is not None:
    #     norm_opposite_direction = -1*np.array(Velocity)/ np.linalg.norm(Velocity)
    #     opposite_radius_component = (R+tolerance) * norm_opposite_direction
    #     ccd_component = ccd_intersection_point + opposite_radius_component
    #
    #     tx = (ccd_component[0] - P[0]) / (new_position[0]-P[0])
    #     ty = (ccd_component[1] - P[1]) / (new_position[1]-P[1])
    #     tx = 0 if tx == np.inf or tx == -np.inf or np.isnan(tx) else tx
    #     ty = 0 if ty == np.inf or ty == -np.inf or np.isnan(ty) else ty
    #
    #     new_velocity = [Velocity[0] * tx, Velocity[1] * ty]
    #     new_position = P + new_velocity
    #
    #     return True, new_position, new_velocity
    #
    # new_position = P
    # intersection_point = utils.circle_line_tangent_point(wall_init,wall_end,P,R)
    # if intersection_point != None:
    #     for tangent_point in intersection_point:
    #         v = [P[0] - tangent_point[0],P[1] - tangent_point[1]]
    #         v2 = np.sqrt(int(v[0])**2 + int(v[1])**2)
    #         u = R*(v/v2)
    #
    #         new_position = tangent_point + u - new_velocity
    #
    #     x_axis = np.array([WIDTH, 0])
    #     new_wall_v = [wall_end[0]-wall_init[0],wall_end[1]-wall_init[1]]
    #     direction = utils.angle(x_axis, np.array(new_wall_v))
    #
    #     v_direction = Velocity[0]*np.cos(direction) + Velocity[1]*np.sin(np.deg2rad(90)-direction)
    #     new_velocity = [v_direction*np.cos(direction), v_direction*np.sin(direction)]
    #
    # return intersection_point is not None, new_position, new_velocity
