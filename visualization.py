from grid import *
from pygame import gfxdraw

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

def create_button(pygame, screen, text, x, y, width, height):
    smallText = pygame.font.Font("freesansbold.ttf",20)
    txt = smallText.render(text, True, (255, 255, 255))
    button = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (0, 0, 0), button)
    screen.blit(txt, (x + (width / 2), y + (height / 2)))
    return button
