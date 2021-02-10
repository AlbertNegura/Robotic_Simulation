import numpy as np
import utils


def draw_robot(pygame, screen, robot):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    pygame.draw.circle(screen, robot.colour, robot.position, robot.radius)
    pygame.draw.circle(screen, robot.colour2, robot.position, robot.radius+0.5, 1)
    pygame.draw.line(screen, robot.colour2, robot.position, robot.facing_position, 2)

def draw_sensors(pygame, screen, robot):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    for sensor in robot.sensors:
        pygame.draw.line(screen, sensor.colour, sensor.line.start, sensor.line.end, 5)


def draw_wall(pygame, screen, origin, end, color=(0,0,0)):
    pygame.draw.line(screen, color, origin, end, 3)
