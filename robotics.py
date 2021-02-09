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


def create_robot():
    robot = Robot()
    return robot

def reset_robot(robot):
    return robot