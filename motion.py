import numpy as np
import utils

def Step(Vr,Vl,l,x0,y0,theta):
    # we asume delta*t = 1 ?
    w = 2*np.pi*omega(Vr,Vl,l)
    Icc_x,Icc_y = ICC(x0,y0,theta,Vl,Vr,l)

    x = np.cos(w)*(x0 - Icc_x) - np.sin(w)*(y0-Icc_y) + Icc_x
    y = np.sin(w)*(x0 - Icc_x) + np.cos(w)*(y0-Icc_y) + Icc_y
    Theta = theta + omega(Vr,Vl,l)

    return x,y,Theta

def ICC(x0,y0,theta,Vl,Vr,l):
    #theta in degrees
    x = x0 - R(Vl,Vr,l)*np.sin(np.deg2rad(theta))
    y = y0 + R(Vl,Vr,l)*np.cos(np.deg2rad(theta))
    return x,y 

def R(Vr,Vl,l):
    return (l/2)*((Vr+Vl)/(Vr-Vl))

def omega(Vr,Vl,l):
    # s^-1
    return (Vr-Vl)/l

def rotate_robot(robot):
    robot.facing_position = utils.rotate_line(robot.position, robot.radius, robot.orientation)

print(Step(30,3,0.2,1,2,90))