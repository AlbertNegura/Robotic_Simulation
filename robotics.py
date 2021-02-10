import numpy as np

class Robot:
    colour = None
    colour2 = None
    orientation = 0
    radius = 0
    position = []
    velocity = []
    acceleration = 0
    sensors = []

    position_history = []
    orientation_history = []
    velocity_history = []

    def save_position(self, new_position):
        self.position_history.append([new_position])

    def save_orientation(self, new_orientation):
        self.orientation_history.append(new_orientation)

    def save_velocity(self, new_velocity):
        self.velocity_history.append(new_velocity)


def create_robot(init_pos=(1600,900),radius = 50):
    robot = Robot()
    robot.position = [np.random.uniform(0+radius,init_pos[0]-radius),np.random.uniform(0+radius,init_pos[1]-radius)]
    robot.radius = radius
    robot.colour = (200,200,200) #light grey
    robot.colour2 = (0,0,0) #black
    return robot

def reset_robot(robot):
    return robot