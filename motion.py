import numpy as np

def Step(Vr,Vl,l,x0,y0,theta):
    # [theta] = radians
    R,w = rotation(Vr,Vl,l)
    Icc_x,Icc_y = ICC(x0,y0,theta,R)

    x = np.cos(w)*(x0-Icc_x) - np.sin(w)*(y0-Icc_y) + Icc_x
    y = np.sin(w)*(x0-Icc_x) + np.cos(w)*(y0-Icc_y) + Icc_y
    Theta = theta + w

    return x,y,Theta

def ICC(x0,y0,theta,R):
    x = x0 - R*np.sin(theta)
    y = y0 + R*np.cos(theta)
    return x,y 

def rotation(Vr,Vl,l):
    R = l/2*((Vr+Vl)/(Vr-Vl))
    w = 2*np.pi*(Vr-Vl)/l
    return R,w

