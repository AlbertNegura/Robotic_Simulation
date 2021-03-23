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

def draw_robot(pygame, screen, robot, width = 2, antialiasing = False):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    if antialiasing:
        pygame.gfxdraw.aacircle(screen, int(robot.position[0]),
                                int(robot.position[1]), int(robot.radius-0.6),
                                robot.colour)
        pygame.gfxdraw.filled_circle(screen, int(robot.position[0]),
                                int(robot.position[1]), int(robot.radius-0.6),
                                robot.colour)
        pygame.gfxdraw.aacircle(screen, int(robot.position[0]),
                                int(robot.position[1]), int(robot.radius-0.1),
                                robot.colour2)

        end = np.asarray(robot.position)
        origin = np.asarray(robot.facing_position)
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
        pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), robot.colour2)
        pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), robot.colour2)
    else:
        pygame.draw.circle(screen, robot.colour, robot.position, robot.radius - 0.6)
        pygame.draw.circle(screen, robot.colour2, robot.position, robot.radius - 0.1, 1)
        pygame.draw.line(screen, robot.colour2, robot.position, robot.facing_position, 2)

def draw_ghost(pygame, screen, position, orientation, radius):
    """
    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    position = [int(position[0]), int(position[1])]
    facing_position = utils.rotate_line(position, radius, orientation)
    pygame.draw.circle(screen, (255,150,150), [position[0], position[1]], int(radius - 0.1), 5)
    pygame.draw.line(screen, (0,0,0), [position[0], position[1]], [int(facing_position[0]), int(facing_position[1])], 2)
    # pygame.gfxdraw.circle(screen, position[0], position[1], int(radius - 0.6), (150,150,150,100))
    # pygame.gfxdraw.circle(screen, position[0], position[1], int(radius - 0.1), (0,0,0,100))
    # pygame.gfxdraw.line(screen, position[0], position[1], int(facing_position[0]), int(facing_position[1]), (0,0,0,100))

def draw_sensor_circle(pygame, screen, position, radius):
    """
    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    position = [int(position[0]), int(position[1])]
    pygame.draw.circle(screen, (255,211,0,100), position, int(radius), 4)


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

def draw_trail_kalman(pygame, screen, trail, disappearing, color):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    for i in range(1,len(trail)):
        old_pos = [int(trail[i][0]),int(trail[i][1])]
        if i+1 >= len(trail):
            new_pos = [int(trail[i][0]),int(trail[i][1])]
        else:
            new_pos = [int(trail[i+1][0]),int(trail[i+1][1])]

        pygame.draw.line(screen, color, old_pos, new_pos, 2)

def draw_sensors(pygame, screen, robot, width=5, antialiasing = False):
    """

    :param pygame:
    :param screen:
    :param robot:
    :return:
    """
    for sensor in robot.sensors:
        if antialiasing:
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
        else:
            pygame.draw.line(screen, sensor.colour, sensor.line_start, sensor.line_end, width)


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


def draw_wall(pygame, screen, origin, end, width=10, color=(0, 0, 0, 70), antialiasing = False):
    """

    :param pygame:
    :param screen:
    :param origin:
    :param end:
    :param width:
    :param color:
    :return:
    """
    if antialiasing:
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
    else:
        pygame.draw.line(screen, color, origin, end, width)

def draw_initial_grid(pygame, screen, grid):
    for squares in grid:
        for square in squares:
            pygame.gfxdraw.rectangle(screen,
                                     pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                                     (0, 200, 200, 50))

def draw_kalman_estimates(pygame, screen, estimates, variances, pos_ests, pos_ests2, robot, width, height, lines_to_draw, draw_ellipses):
    if draw_ellipses:
        values_to_plot = len(estimates) if len(estimates) < 10 else 10
        for i in range(values_to_plot):
            estimate = estimates[-i]
            estimate[0] = np.clip(estimate[0],0, width - int(height/3))
            estimate[1] = np.clip(estimate[1],0, height - int(height/3))

            orientation = estimate[2]+90


            variance = variances[-i][:2,:2]
            if np.any(np.isnan(variance)) or len(variance) < 2 or len(variance[0]) < 2:
                return
            eigs = np.linalg.eigvalsh(variance)
            var_x = np.sqrt(eigs[0])*estimate[0]
            var_y = np.sqrt(eigs[1])*estimate[1]

            if not np.isnan(var_x) and not np.isnan(var_y):
                rect = pygame.Rect((int(estimate[0]-int(var_x/2)), int(estimate[1]-int(var_y/2))), (int(var_x), int(var_y)))
                shape_surf = pygame.Surface((int(var_x), int(var_y)))
                shape_surf.set_colorkey((0,0,0))
                pygame.draw.ellipse(shape_surf, (17,30,108,100), (0,0,*rect.size), 2)
                rotated_surf = pygame.transform.rotate(shape_surf, orientation)
                screen.blit(rotated_surf, rotated_surf.get_rect(center=rect.center))
                # pygame.gfxdraw.ellipse(screen, int(estimate[0]), int(estimate[1]), int(var_x), int(var_y), (17, 30, 108, 100))
    if lines_to_draw == 0:
        return
    for i in range(5, len(pos_ests)):
        if i%3 == 0:
            if lines_to_draw == 1 or lines_to_draw == 3:
                estimate1 = pos_ests[i-3]
                estimate2 = pos_ests[i]
                lowerx = robot.position[0]-50 if i >= len(pos_ests) - 5 else 0
                lowery = robot.position[1]-50 if i >= len(pos_ests) - 5 else 0
                upperx = robot.position[0]+50 if i >= len(pos_ests) - 5 else width - (height/3)
                uppery = robot.position[1]+50 if i >= len(pos_ests) - 5 else height - (height/3)
                estimate1[0] = np.clip(estimate1[0],lowerx, upperx)
                estimate1[1] = np.clip(estimate1[1],lowery, uppery)
                estimate2[0] = np.clip(estimate2[0],lowerx, upperx)
                estimate2[1] = np.clip(estimate2[1],lowery, uppery)
                pygame.draw.line(screen, (200, 50, 200, 100), (int(estimate1[0]), int(estimate1[1])),(int(estimate2[0]), int(estimate2[1])),2)
            if lines_to_draw == 2 or lines_to_draw == 3:
                estimate1 = pos_ests2[i-3]
                estimate2 = pos_ests2[i]
                lowerx = robot.position[0]-50 if i >= len(pos_ests2) - 5 else 0
                lowery = robot.position[1]-50 if i >= len(pos_ests2) - 5 else 0
                upperx = robot.position[0]+50 if i >= len(pos_ests2) - 5 else width - (height/3)
                uppery = robot.position[1]+50 if i >= len(pos_ests2) - 5 else height - (height/3)
                estimate1[0] = np.clip(estimate1[0],lowerx, upperx)
                estimate1[1] = np.clip(estimate1[1],lowery, uppery)
                estimate2[0] = np.clip(estimate2[0],lowerx, upperx)
                estimate2[1] = np.clip(estimate2[1],lowery, uppery)
                pygame.draw.line(screen, (100, 100, 50, 100), (int(estimate1[0]), int(estimate1[1])),(int(estimate2[0]), int(estimate2[1])),2)



def draw_grid(pygame, screen, grid, cleaning_mode = False, draw_grid = False, screen2 = None):
    """

    :param pygame:
    :param screen:
    :param grid:
    :return:
    """
    if draw_grid:
        if screen2 is not None:
            screen.blit(screen2,(0,0))
    for squares in grid:
        for square in squares:
                # pygame.gfxdraw.rectangle(screen,
                #                          pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                #                          (0, 200, 200, 50))
            if cleaning_mode:
                if not square.visited:
                    pygame.gfxdraw.box(screen,
                                       pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                                       (155, 118, 53, 50))

def draw_beacons_and_obstacles(pygame, screen, grid, draw_beacons=False, draw_obstacles=False, beacon_cells_list = None, obstacle_cells_list = None):
    if draw_beacons:
        for i,j in beacon_cells_list:
            square = grid[j][i] # for some reason, it's inverted
            if square.beacon:
                pygame.gfxdraw.aacircle(screen, square.position[0]+int(square.size/2), square.position[1]+int(square.size/2), int(square.size/2),
                                   (17, 30, 108, 100))
                pygame.gfxdraw.filled_circle(screen, square.position[0]+int(square.size/2), square.position[1]+int(square.size/2), int(square.size/2),
                                   (17, 30, 108, 100))
    if draw_obstacles:
        for i,j in obstacle_cells_list:
            square = grid[i][j]
            if square.obstacle:
                pygame.gfxdraw.box(screen,
                                   pygame.Rect(square.position[0], square.position[1], square.size, square.size),
                                   (0, 0, 0, 10))

def write_text(pygame, screen, text, position = (1300, 300), font = None):
    """

    :param pygame:
    :param screen:
    :param text:
    :param position:
    :return:
    """
    img = font.render(text, True, (0,0,0))
    screen.blit(img, position)

def write_text_list(pygame, screen, text, position=(1300, 300), WIDTH = 1600, HEIGHT = 900, font = None):
    """

    :param pygame:
    :param screen:
    :param text:
    :param position:
    :return:
    """
    pos_iterator = [0,int(0.05*HEIGHT)]
    for i in range(len(text)):
        t = text[i]
        img = font.render(t, True, (0, 0, 0))
        screen.blit(img, (position[0] + pos_iterator[0]*i, position[1] + pos_iterator[1]*i))

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


def draw_lines_to_sensors(pygame, screen, position, grid, beacon_cells):
    for x,y in beacon_cells:
        square = grid[y][x]
        end_pos = (square.position[0],square.position[1])
        pygame.draw.line(screen, (150,0,0), position, end_pos, 1)


def draw_beacon_circle(pygame, screen, position2, grid, beacon_cells):
    """
    :param pygame:
    :param screen:
    :param robot:
    :return:
    """

    for x,y in beacon_cells:
        square = grid[y][x]
        position = (square.position[0],square.position[1])
        radius = np.abs(np.linalg.norm(np.subtract(position,position2)))
        pygame.draw.circle(screen, (0, 211, 255, 100), position, int(radius), 4)



        '''[]

If we attach an automatic controller to the robot, such as the one we have evolved for the previous assignment, we can see that despite the movements being quite accurately predicted, the dead reckoning path is completely displaced due to the collisions. Furthermore, possibly due to the velocity of the robot, the kalman estimated and predicted paths are slightly displaced from the actual positions of the robot, but are not too far behind in cases where either bilateration or triangulation can be applied. Furthermore, due to the high velocity, the separation between the estimated and predicted poses is significantly more distinguishable.



[] 

We hope you enjoyed our video presentation on self-localization using a regular Kalman filter. We intend to continue working on this project and add additional features and visualization methods while optimizing existing ones. Thank you for listening!'''
        