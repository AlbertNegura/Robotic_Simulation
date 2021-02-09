import numpy as np

def Step(Vr,Vl,l,x0,y0,theta):
    # we asume delta*t = 1 ?
    w = omega(Vr,Vl,l)
    Icc_x,Icc_y = ICC(x0,y0,theta,Vl,Vr,l)

    x = np.cos(w)*(x0 - Icc_x) - np.sin(w)*(y0-Icc_y) + Icc_x
    y = np.sin(w)*(x0 - Icc_x) + np.cos(w)*(y0-Icc_y) + Icc_y
    Theta = theta + w

    return x,y,Theta

def ICC(x0,y0,theta,Vl,Vr,l):
    x = x0 - R(Vl,Vr,l)*np.sin(theta)
    y = y0 + R(Vl,Vr,l)*np.cos(theta)
    return x,y 

def R(Vr,Vl,l):
    return (l/2)*((Vr+Vl)/(Vr-Vl))

def omega(Vr,Vl,l):
    return (Vr-Vl)/l