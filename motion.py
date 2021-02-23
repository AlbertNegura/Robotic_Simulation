"""
Robotic Simulation Software motion model calculations
Authors:
Sergi Nogues Farres
"""
import numpy as np

def Step(Vr,Vl,l,x0,y0,theta):
    """
    Execute a motion step according to the kinematics equations discussed.
    :param Vr: right wheel velocity
    :param Vl: left wheel velocity
    :param l: distance between the wheels
    :param x0: the x position of the robot
    :param y0: the y position of the robot
    :param theta: the angle the robot is facing in radians
    :return: the new x,y positions and theta orientation in radians
    """
    # [theta] = radians
    R,w = rotation(Vr,Vl,l)
    Icc_x,Icc_y = ICC(x0,y0,theta,R)

    x = np.cos(w)*(x0-Icc_x) - np.sin(w)*(y0-Icc_y) + Icc_x
    y = np.sin(w)*(x0-Icc_x) + np.cos(w)*(y0-Icc_y) + Icc_y
    Theta = theta + w

    return x,y,Theta

def ICC(x0,y0,theta,R):
    """
    Calculate ICC distance for the wheels
    :param x0: the x coordinate of the robot's center
    :param y0: the y coordinate of the robot's center
    :param theta: the angle of the robot
    :param R: the distance travelled
    :return: the new x,y coordinates of the robot.
    """
    x = x0 - R*np.sin(theta)
    y = y0 + R*np.cos(theta)
    return x,y 

def rotation(Vr,Vl,l):
    """
    Calculate corresponding rotation after applying equations of motion.
    :param Vr: velocity of the right wheel
    :param Vl: velocity of the left wheel
    :param l: diameter of the robot
    :return: the distance travelled by the robot at the corresponding angle as a R,w pair
    """
    R = l/2*((Vr+Vl)/(Vr-Vl))
    w = 2*np.pi*(Vr-Vl)/l
    return R,w

