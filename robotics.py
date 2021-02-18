import numpy as np
import motion
import physics
import utils
import config


class Robot:
    colour = None
    colour2 = None
    orientation = 0  # degrees
    facing_position = []  # must remember to set equal to radius - 1
    radius = 0
    position = []
    acceleration = 0.005
    sensors = []
    velocity_right = 0
    velocity_left = 0
    velocity = [0, 0]
    force = 0

    position_history = []
    orientation_history = []
    velocity_history = []

    def save_position(self, new_position):
        self.position_history.append([new_position])

    def save_orientation(self, new_orientation):
        self.orientation_history.append(new_orientation)


    def move(self, walls):
        update=False
        j = 0
        if self.velocity_right != self.velocity_left:
            new_x, new_y, theta = motion.Step(self.velocity_right, self.velocity_left, self.radius*2, self.position[0], self.position[1], np.radians(self.orientation))
            self.force = np.linalg.norm([self.velocity_left,self.velocity_right])
            for i in range(len(walls)):
                if not update:
                    j += 1
                    if j >= len(walls):
                        break
                else:
                    j = 0
                    update = False
                wall = walls[j]
                is_intersection, new_position = physics.resolve_wall_collision(wall[0], wall[1], self.position,
                                                                                             self.force, self.radius,
                                                                                             self.orientation)
                if is_intersection:
                    update = True
                    self.position = new_position#utils.rotate(new_position, point_of_rotation, np.radians(self.orientation))
            self.position = [self.position[0]+self.force*np.cos(np.radians(self.orientation)),self.position[1]+self.force*np.sin(np.radians(self.orientation))]
            utils.clip(self.position, [self.radius+1, self.radius+1], [config.WIDTH - int(config.HEIGHT / 3) - self.radius-1, config.HEIGHT - int(config.HEIGHT / 3) - self.radius-1], self)
            self.orientation = np.degrees(theta)
            for sensor in self.sensors:
                sensor.update_sensor(self.position, np.radians(self.orientation - self.orientation_history[-1]), None)
        else:
            self.force = np.linalg.norm([self.velocity_left,self.velocity_right])
            for i in range(len(walls)):
                if not update:
                    j += 1
                    if j >= len(walls):
                        break
                else:
                    j = 0
                    update = False
                wall = walls[j]
                is_intersection, new_position = physics.resolve_wall_collision(wall[0], wall[1], self.position,
                                                                                             self.force, self.radius,
                                                                                             self.orientation)
                if is_intersection:
                    update = True
                    self.position = new_position#utils.rotate(new_position, point_of_rotation, np.radians(self.orientation))
            self.position = [self.position[0]+self.force*np.cos(np.radians(self.orientation)),self.position[1]+self.force*np.sin(np.radians(self.orientation))]  # utils.rotate(self.position, self.position+[self.velocity_left/2+self.velocity_right/2],np.radians(self.orientation))

            utils.clip(self.position, [self.radius+1, self.radius+1], [config.WIDTH - int(config.HEIGHT / 3) - self.radius-1, config.HEIGHT - int(config.HEIGHT / 3) - self.radius-1], self)
            for sensor in self.sensors:
                sensor.update_sensor(self.position, 0, None)
        self.rotate()

        self.save_position(self.position)
        self.save_orientation(self.orientation)

    def adjust_sensors(self, Walls):
        for sensor in self.sensors:
            for wall in Walls:
                sensor_line = np.array([sensor.get_start(),sensor.get_end()])
                wall_line = np.array([wall[0],wall[1]])
                # print("lines", sensor_line, wall_line)
                intersec_point = utils.intersection(sensor_line,wall_line)
                if (intersec_point):
                    sensor.update_sensor(self.position, 0, intersec_point)

    def rotate(self):
        self.facing_position = utils.rotate_line(self.position, self.radius, np.radians(self.orientation))


def create_robot(init_pos=(100,200),radius = 50, acceleration = 0.005,num_sensors = 12):
    robot = Robot()
    robot.position = [int(np.random.randint(radius+1,init_pos[0]-radius-1)),int(np.random.randint(radius+1,init_pos[1]-radius-1))]
    robot.radius = radius
    robot.colour = (200,200,200) #light grey
    robot.colour2 = (0,0,0) #black
    robot.orientation = 0
    robot.acceleration = acceleration
    robot.facing_position = [robot.position[0]+robot.radius-1, robot.position[1]]
    prev_degree = robot.orientation #starting angle
    for s in range(num_sensors):
        sensor = Sensor(robot.position, prev_degree, num_sensors, robot)
        sensor.colour = (255, 211, 0) #Cyber Yellow
        prev_degree = sensor.get_prev_degree()
        robot.sensors.append(sensor)
    return robot


def reset_robot(robot):
    return robot


class Sensor:
    line_start = []
    line_end = []
    radians = 0
    colour = None
    max_radius = 100
    radius = 100
    intersection = []

    def __init__(self, position, prev_degree, num_of_sensors, robot):
        self.robot = robot
        self.num_of_sensors = num_of_sensors
        self.line_start = position
        self.radians = np.radians(prev_degree+(360/num_of_sensors))
        self.line_end = utils.rotate_line(position, self.max_radius, self.radians)

    def get_start(self):
        #temp = [self.line_start[0]+np.sin(self.radians)*self.robot.radius,self.line_start[1]+np.cos(self.radians)*self.robot.radius]
        return self.line_start

    def get_end(self):
        return self.line_end

    def get_prev_degree(self):
        return np.degrees(self.radians)

    def get_max_radius(self):
        return self.max_radius

    def update_sensor(self, new_position, angle, intersection):
        self.line_start = new_position
        self.radians = angle + self.radians
        self.instersection = intersection
        if (intersection == None):
            self.radius = self.max_radius
        else:
            self.radius = utils.distance_between(new_position, intersection)
        self.line_end = utils.rotate_line(new_position, self.radius, self.radians)
        self.line_start = utils.rotate_line(new_position, self.robot.radius, self.radians)

