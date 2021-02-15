"""
Physics script with Physics-based interactions (i.e. collisions).
"""
import numpy as np
import utils
from config import WIDTH

def resolve_wall_collision(wall_init, wall_end, P, Velocity, R):
    """
    :param wall_init: starting point of the wall (x,y)
    :param wall_end: end point of the wall (x,y)
    :param P: origin of the circle (x,y)
    :param Velocity: velocity components of the circle
    :param R: Radius of the circle
    :return: Given a circle (P,R) and a line (wall_init, wall_end), returns the new position of the circle tangent to the line (if there is collision) and the new velocity components (Vx, Vy) after collision
    """

    new_velocity = Velocity
    new_position = P
    intersection_point = utils.circle_line_tangent_point(wall_init,wall_end,P,R)
    if intersection_point != None:
        for tangent_point in intersection_point:
            v = [P[0] - tangent_point[0],P[1] - tangent_point[1]]
            v2 = np.sqrt(int(v[0])**2 + int(v[1])**2)
            u = R*(v/v2)
            new_position = tangent_point + u - Velocity

        x_axis = np.array([WIDTH, 0])
        new_wall_v = [wall_end[0]-wall_init[0],wall_end[1]-wall_init[1]]
        direction = utils.angle(x_axis, np.array(new_wall_v))

        v_direction = Velocity[0]*np.cos(direction) + Velocity[1]*np.cos(np.deg2rad(90)-direction)
        new_velocity = [v_direction*np.cos(direction), v_direction*np.sin(direction)]

    return intersection_point is not None, new_position, new_velocity

