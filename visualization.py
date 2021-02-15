from grid import *
import pygame.gfxdraw


def draw_robot(pygame, screen, robot):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    pygame.draw.circle(screen, robot.colour, robot.position, robot.radius)
    pygame.draw.circle(screen, robot.colour2, robot.position, robot.radius + 0.5, 1)
    pygame.draw.line(screen, robot.colour2, robot.position, robot.facing_position, 2)


def draw_sensors(pygame, screen, robot):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    for sensor in robot.sensors:
        pygame.draw.line(screen, sensor.colour, sensor.get_start(), sensor.get_end(), 5)


def draw_sensor_info(screen, robot, font):
    for sensor in robot.sensors:
        sensor_info = font.render(str(int(sensor.radius)), True, (255, 0, 0))
        sensor_info_position = sensor.line_start - (sensor.line_start - sensor.line_end) * 0.10
        sensor_info_position[0] -= 5
        sensor_info_position[1] -= 5
        screen.blit(sensor_info, sensor_info_position)


def draw_wall(pygame, screen, origin, end, width=10, color=(0, 0, 0)):
    pygame.draw.line(screen, color, origin, end, width)


def draw_grid(pygame, screen, grid):
    for squares in grid:
        for square in squares:
            pygame.gfxdraw.rectangle(screen,
                                     pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                                     (0, 200, 200, 50))

def write_text(pygame, screen, text, position = (1300, 300)):
    font = pygame.font.SysFont(None, 24)
    img = font.render(text, True, (0,0,0))
    screen.blit(img, position)
