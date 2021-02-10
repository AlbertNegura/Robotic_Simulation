import numpy as np
import motion
import utils

class Robot:
    colour = None
    colour2 = None
    orientation = 0
    facing_position = [] # must remember to set equal to radius - 1
    radius = 0
    position = []
    velocity = []
    acceleration = 0.0005
    sensors = []
    velocity_right = 0
    velocity_left = 0

    position_history = []
    orientation_history = []
    velocity_history = []

    def save_position(self, new_position):
        self.position_history.append([new_position])

    def save_orientation(self, new_orientation):
        self.orientation_history.append(new_orientation)

    def save_velocity(self, new_velocity):
        self.velocity_history.append(new_velocity)

    def move(self):
        if self.velocity_right != self.velocity_left:
            new_x, new_y, theta = motion.step(self.velocity_right, self.velocity_left, self.radius, self.position[0], self.position[1], self.orientation)
            self.position = [new_x, new_y]
            self.orientation = theta
        else:
            self.position = utils.rotate(self.position, self.position+[self.velocity_left/2+self.velocity_right/2],np.radians(self.orientation))




def create_robot(init_pos=(1600,900),radius = 50):
    robot = Robot()
    robot.position = [np.random.uniform(0+radius,init_pos[0]-radius),np.random.uniform(0+radius,init_pos[1]-radius)]
    robot.radius = radius
    robot.colour = (200,200,200) #light grey
    robot.colour2 = (0,0,0) #black
    robot.orientation = 0
    robot.facing_position = [robot.position[0]+robot.radius-1, robot.position[1]]
    return robot

def reset_robot(robot):
    return robot