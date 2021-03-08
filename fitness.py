import numpy as np
def fitness(total_area, num_c, sensor_values):
    """
    :param total_area: maximise total area covered (from the robot's self.position_history)
    :param num_c: minimise number of collisions
    :param sensor_values: Average value of the robot's sensors
    """
    a = 2000 # to be determined manually
    b = -100
    c = -1
    f = a*total_area + b*num_c + c*sensor_values
    if(f<0): f=0
    return f/1000
