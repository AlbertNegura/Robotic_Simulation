"""Fitness function used for controller evolution
Authors:
Julien Havel
Kamil Inglot
Albert Negura
Sergi Nogues Farres
"""
import numpy as np
from config import *
def fitness(total_area, num_c, sensor_values):
    """
    :param total_area: maximise total area covered (from the robot's self.position_history)
    :param num_c: minimise number of collisions
    :param sensor_values: Average value of the robot's sensors
    """
    a = DIRT_VALUE # to be determined manually
    b = COLLISION_VALUE
    c = SENSOR_VALUE
    sensor_values = np.round(sensor_values, 5)
    if sensor_values == 0:
        f = a*total_area + b*num_c - 1000
    elif SENSOR_EXPONENTIAL:
        f = a*total_area + b*num_c + c*np.exp(1/(sensor_values-(RADIUS+2)*SENSORS))
    else:
        f = a*total_area + b*num_c + c*sensor_values
    if(f<0): f=0
    return f/1000
