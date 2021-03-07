import numpy as np
def fitness(total_area, num_c, sensor_values):
    """
    :param total_area: maximise total area covered (from the robot's self.position_history)
    :param num_c: minimise number of collisions
    :param sensor_values: Average value of the robot's sensors
    """
    a = 2 # to be determined manually
    b = -2
    c = 0

    return a*total_area + b*num_c + c*sensor_values
