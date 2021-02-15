"""
Physics script with Physics-based interactions (i.e. collisions).
"""
import numpy as np
import utils

#region Test
"""
x = Point(0, 0)
y = Point(1, 1)
c = Circle(x, 5)

l1 = Line(Point(5, -5), Point(5, 5))
print(c.is_tangent(l1))  # is l tangent to c? True

l2 = Line(x, y)
c.is_tangent(l2)  # is l tangent to c? False

l3=Line(x, Point(0,1))
l4 = l3.perpendicular_line(x)

p = intersection(c, l1)
print(p)

"""
wall_init=[0, 600]
wall_end=[1600, 600]
P=[1124, 580.411]
Theta=90
Velocity=10
R=20
#endregion

def resolve_wall_collision(wall_init, wall_end, P, Theta, Velocity, R):
    """
    :param wall_init: starting point of the wall (x,y)
    :param wall_end: end point of the wall (x,y)
    :param P: origin of the circle (x,y)
    :param Theta: angle between the x-axis and the velocity vector of the circle in degrees
    :param Velocity: velocity of the circle as scalar
    :param R: Radius of the circle
    :return: Given a circle (P,R) and a line (wall_init, wall_end), returns the new position of the circle tangent to the line (if there is collision) and the new velocity components (Vx, Vy) after collision
    """

    new_position = []
    new_position = P
    intersection_point = utils.circle_line_tangent_point(wall_init,wall_end,P,R)
    intersec = False
    if intersection_point != None:
        intersec = True
        for tangent_point in intersection_point:
            v = [P[0] - tangent_point[0],P[1] - tangent_point[1]]
            v2 = np.sqrt(int(v[0])**2 + int(v[1])**2)
            u = R*(v/v2)
            new_position = tangent_point + u

    """# new velocity
    V_x = Velocity * np.cos(-np.deg2rad(Theta))
    V_y = Velocity * np.sin(-np.deg2rad(Theta))
    V = Point(V_x + P[0], V_y + P[1])
    V_vector = Line(robot_origin, V)  # velocity vector"""

    return intersec, new_position




resolve_wall_collision(wall_init, wall_end, P, Theta, Velocity, R)
