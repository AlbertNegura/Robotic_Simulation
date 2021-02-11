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
    acceleration = 0.005
    sensors = []
    velocity_right = 0
    velocity_left = 0
    velocity = [0,0]

    position_history = []
    orientation_history = []
    velocity_history = []

    def save_position(self, new_position):
        self.position_history.append([new_position])

    def save_orientation(self, new_orientation):
        self.orientation_history.append(new_orientation)


    def move(self):
        if self.velocity_right != self.velocity_left:
            new_x, new_y, theta = motion.Step(self.velocity_right, self.velocity_left, self.radius, self.position[0], self.position[1], np.radians(self.orientation))
            self.velocity = np.subtract([new_x, new_y], self.position)
            self.position = np.add(self.position, self.velocity)
            self.orientation = np.degrees(theta)
        else:
            self.position = np.add(self.position, self.velocity)#utils.rotate(self.position, self.position+[self.velocity_left/2+self.velocity_right/2],np.radians(self.orientation))
        self.rotate()
        for sensor in self.sensors:
            sensor.update_sensor(self.position, np.radians(self.orientation))
        self.save_position(self.position)
        self.save_orientation(self.orientation)


    def rotate(self):
        self.facing_position = utils.rotate_line(self.position, self.radius, np.radians(self.orientation))




def create_robot(init_pos=(100,200),radius = 50, acceleration = 0.005):
    robot = Robot()
    robot.position = [int(np.random.uniform(radius+1,init_pos[0]-radius-1)),int(np.random.uniform(radius+1,init_pos[1]-radius-1))]
    robot.radius = radius
    robot.colour = (200,200,200) #light grey
    robot.colour2 = (0,0,0) #black
    robot.orientation = 0
    robot.acceleration = acceleration
    robot.facing_position = [robot.position[0]+robot.radius-1, robot.position[1]]
    num_sensors = 12
    prev_degree = robot.orientation #starting angle
    for s in range(num_sensors):
        sensor = Sensor(robot.position, prev_degree, num_sensors)
        sensor.colour = (255, 211, 0) #Cyber Yellow
        prev_degree = sensor.get_prev_degree()
        robot.sensors.append(sensor)
    return robot


def reset_robot(robot):
    return robot


class Sensor():
    line_start = []
    line_end = []
    radians = 0
    colour = None
    max_radius = 100

    def __init__(self, position, prev_degree, num_of_sensors):
        self.num_of_sensors = num_of_sensors
        self.line_start = position
        self.radians = np.radians(prev_degree+(360/num_of_sensors))
        self.line_end = utils.rotate_line(position, self.max_radius, self.radians)

    def get_start(self):
        return self.line_start

    def get_end(self):
        return self.line_end

    def get_prev_degree(self):
        return np.degrees(self.radians)

    def update_sensor(self, new_position, angle):
        self.line_start = new_position
        self.radians = self.radians + angle
        self.line_end = utils.rotate_line(new_position, self.max_radius, self.radians)

