"""
Physics script with Physics-based interactions (i.e. collisions).
"""
import numpy as np
import utils
from config import WIDTH

def resolve_wall_collision(wall_init, wall_end, P, Velocity, R, angle, tolerance = 0):
    """
    :param wall_init: starting point of the wall (x,y)
    :param wall_end: end point of the wall (x,y)
    :param P: origin of the circle (x,y)
    :param Velocity: velocity components of the circle
    :param R: Radius of the circle
    :return: Given a circle (P,R) and a line (wall_init, wall_end), returns the new position of the circle tangent to the line (if there is collision) and the new velocity components (Vx, Vy) after collision
    """

    angle = np.radians(angle)
    unit_vector_along_velocity = [Velocity[0]*np.cos(np.radians(angle)),Velocity[1]*np.sin(np.radians(angle))]
    unit_vector_along_velocity = unit_vector_along_velocity/np.linalg.norm(unit_vector_along_velocity) if np.linalg.norm(unit_vector_along_velocity) != 0 else unit_vector_along_velocity
    new_velocity = Velocity
    new_position = [P[0]+unit_vector_along_velocity[0]*np.linalg.norm(Velocity),P[1]+unit_vector_along_velocity[1]*np.linalg.norm(Velocity)]
    ccd_intersection_point = utils.intersection([wall_init,wall_end],[P, new_position])
    # currently resolving collisions based on the center of the circle colliding with a wall that is R closer to the circle in the opposite direction of movement - need to instead of the whole circle
    tolerance = np.linalg.norm(Velocity)*2 if tolerance == 0 and np.linalg.norm(Velocity) >= 1. else Velocity[0] + Velocity[1]
    if ccd_intersection_point is not None:
        norm_opposite_direction = -1*np.array(Velocity)/ np.linalg.norm(Velocity)
        opposite_radius_component = (R+tolerance) * norm_opposite_direction
        ccd_component = ccd_intersection_point + opposite_radius_component

        tx = (ccd_component[0] - P[0]) / (new_position[0]-P[0])
        ty = (ccd_component[1] - P[1]) / (new_position[1]-P[1])
        tx = 0 if tx == np.inf or tx == -np.inf or np.isnan(tx) else tx
        ty = 0 if ty == np.inf or ty == -np.inf or np.isnan(ty) else ty

        new_velocity = [Velocity[0] * tx, Velocity[1] * ty]
        new_position = P + new_velocity

        return True, new_position, new_velocity

    intersection_point = utils.circle_line_tangent_point(wall_init,wall_end,P,R)
    if intersection_point != None:
        for tangent_point in intersection_point:
            v = [P[0] - tangent_point[0],P[1] - tangent_point[1]]
            v2 = np.sqrt(int(v[0])**2 + int(v[1])**2)
            u = R*(v/v2)

            new_position = tangent_point + u - new_velocity

        x_axis = np.array([WIDTH, 0])
        new_wall_v = [wall_end[0]-wall_init[0],wall_end[1]-wall_init[1]]
        direction = utils.angle(x_axis, np.array(new_wall_v))

        v_direction = Velocity[0]*np.cos(direction) + Velocity[1]*np.sin(np.deg2rad(90)-direction)
        new_velocity = [v_direction*np.cos(direction), v_direction*np.sin(direction)]

    return intersection_point is not None, new_position, new_velocity



