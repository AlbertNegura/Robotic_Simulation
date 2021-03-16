"""
Robotic Simulation Software Varioud drawing and visualization functions. In-depth comments not included as they are simply generic pygame drawing functions that are very self-explanatory in this context.
Authors:
Julien Havel
Kamil Inglot
Albert Negura
Sergi Nogues Farres
"""
from grid import *
from pygame import gfxdraw
import math

def draw_robot(pygame, screen, robot):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    pygame.draw.circle(screen, robot.colour, robot.position, robot.radius - 0.6)
    pygame.draw.circle(screen, robot.colour2, robot.position, robot.radius - 0.1, 1)
    pygame.draw.line(screen, robot.colour2, robot.position, robot.facing_position, 2)

def draw_ghost(pygame, screen, robot):
    """
    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    pygame.gfxdraw.circle(screen, robot.position[0], robot.position[1], robot.radius - 0.6, (200,200,200,0.5))
    pygame.gfxdraw.circle(screen, robot.position[0], robot.position[1], robot.radius - 0.1, (0,0,0,0.5))
    pygame.gfxdraw.line(screen, robot.position[0], robot.position[1], robot.facing_position[0], robot.facing_position[1], (0,0,0,0.5))


def draw_trail(pygame, screen, robot, disappearing):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    if disappearing and len(robot.position_history) >= 100:
        for i in range(1,100):
            old_pos = robot.position_history[-i]
            if i == 100:
                new_pos = robot.position
            else:
                new_pos = robot.position_history[-i-1]
            for j in range(20):
                # gfxdraw does not support thickness - can instead draw multiple times in the same position to simulate thickness
                pygame.gfxdraw.line(screen, int(old_pos[0]), int(old_pos[1]), int(new_pos[0]), int(new_pos[1]), (0,100,0,int(100-i)))

    else:
        for i in range(len(robot.position_history)):
            old_pos = robot.position_history[i]
            if i+1 >= len(robot.position_history):
                new_pos = robot.position
            else:
                new_pos = robot.position_history[i+1]
            pygame.draw.line(screen, (0,100,0), old_pos, new_pos, 2)


def draw_sensors(pygame, screen, robot, width=5):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    for sensor in robot.sensors:
        end = np.asarray(sensor.line_end)
        origin = np.asarray(sensor.line_start)
        center_L1 = (origin + end) / 2
        angle = math.atan2(origin[1] - end[1], origin[0] - end[0])
        length = np.linalg.norm(end - origin)
        UL = (center_L1[0] + (length / 2.) * np.cos(angle) - (width / 2.) * np.sin(angle),
              center_L1[1] + (width / 2.) * np.cos(angle) + (length / 2.) * np.sin(angle))
        UR = (center_L1[0] - (length / 2.) * np.cos(angle) - (width / 2.) * np.sin(angle),
              center_L1[1] + (width / 2.) * np.cos(angle) - (length / 2.) * np.sin(angle))
        BL = (center_L1[0] + (length / 2.) * np.cos(angle) + (width / 2.) * np.sin(angle),
              center_L1[1] - (width / 2.) * np.cos(angle) + (length / 2.) * np.sin(angle))
        BR = (center_L1[0] - (length / 2.) * np.cos(angle) + (width / 2.) * np.sin(angle),
              center_L1[1] - (width / 2.) * np.cos(angle) - (length / 2.) * np.sin(angle))
        pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), sensor.colour)
        pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), sensor.colour)


def draw_sensor_info(screen, robot, font):
    """

    :param screen:
    :param robot:
    :param font:
    :return:
    """
    for sensor in robot.sensors:
        sensor_value = max(0,sensor.radius  - robot.radius)
        sensor_info = font.render(str(int(sensor_value)), True, (255, 0, 0))
        sensor_info_position = sensor.line_start - (sensor.line_start - sensor.line_end) * 0.10
        sensor_info_position[0] -= 5
        sensor_info_position[1] -= 5
        screen.blit(sensor_info, sensor_info_position)


def draw_wall(pygame, screen, origin, end, width=10, color=(0, 0, 0, 70)):
    """

    :param pygame:
    :param screen:
    :param origin:
    :param end:
    :param width:
    :param color:
    :return:
    """
    end = np.asarray(end)
    origin = np.asarray(origin)
    center_L1 = (origin+end)/2
    angle = math.atan2(origin[1]-end[1],origin[0]-end[0])
    length = np.linalg.norm(end-origin)
    UL = (center_L1[0] + (length / 2.) * np.cos(angle) - (width / 2.) * np.sin(angle),
          center_L1[1] + (width / 2.) * np.cos(angle) + (length / 2.) * np.sin(angle))
    UR = (center_L1[0] - (length / 2.) * np.cos(angle) - (width / 2.) * np.sin(angle),
          center_L1[1] + (width / 2.) * np.cos(angle) - (length / 2.) * np.sin(angle))
    BL = (center_L1[0] + (length / 2.) * np.cos(angle) + (width / 2.) * np.sin(angle),
          center_L1[1] - (width / 2.) * np.cos(angle) + (length / 2.) * np.sin(angle))
    BR = (center_L1[0] - (length / 2.) * np.cos(angle) + (width / 2.) * np.sin(angle),
          center_L1[1] - (width / 2.) * np.cos(angle) - (length / 2.) * np.sin(angle))
    pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), color)
    pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), color)


def draw_grid(pygame, screen, grid_1):
    """

    :param pygame:
    :param screen:
    :param grid:
    :return:
    """
    for squares in grid_1:
        for square in squares:
            pygame.gfxdraw.rectangle(screen,
                                     pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                                     (0, 200, 200, 50))

def draw_dirt(pygame, screen, grid, draw_dirt=True, draw_beacons=False, draw_obstacles=False):
    for squares in grid:
        for square in squares:
            if draw_dirt:
                if not square.visited:
                    pygame.gfxdraw.box(screen,
                                       pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                                       (155, 118, 53, 50))
            if draw_obstacles:
                if square.obstacle:
                    pygame.gfxdraw.box(screen,
                                       pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                                       (0, 0, 0, 10))
            if draw_beacons:
                if square.beacon:
                    pygame.gfxdraw.aacircle(screen, square.position[0]+int(square.size/2), square.position[1]+int(square.size/2), int(square.size/2),
                                       (17, 30, 108, 100))
                    pygame.gfxdraw.filled_circle(screen, square.position[0]+int(square.size/2), square.position[1]+int(square.size/2), int(square.size/2),
                                       (17, 30, 108, 100))

def write_text(pygame, screen, text, position = (1300, 300)):
    """

    :param pygame:
    :param screen:
    :param text:
    :param position:
    :return:
    """
    font = pygame.font.SysFont(None, 24)
    img = font.render(text, True, (0,0,0))
    screen.blit(img, position)

def create_button(pygame, screen, text, x, y, width, height):
    """

    :param pygame:
    :param screen:
    :param text:
    :param x:
    :param y:
    :param width:
    :param height:
    :return:
    """
    smallText = pygame.font.Font("freesansbold.ttf",20)
    txt = smallText.render(text, True, (255, 255, 255))
    button = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (0, 0, 0), button)
    screen.blit(txt, (x + (width / 2) - 80, y + (height / 2) - 10))
    return button
