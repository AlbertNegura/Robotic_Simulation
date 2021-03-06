"""Robotic Simulation Software Robotics Handler
Authors:
Julien Havel
Kamil Inglot
Albert Negura
Sergi Nogues Farres
"""
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
    max_vel = 0
    force = 0
    grid_covered = []
    collisions = 0

    position_history = []
    orientation_history = []


    def save_position(self, new_position):
        """
        Save position to the position_history
        :param new_position:
        :return:
        """
        self.position_history.append(new_position)

    def save_orientation(self, new_orientation):
        """
        Save the orientation to the orientation history
        :param new_orientation:
        :return:
        """
        self.orientation_history.append(new_orientation)


    def move(self, walls):
        """
        Move the robot while keeping track of all walls. Can update the walls so it only keeps track of the walls present in a neighbouring grid based on the distance the robot travels in one frame.
        :param walls:
        :return:
        """
        update=False
        collision = False
        j = 0
        new_position = self.position

        if self.velocity_right > self.max_vel:
            self.velocity_right = round(self.max_vel,1)
        if self.velocity_right < -self.max_vel:
            self.velocity_right = -round(self.max_vel,1)
        if self.velocity_left > self.max_vel:
            self.velocity_left = round(self.max_vel,1)
        if self.velocity_left < -self.max_vel:
            self.velocity_left = -round(self.max_vel,1)

        # calculate force
        self.force = np.linalg.norm([self.velocity_left, self.velocity_right]) * np.sign(
            self.velocity_left + self.velocity_right)
        if self.force == np.nan:
            self.force = 0.

        # if wheels are not moving the equal velocity, resolve their movement differently
        if self.velocity_right != self.velocity_left:
            # motion model step
            new_x, new_y, theta = motion.Step(self.velocity_right, self.velocity_left, self.radius*2, self.position[0], self.position[1], np.radians(self.orientation))
            # discrete collision detection and resolution, trying to loop over all walls as many times as necessary until all collision resolved
            # note that this does not handle collisions with boundary walls - boundary wall collisions take precedence and "break" the simulation
            # a trivial solution would be to place secondary boundary walls on top (but slightly closer to the inside) of the existing boundary walls and treat them as normal walls
            # I do not know why I did not do that, but if it becomes necessary, I will add it
            for i in range(len(walls)):
                if not update:
                    j += 1
                    if j >= len(walls):
                        break
                else:
                    j = 0
                    update = False
                wall = walls[j]
                is_intersection, new_P = physics.resolve_wall_collision(wall[0], wall[1], new_position,
                                                                                             self.force, self.radius,
                                                                                             self.orientation)
                if is_intersection:
                    new_position = new_P
                    collision = True
                    #update = True
            # determine new position after accounting for parallel velocity component
            self.collisions += 1 if collision else 0
            new_position = [new_position[0]+self.force*np.cos(np.radians(self.orientation)),new_position[1]+self.force*np.sin(np.radians(self.orientation))]  # utils.rotate(self.position, self.position+[self.velocity_left/2+self.velocity_right/2],np.radians(self.orientation))
            # if it moves too quickly, try to resolve continuous collisions
            # resolve collisions using continuous collision detection - if no collisions, just returns the new_position itself
            new_position = physics.resolve_past_collision(walls, [],self.position, new_position, self.radius, self.force, self.orientation)
            # set the robot position to the new position
            self.position = new_position#utils.rotate(new_position, point_of_rotation, np.radians(self.orientation))
            # clip the robot's position to within the boundaries - can do it earlier
            utils.clip(self.position, [self.radius+1, self.radius+1], [config.WIDTH - int(config.HEIGHT / 3) - self.radius-1, config.HEIGHT - int(config.HEIGHT / 3) - self.radius-1], self)
            # set the orientation to the new orientation determined by the motion model
            self.orientation = np.degrees(theta)
            # update the sensors when done
            for sensor in self.sensors:
                sensor.update_sensor(self.position, np.radians(self.orientation - self.orientation_history[-1]), None)
        else:
            # discrete collision detection and resolution, trying to loop over all walls as many times as necessary until all collision resolved
            # note that this does not handle collisions with boundary walls - boundary wall collisions take precedence and "break" the simulation
            # a trivial solution would be to place secondary boundary walls on top (but slightly closer to the inside) of the existing boundary walls and treat them as normal walls
            # I do not know why I did not do that, but if it becomes necessary, I will add it
            for i in range(len(walls)):
                if not update:
                    j += 1
                    if j >= len(walls):
                        break
                else:
                    j = 0
                    update = False
                wall = walls[j]
                is_intersection, new_P = physics.resolve_wall_collision(wall[0], wall[1], new_position,
                                                                                             self.force, self.radius,
                                                                                             self.orientation)
                if is_intersection:
                    new_position = new_P
                    collision = True
                    #update = True
            collisions = []
            # determine new position after accounting for parallel velocity component
            self.collisions += 1 if collision else 0
            new_position = [new_position[0]+self.force*np.cos(np.radians(self.orientation)),new_position[1]+self.force*np.sin(np.radians(self.orientation))]  # utils.rotate(self.position, self.position+[self.velocity_left/2+self.velocity_right/2],np.radians(self.orientation))
            # if it moves too quickly, try to resolve continuous collisions
            # resolve collisions using continuous collision detection - if no collisions, just returns the new_position itself
            new_position = physics.resolve_past_collision(walls, [],self.position, new_position, self.radius, self.force, self.orientation)
            # set the robot position to the new position
            self.position = new_position#utils.rotate(new_position, point_of_rotation, np.radians(self.orientation))
            # clip the robot's position to within the boundaries - can do it earlier
            utils.clip(self.position, [self.radius+1, self.radius+1], [config.WIDTH - int(config.HEIGHT / 3) - self.radius-1, config.HEIGHT - int(config.HEIGHT / 3) - self.radius-1], self)
            # update the sensors when done
            for sensor in self.sensors:
                sensor.update_sensor(self.position, 0, None)
        # update the robot's orientation accordingly
        self.rotate()
        # save position and orientation to their respective history lists
        self.save_position(self.position)
        self.save_orientation(self.orientation)

    def adjust_sensors(self, Walls):
        """
        Adjust the sensors attached to the robot by calculating their intersections with accompanying walls.
        :param Walls: The walls to calculate the intersections with
        :return:
        """
        for sensor in self.sensors:
            for wall in Walls:
                sensor_line = np.array([self.position,sensor.line_end])
                wall_line = np.array([wall[0],wall[1]])
                # print("lines", sensor_line, wall_line)
                intersec_point = utils.intersection(sensor_line,wall_line)
                if (intersec_point):
                    sensor.update_sensor(self.position, 0, intersec_point)

    def rotate(self):
        """
        Change the robot's facing position based on its orientation.
        :return:
        """
        self.facing_position = utils.rotate_line(self.position, self.radius, np.radians(self.orientation))

    def sensor_values(self):
        """
        :return: numpy array of shape (1,num_sensors) with current sensor values
        Used for RNN purposes
        """
        values = []
        for s in self.sensors:
            values.append(s.radius)
        return np.array([values])

    def vr_vl(self):
        """
        :return: numpy array of shape (1,2) with current Vl and Vr
        Used for RNN purposes
        """
        return np.array([[self.velocity_left, self.velocity_right]])


def create_robot(init_pos=(100,200),radius = 50, acceleration = 0.005,num_sensors = 12, max_radius = 50):
    """
    Create the robot with the specified parameters.
    :param init_pos: Upper bounds to the initial possition the robot can spawn at.
    :param radius: The radius of the robot
    :param acceleration: The acceleration of the robot
    :param num_sensors: The number of sensors to be created.
    :return:
    """
    robot = Robot()
    robot.position = [int(np.random.randint(radius+1,init_pos[0]-radius-1)),int(np.random.randint(radius+1,init_pos[1]-radius-1))]
    robot.radius = radius
    robot.colour = (200,200,200) #light grey
    robot.colour2 = (0,0,0) #black
    robot.orientation = 0
    robot.acceleration = acceleration
    robot.facing_position = [robot.position[0]+robot.radius-1, robot.position[1]]
    robot.sensors = []
    robot.position_history = [robot.position]
    robot.orientation_history = [robot.orientation]
    robot.max_vel = radius / 1.5
    prev_degree = robot.orientation #starting angle
    for s in range(num_sensors):
        sensor = Sensor(robot.position, prev_degree, num_sensors, robot, max_radius)
        sensor.colour = (255, 211, 0) #Cyber Yellow
        prev_degree = np.degrees(sensor.radians)
        robot.sensors.append(sensor)
    return robot


class Sensor:
    line_start = []
    line_end = []
    radians = 0
    colour = None
    max_radius = 120
    radius = 100
    intersection = []

    def __init__(self, position, prev_degree, num_of_sensors, robot, max_radius):
        """
        :param position: position from which the sensor should start sensing
        :param prev_degree: the robot orientation to calculate sensor positions from
        :param num_of_sensors: the number of sensors created
        :param robot: the robot itself
        :param max_radius: the maximum length of a sensor
        """
        self.max_radius = max_radius + robot.radius
        self.robot = robot
        self.num_of_sensors = num_of_sensors
        self.line_start = position
        self.radians = np.radians(prev_degree+(360/num_of_sensors))
        self.line_end = utils.rotate_line(position, self.max_radius, self.radians)

    def update_sensor(self, new_position, angle, intersection):
        """
        Update the sensor position based on the new orientation.
        :param new_position: The new position from which to draw the sensor
        :param angle: The angle of the robot
        :param intersection: The new position until which to draw the sensor
        :return:
        """
        self.line_start = new_position
        self.radians = angle + self.radians
        self.instersection = intersection
        if (intersection == None):
            self.radius = self.max_radius
        else:
            self.radius = utils.distance_between(new_position, intersection)
        self.line_end = utils.rotate_line(new_position, self.radius, self.radians)
        self.line_start = utils.rotate_line(new_position, self.robot.radius, self.radians)

