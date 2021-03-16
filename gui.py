"""Robotic Simulation Software GUI and Main Loop
Authors:
Julien Havel
Kamil Inglot
Albert Negura
Sergi Nogues Farres
"""
import visualization
from config import *
import time
from typing import Any
import grid
import tkinter as tk
from tkinter import filedialog
import evolution
import fitness
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

# set up the pygame environment and keyboard
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# global values for acceleration, wheel controlled and direction
accel = False
wheel = 0
direction = 0
turn = 0
clean_cells = 0


CURRENT_WALL_CONFIG = 0


ALLWALLS = [
           [[[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

           [[[0, 0], [-1, -1]], [[352, 82], [349, 264]], [[349, 263], [494, 258]], [[494, 258], [497, 80]],
               [[497, 80], [352, 80]], [[776, 242], [764, 486]], [[764, 486], [956, 493]], [[956, 493], [947, 242]],
               [[947, 242], [775, 243]],
            [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[0, 0], [-1, -1]], [[650, 0], [650, 125]], [[650, 175], [650, 425]], [[650, 475], [650, 600]],
               [[0, 300], [305, 300]], [[345, 300], [955, 300]], [[995, 300], [1300, 300]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[0, 0], [-1, -1]], [[106, 96], [1201, 95]], [[1178, 362], [1001, 241]], [[1001, 241], [812, 362]],
            [[812, 362], [673, 238]], [[673, 238], [505, 352]], [[505, 352], [331, 218]], [[331, 218], [184, 351]],
            [[85, 509], [1185, 507]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[0, 0], [-1, -1]], [[311, 6], [308, 171]], [[309, 246], [307, 384]], [[305, 471], [293, 600]], [[429, 247],
           [531, 166]], [[531, 166], [689, 248]], [[689, 249], [875, 158]], [[883, 163], [1106, 260]], [[1106, 369],
           [977, 479]], [[977, 479], [825, 382]], [[824, 382], [621, 480]], [[621, 480], [440, 389]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

           [[[5, 5], [5, 595]], [[5, 595], [1600, 595]], [[5, 5], [1600, 5]], [[1295, 5], [1295, 595]], [[5, 5], [0, 0]], [[0, 0], [0, 600]], [[0, 600], [1600, 600]], [[0, 0], [1600, 0]], [[1295, 5], [1295, 595]], [[164, 122], [185, 277]], [[183, 278], [389, 268]], [[389, 268], [373, 128]], [[374, 124], [166, 125]], [[840, 136], [842, 287]], [[842, 287], [1102, 294]], [[1102, 294], [1105, 142]], [[1107, 138], [843, 131]], [[500, 220], [635, 162]], [[635, 162], [743, 261]], [[971, 499], [745, 371]], [[738, 366], [680, 435]], [[680, 435], [573, 351]], [[573, 351], [443, 431]], [[973, 366], [975, 525]], [[975, 525], [1134, 519]], [[1134, 519], [1141, 372]], [[1135, 371], [973, 368]], [[135, 468], [236, 395]], [[236, 395], [280, 480]],
            [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

           [[[5, 5], [5, 595]], [[5, 595], [1600, 595]], [[5, 5], [1600, 5]], [[1295, 5], [1295, 595]], [[5, 5], [0, 0]], [[0, 0], [0, 600]], [[0, 600], [1600, 600]], [[0, 0], [1600, 0]], [[1295, 5], [1295, 595]], [[252, 110], [255, 245]], [[255, 245], [481, 248]], [[481, 248], [487, 119]], [[488, 117], [252, 113]], [[580, 245], [822, 238]], [[928, 113], [960, 248]], [[960, 248], [1088, 241]], [[1088, 241], [1085, 111]], [[1085, 110], [932, 113]], [[1091, 238], [1222, 241]], [[255, 245], [86, 236]], [[468, 596], [478, 334]], [[972, 323], [981, 596]], [[579, 244], [587, 355]], [[587, 355], [833, 358]], [[833, 358], [824, 241]],
            [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[5, 5], [5, 595]], [[5, 595], [1600, 595]], [[5, 5], [1600, 5]], [[1295, 5], [1295, 595]], [[5, 5], [0, 0]], [[0, 0], [0, 600]], [[0, 600], [1600, 600]], [[0, 0], [1600, 0]], [[1295, 5], [1295, 595]], [[78, 92], [472, 83]], [[471, 83], [470, 348]], [[574, 348], [584, 90]], [[584, 88], [869, 101]], [[870, 101], [876, 5]], [[93, 195], [389, 190]], [[389, 190], [378, 595]], [[103, 595], [113, 270]], [[114, 270], [298, 280]], [[298, 280], [288, 380]], [[288, 380], [196, 376]], [[383, 427], [882, 423]], [[743, 422], [744, 169]], [[998, 14], [989, 427]], [[594, 430], [603, 518]], [[603, 514], [786, 510]], [[990, 422], [1143, 423]], [[1294, 347], [1222, 343]], [[1144, 9], [1145, 249]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]]]

WALL_NAMES = ["(D) Empty Room", "(R) Boxes", "(R) Four Rooms", "(R) Zigzag Corridor", "(T) Zigzag Barrier", "(T) Boxes and Zigzags", "(T) Boxface", "(T) Maze"]

current_generation = 0
best_individuals = utils.read_weights_gui()

nn = neuralnetwork.RNN(robot.sensor_values(), np.array([0, 0]), SENSORS, HIDDEN_NODES)
if len(best_individuals)>0:
    nn.update_weights(best_individuals[current_generation])

pygame.font.init()
keyboard_info = kl.KeyboardInfo(
    position=(0, HEIGHT - int(HEIGHT / 3)),
    padding=2,
    color=~grey
)
# set the letter key color, padding, and margin info in px
key_info = kl.KeyInfo(
    margin=10,
    color=black,
    txt_color=black,  # invert grey
    txt_font=pygame.font.SysFont('Arial', key_size // 4),
    txt_padding=(key_size // 6, key_size // 10)
)

# set the letter key size info in px
letter_key_size = (key_size, key_size)
keyboard_layout = klp.KeyboardLayout(
    layout_name,
    keyboard_info,
    letter_key_size,
    key_info,

)

# if key is unused, make it black
unused_key_info = kl.KeyInfo(
    margin=14,
    color=grey,
    txt_color=dark_grey,
    txt_font=pygame.font.SysFont('Arial', key_size // 4),
    txt_padding=(key_size // 6, key_size // 10)
)
# otherwise, make it white if unpressed/inactive and green if pressed/active
used_key_info = kl.KeyInfo(
    margin=14,
    color=pygame.Color('green'),
    txt_color=pygame.Color('white'),
    txt_font=pygame.font.SysFont('Arial', key_size // 4),
    txt_padding=(key_size // 6, key_size // 10)
)
# set all keys to the specified keyboard layout
for key in valid_keys_kl:
    keyboard.update_key(keyboard_layout, key, unused_key_info)

def accelerate():
    """
    Add the corresponding acceleration to the corresponding robot wheels.
    :return:
    """
    global accel, wheel, direction
    if not accel:
        return
    # increase velocity of the corresponding wheel in the corresponding direction by the acceleration value set in the config.ini file
    if wheel == LEFT and not KALMAN_MODE:
        robot.velocity_left += robot.acceleration*direction
    if wheel == RIGHT and not KALMAN_MODE:
        robot.velocity_right += robot.acceleration*direction
    if wheel == BOTH and direction != STOP and not KALMAN_MODE:
        robot.velocity_left += robot.acceleration*direction
        robot.velocity_right += robot.acceleration*direction
    elif wheel == BOTH and not KALMAN_MODE:
        robot.velocity_left = STOP
        robot.velocity_right = STOP

    if KALMAN_MODE:
        if wheel == BOTH and turn == NO_TURN and direction != STOP:
            robot.velocity_left += robot.acceleration*direction
            robot.velocity_right += robot.acceleration*direction
        elif wheel == BOTH and direction == STOP:
            robot.velocity_left = STOP
            robot.velocity_right = STOP
        if wheel == LEFT and turn == TURN_LEFT:
            robot.velocity_left += robot.acceleration*1
            robot.velocity_right += robot.acceleration*-1
        if wheel == RIGHT and turn == TURN_RIGHT:
            robot.velocity_left += robot.acceleration*-1
            robot.velocity_right += robot.acceleration*1



def map_user_input(pgkey):
    """
    Exit the map menu by pressing escape.
    :param pgkey: Pygame Key event triggered.
    :return:
    """
    global MAP_MENU
    if pgkey[pygame.K_ESCAPE]:
        MAP_MENU = None


def user_input(pgkey):
    """
    Handle user input.
    :param pgkey: Pygame Key event triggered.
    :return:
    """
    global EDIT_MODE, REPLAY_MODE, SHOW_VELOCITY_PER_WHEEL, SHOW_SENSORS, SHOW_SENSOR_INFO, DRAW_GRID, DRAW_TRAIL
    global DISAPPEARING_TRAIL, MAP_MENU, CLEANING_MODE, WALLS, DRAW_GHOSTS, AUTONOMOUS_MODE, EVOLVE, KALMAN_MODE
    global CURRENT_WALL_CONFIG, OBSTACLE_GRID
    global accel, wheel, direction, clean_cells, grid_1, current_generation, best_individuals, fitnesses, areas, turn
    if pgkey[pygame.K_w]:
        accel = True
        if not KALMAN_MODE:
            wheel = LEFT
            direction = FORWARD
        else:
            wheel = BOTH
            direction = FORWARD
            turn = NO_TURN
        keyboard.update_key(keyboard_layout, kl.Key.W, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.W, unused_key_info)
    if pgkey[pygame.K_s]:
        accel = True
        if not KALMAN_MODE:
            wheel = LEFT
            direction = BACKWARD
        else:
            wheel = BOTH
            direction = BACKWARD
            turn = NO_TURN
        keyboard.update_key(keyboard_layout, kl.Key.S, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.S, unused_key_info)
    if pgkey[pygame.K_o]:
        accel = True
        wheel = RIGHT
        direction = FORWARD
        keyboard.update_key(keyboard_layout, kl.Key.O, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.O, unused_key_info)
    if pgkey[pygame.K_l]:
        accel = True
        wheel = RIGHT
        direction = BACKWARD
        keyboard.update_key(keyboard_layout, kl.Key.L, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.L, unused_key_info)
    if pgkey[pygame.K_t]:
        accel = True
        wheel = BOTH
        direction = FORWARD
        keyboard.update_key(keyboard_layout, kl.Key.T, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.T, unused_key_info)
    if pgkey[pygame.K_g]:
        accel = True
        wheel = BOTH
        direction = BACKWARD
        keyboard.update_key(keyboard_layout, kl.Key.G, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.G, unused_key_info)
    if pgkey[pygame.K_x]:
        accel = True
        wheel = BOTH
        direction = STOP
        keyboard.update_key(keyboard_layout, kl.Key.X, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.X, unused_key_info)
    if pgkey[pygame.K_v]:
        global current_tick, robot, current_frame
        # reset the robot and simulation
        current_frame = 0
        robot = robotics.create_robot(init_pos=(WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)), radius=RADIUS, acceleration=ACCELERATION, num_sensors=SENSORS, max_radius=SENSOR_LENGTH, grid_size=GRID_SIZE)
        wheel = BOTH
        direction = STOP
        current_tick = STOP
        robot.velocity_left=STOP
        robot.velocity_right=STOP
        clean_cells = 0
        fitnesses = [0]
        areas = [0]
        for cells in grid_1:
            for cell in cells:
                cell.visited = False
        keyboard.update_key(keyboard_layout, kl.Key.V, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.V, unused_key_info)
    if pgkey[pygame.K_k]:
        KALMAN_MODE = not KALMAN_MODE
        keyboard.update_key(keyboard_layout, kl.Key.K, used_key_info)
    else:
        if not KALMAN_MODE:
            keyboard.update_key(keyboard_layout, kl.Key.K, unused_key_info)
    if pgkey[pygame.K_e]:
        EDIT_MODE = not EDIT_MODE
        keyboard.update_key(keyboard_layout, kl.Key.E, used_key_info)
    else:
        if not EDIT_MODE:
            keyboard.update_key(keyboard_layout, kl.Key.E, unused_key_info)
    if pgkey[pygame.K_c]:
        CLEANING_MODE = not CLEANING_MODE
        clean_cells = 0
        for cells in grid_1:
            for cell in cells:
                cell.visited = False
        keyboard.update_key(keyboard_layout, kl.Key.C, used_key_info)
    else:
        if not CLEANING_MODE:
            keyboard.update_key(keyboard_layout, kl.Key.C, unused_key_info)
    if pgkey[pygame.K_1]:
        SHOW_VELOCITY_PER_WHEEL = not SHOW_VELOCITY_PER_WHEEL
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_1, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_1, unused_key_info)
    if pgkey[pygame.K_2]:
        SHOW_SENSORS = not SHOW_SENSORS
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_2, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_2, unused_key_info)
    if pgkey[pygame.K_3]:
        SHOW_SENSOR_INFO = not SHOW_SENSOR_INFO
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_3, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_3, unused_key_info)
    if pgkey[pygame.K_4]:
        DRAW_GRID = not DRAW_GRID
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_4, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_4, unused_key_info)
    if pgkey[pygame.K_5]:
        DRAW_TRAIL = not DRAW_TRAIL
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_5, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_5, unused_key_info)
    if pgkey[pygame.K_6]:
        DISAPPEARING_TRAIL = not DISAPPEARING_TRAIL
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_6, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_6, unused_key_info)
    if pgkey[pygame.K_7]:
        OBSTACLE_GRID = not OBSTACLE_GRID
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_7, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.DIGIT_7, unused_key_info)
    if pgkey[pygame.K_m]:
        MAP_MENU = True
        keyboard.update_key(keyboard_layout, kl.Key.M, used_key_info)
        map_settings()
    else:
        keyboard.update_key(keyboard_layout, kl.Key.M, unused_key_info)
    if pgkey[pygame.K_n]:
        # remove all walls
        WALLS = [([0,0],[-1,-1])]
        keyboard.update_key(keyboard_layout, kl.Key.N, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.N, unused_key_info)
    if pgkey[pygame.K_a]:
        if not KALMAN_MODE:
            AUTONOMOUS_MODE = not AUTONOMOUS_MODE
        else:
            accel = True
            turn = TURN_LEFT
            wheel = LEFT
        keyboard.update_key(keyboard_layout, kl.Key.A, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.A, unused_key_info)
    if pgkey[pygame.K_d]:
        if not KALMAN_MODE:
            AUTONOMOUS_MODE = not AUTONOMOUS_MODE
        else:
            accel = True
            turn = TURN_RIGHT
            wheel = RIGHT
        keyboard.update_key(keyboard_layout, kl.Key.D, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.D, unused_key_info)
    if pgkey[pygame.K_q]:
        if current_generation == len(best_individuals)-1:
            current_generation = 0
        else:
            current_generation = current_generation + 1
        nn.update_weights(best_individuals[current_generation])
        EVOLVE = not EVOLVE
        keyboard.update_key(keyboard_layout, kl.Key.Q, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.Q, unused_key_info)
    if pgkey[pygame.K_z]:
        if current_generation == 0:
            current_generation = len(best_individuals)-1
        else:
            current_generation = current_generation - 1
        nn.update_weights(best_individuals[current_generation])
        EVOLVE = not EVOLVE
        keyboard.update_key(keyboard_layout, kl.Key.Z, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.Z, unused_key_info)
    if pgkey[pygame.K_LEFTBRACKET]:
        if CURRENT_WALL_CONFIG == 0:
            CURRENT_WALL_CONFIG = len(ALLWALLS)-1
        else:
            CURRENT_WALL_CONFIG -= 1
        WALLS = ALLWALLS[CURRENT_WALL_CONFIG]
        EVOLVE = not EVOLVE
        if KALMAN_MODE:
            grid.reset_grid(grid_1)
            obstacles, obstacle_cells, non_obstacle_cells, beacons, beacon_cells = grid.add_grid_obstacles(grid_1,
                                                                                                           WALLS,
                                                                                                           GRID_SIZE,
                                                                                                           WIDTH,
                                                                                                           HEIGHT)
            # beacons, beacon_cells = grid.add_grid_beacons_wall(grid_1, WALLS, GRID_SIZE, WIDTH, HEIGHT)
            robot.initialize_belief_map(grid_1, obstacles, obstacle_cells, non_obstacle_cells)
        keyboard.update_key(keyboard_layout, kl.Key.LEFTBRACKET, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.LEFTBRACKET, unused_key_info)

    if pgkey[pygame.K_RIGHTBRACKET]:
        if CURRENT_WALL_CONFIG == len(ALLWALLS)-1:
            CURRENT_WALL_CONFIG = 0
        else:
            CURRENT_WALL_CONFIG += 1
        WALLS = ALLWALLS[CURRENT_WALL_CONFIG]
        EVOLVE = not EVOLVE
        if KALMAN_MODE:
            grid.reset_grid(grid_1)
            obstacles, obstacle_cells, non_obstacle_cells, beacons, beacon_cells = grid.add_grid_obstacles(grid_1,
                                                                                                           WALLS,
                                                                                                           GRID_SIZE,
                                                                                                           WIDTH,
                                                                                                           HEIGHT)
            # beacons, beacon_cells = grid.add_grid_beacons_wall(grid_1, WALLS, GRID_SIZE, WIDTH, HEIGHT)
            robot.initialize_belief_map(grid_1, obstacles, obstacle_cells, non_obstacle_cells)
        keyboard.update_key(keyboard_layout, kl.Key.RIGHTBRACKET, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.RIGHTBRACKET, unused_key_info)

    if pgkey[pygame.K_b]:
        grid.reset_grid(grid_1)
        obstacles, obstacle_cells, non_obstacle_cells, beacons, beacon_cells = grid.add_grid_obstacles(grid_1, WALLS, GRID_SIZE, WIDTH, HEIGHT)
        # beacons, beacon_cells = grid.add_grid_beacons_wall(grid_1, WALLS, GRID_SIZE, WIDTH, HEIGHT)
        robot.initialize_belief_map(grid_1, obstacles, obstacle_cells, non_obstacle_cells)
        keyboard.update_key(keyboard_layout, kl.Key.RIGHTBRACKET, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.RIGHTBRACKET, unused_key_info)


    # TODO:
    # IF EVOLUTION MODE KEY IS PRESSED
    # display last best generation on training map while all generations train in parallel?
    # OPTIONAL: LOAD IN OPTIONS HERE
    # NOTE: OPTIONS INCLUDE CURRENT WALL CONFIGURATION AND ROBOT
    # EACH EVOLUTION STEP LET ROBOT RUN FOR X TIME STEPS
    # EACH TIME STEP CALCULATE COLLISIONS / SENSOR DATA / CLEANING DATA AND MOTION (+ LOG THEM)
    # AFTER CURRENT GENERATION IS DONE WITH X TIME STEPS, CALCULATE FITNESS VALUE BASED ON COLLISIONS / SENSOR DATA / CLEANING DATA
    # EVOLVE NN WEIGHTS CORRESPONDINGLY
    # GO TO NEXT EVOLUTION STEP
    # BONUS: WORK WITH COPIES OF ROBOT TO ALLOW MULTIPLE INDIVIDUALS FOR EACH GENERATION AND SELECT BEST INDIVIDUAL FOR NEW WEIGHTS
    # evolution.execute(options)
    # execute() WITH RESULTS

    # TODO: pickle dump nn weights of current best robot if key is pressed
    # TODO: pickle load nn weights of robot from saved default pickle file from previous todo
fig = plt.figure(figsize=[3, 3])
ax = fig.add_subplot(111)
canvas = agg.FigureCanvasAgg(fig)

def plot(data):
    """
    Generate a plot of some data
    :param data: the data to plot
    :return: the plot as a pygame image
    """
    ax.clear()
    ax.plot(data, color="b")
    canvas.draw()
    renderer = canvas.get_renderer()

    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()

    return pygame.image.fromstring(raw_data, size, "RGB")
fitnesses = [0]
areas = [0]
surf = plot(fitnesses)
surf2 = plot(areas)

def execute():
    """
    Execute the main loop of the game - add walls, robot, sensors and simulate motion, collisions and user input.
    :return:
    """
    global WALLS, surf, surf2
    global EDIT_MODE
    global accel, wheel, direction, turn
    global current_frame
    global clean_cells
    global grid_1
    global REPLAY_MODE
    global POSITION_HISTORY
    global ORIENTATION_HISTORY
    global fitnesses

    DRAWING = False
    origin = None
    end = None

    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # clock = pygame.time.Clock()

    info_font = pygame.font.SysFont("Arial",11)
    mini_info_font = pygame.font.SysFont("Arial",8)
    pygame.display.set_caption("Robot Visualization")

    terminate = False
    current_frame = 0
    clean_cells = 0

    visualization.draw_grid(pygame, screen, grid_1)
    size_of_grid = len(grid_1)*len(grid_1[0])


    while not terminate:
        screen.fill((255,255,255))
        keyboard_layout.draw(screen)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate = True
            if EDIT_MODE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not DRAWING:
                        origin = pygame.mouse.get_pos()
                        DRAWING = True
                        # print('origin', origin)
                if event.type == pygame.MOUSEBUTTONUP:
                    if DRAWING:
                        end = pygame.mouse.get_pos()
                        # print(origin, end)
                        if origin != None and end != None:
                            origin = utils.clip_value(origin, [0,0], [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)])
                            end = utils.clip_value(end, [0,0], [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)])
                            if origin[0] != end[0] and origin[0] != end[0]: # not a point
                                if origin[0] != 0 or end[0] != 0: # not left wall
                                    if origin[0] != end[0] and origin[0] != WIDTH - int(HEIGHT / 3) or end[0] != WIDTH - int(HEIGHT / 3): # not right wall
                                        if origin[1] != end[1] and origin[1] != 0 or end[1] != 0: # not top wall
                                            if origin[1] != HEIGHT - int(HEIGHT / 3) or end[1] != HEIGHT - int(HEIGHT / 3): # not bottom wall
                                                WALLS.append((origin, end))

                            # print('Drawn')
                    origin = None
                    end = None
                    DRAWING = False

            if event.type == pygame.KEYDOWN:
                user_input(pygame.key.get_pressed())
            elif event.type == pygame.KEYUP:
                accel = False
                user_input(pygame.key.get_pressed())

        for wall in WALLS:
            #print(WALLS)
            visualization.draw_wall(pygame, screen, wall[0], wall[1], WALL_WIDTH, antialiasing=ANTIALIASING)
        for wall in EDGE_WALLS:
            visualization.draw_wall(pygame, screen, wall[0], wall[1], WALL_WIDTH, (100,100,100), antialiasing=ANTIALIASING)
        if accel:
            accelerate()
        if not KALMAN_MODE:
            if AUTONOMOUS_MODE:
                #nn, index, value = evolve.get_current_best()
                vels = nn.feedforward(robot.sensor_values())
                robot.velocity_left = robot.max_vel*vels[0]
                robot.velocity_right = robot.max_vel*vels[1]
            #if EVOLVE:
                #evolve = asyncio.run(asyncevol(evolve))



        robot.move(WALLS)

        # for wall in WALLS:
        #     tangent_coords = utils.circle_line_tangent_point(wall[0], wall[1], robot.position, robot.radius)
        #     tangent = pygame.Surface((5, 5))
        #     tangent.fill((200, 0, 0))
        #     if tangent_coords is not None:
        #         for t_coords in tangent_coords:
        #             screen.blit(tangent, (t_coords[0], t_coords[1]))
        if REPLAY_MODE:
            if len(ORIENTATION_HISTORY) > 0 and len(POSITION_HISTORY) > 0:
                robot.position = POSITION_HISTORY[0]
                POSITION_HISTORY = np.delete(POSITION_HISTORY, (0), axis = 0)
                robot.orientation = ORIENTATION_HISTORY[0]
                ORIENTATION_HISTORY = np.delete(ORIENTATION_HISTORY, (0), axis=0)

        visualization.draw_robot(pygame, screen, robot, antialiasing=ANTIALIASING)
        if current_frame > 2 and (DRAW_TRAIL or DISAPPEARING_TRAIL):
            visualization.draw_trail(pygame, screen, robot, DISAPPEARING_TRAIL)
        robot.adjust_sensors(WALLS)
        robot.adjust_sensors(EDGE_WALLS)

        if SHOW_SENSORS:
            visualization.draw_sensors(pygame, screen, robot, antialiasing=ANTIALIASING)
        if SHOW_SENSOR_INFO:
            visualization.draw_sensor_info(screen, robot, mini_info_font)

        if SHOW_VELOCITY_PER_WHEEL:
            left_vel = info_font.render(str(int(round(robot.velocity_left/0.1))), True, (0, 0, 0))
            screen.blit(left_vel, (robot.position[0]-10, robot.position[1]-5))
            right_vel = info_font.render(str(int(round(robot.velocity_right/0.1))), True, (0, 0, 0))
            screen.blit(right_vel, (robot.position[0]+10, robot.position[1]-5))

        if DRAW_GRID:
            visualization.draw_grid(pygame, screen, grid_1)

        if CLEANING_MODE and not KALMAN_MODE:
            clean_cells, _ = grid.get_cells_at_position_in_radius(grid_1, robot.position, GRID_SIZE, CLEANING_RANGE, clean_cells, beacon_cells = KALMAN_MODE)
            visualization.draw_dirt(pygame, screen, grid_1)
        if KALMAN_MODE:
            if CLEANING_MODE:
                clean_cells, _ = grid.get_cells_at_position_in_radius(grid_1, robot.position, GRID_SIZE, CLEANING_RANGE, clean_cells, beacon_cells = False)
            beacon_cells, robot.grid_pos = grid.get_cells_at_position_in_radius(grid_1, robot.position, GRID_SIZE, int(SENSOR_LENGTH/GRID_SIZE), clean_cells, beacon_cells=KALMAN_MODE)

            visualization.draw_dirt(pygame, screen, grid_1, CLEANING_MODE, OBSTACLE_GRID, KALMAN_MODE)

        # Position text
        visualization.write_text(pygame,screen,"- Frame/FPS: ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.9*HEIGHT)))
        visualization.write_text(pygame,screen,"{:.0f}/{:.2f}".format(current_frame,clock.get_fps()),(WIDTH-int(0.10625*WIDTH),HEIGHT-int(0.9*HEIGHT)))
        # Position text
        visualization.write_text(pygame,screen,"- Position: ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.85*HEIGHT)))
        circle_pos = [int(robot.position[0]),int(robot.position[1])]
        visualization.write_text(pygame,screen,str(circle_pos),(WIDTH-int(0.11875*WIDTH),HEIGHT-int(0.85*HEIGHT)))
        # Vr, Vl
        visualization.write_text(pygame,screen,"- Vl, Vr: ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.8*HEIGHT)))
        visualization.write_text(pygame,screen,str(round(robot.velocity_left,3)),(WIDTH-int(0.11875*WIDTH),HEIGHT-int(0.8*HEIGHT)))
        visualization.write_text(pygame,screen,str(round(robot.velocity_right,3)),(WIDTH-int(0.0875*WIDTH),HEIGHT-int(0.8*HEIGHT)))
        # Cells cleaned
        areas.append(round(clean_cells/size_of_grid*100,3))
        visualization.write_text(pygame,screen,"- Cells Cleaned ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.75*HEIGHT)))
        visualization.write_text(pygame,screen,str(clean_cells)+" / "+str(round(clean_cells/size_of_grid*100,3))+"%",(WIDTH-int(0.0875*WIDTH),HEIGHT-int(0.75*HEIGHT)))
        # Collisions
        visualization.write_text(pygame,screen,"- Collisions ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.7*HEIGHT)))
        visualization.write_text(pygame,screen,str(robot.collisions),(WIDTH-int(0.0875*WIDTH),HEIGHT-int(0.7*HEIGHT)))
        # Current generation
        visualization.write_text(pygame,screen,"- Generation ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.65*HEIGHT)))
        visualization.write_text(pygame,screen,str(current_generation+1),(WIDTH-int(0.0875*WIDTH),HEIGHT-int(0.65*HEIGHT)))
        # Current generation
        visualization.write_text(pygame,screen,"- Autonomous ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.60*HEIGHT)))
        visualization.write_text(pygame,screen,str(AUTONOMOUS_MODE),(WIDTH-int(0.09*WIDTH),HEIGHT-int(0.60*HEIGHT)))
        # Current fitness
        fitnesses.append(round(fitness.fitness(round(clean_cells/size_of_grid*100,3),robot.collisions, np.sum(robot.sensor_values())),3))
        visualization.write_text(pygame,screen,"- Fitness ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.55*HEIGHT)))
        visualization.write_text(pygame,screen,str(fitnesses[-1]),(WIDTH-int(0.09*WIDTH),HEIGHT-int(0.55*HEIGHT)))
        # Fitness plot
        if AUTONOMOUS_MODE:
            if current_frame%TICK_RATE==0:
                surf=plot(fitnesses)
                surf2=plot(areas)
            screen.blit(surf, (WIDTH-int(0.4*WIDTH), HEIGHT-int(0.33*HEIGHT)))
            visualization.write_text(pygame,screen,"Fitness",(WIDTH-int(0.325*WIDTH),HEIGHT-int(0.31*HEIGHT)))
            screen.blit(surf2, (WIDTH-int(0.2*WIDTH), HEIGHT-int(0.33*HEIGHT)))
            visualization.write_text(pygame,screen,"Area Cleaned",(WIDTH-int(0.125*WIDTH),HEIGHT-int(0.31*HEIGHT)))

            # Wall Config
            fitnesses.append(round(fitness.fitness(round(clean_cells/size_of_grid*100,3),robot.collisions, np.sum(robot.sensor_values())),3))
            visualization.write_text(pygame,screen,"- Walls ",(WIDTH-int(0.175*WIDTH),HEIGHT-int(0.50*HEIGHT)))
            visualization.write_text(pygame,screen,str(WALL_NAMES[CURRENT_WALL_CONFIG]),(WIDTH-int(0.12*WIDTH),HEIGHT-int(0.50*HEIGHT)))

        pygame.display.update()
        clock.tick(TICK_RATE)
        current_frame += 1

    pygame.quit()


def map_settings():
    """
    Map loader pygame screen.
    :return:
    """
    global WALLS, MAP_MENU, REPLAY_MODE, POSITION_HISTORY, ORIENTATION_HISTORY, current_frame, grid_1
    click = False
    t = time.localtime()
    while MAP_MENU is not None:
        screen.fill((255,255,255))

        visualization.write_text(pygame, screen, 'MAP CONFIG', (750,100))
        root = tk.Tk()
        root.withdraw()
        mx, my = pygame.mouse.get_pos()

        button_1 = visualization.create_button(pygame, screen, "Save Map", 100, 200, 200, 50)
        button_2 = visualization.create_button(pygame, screen, "Load Map", 100, 300, 200, 50)
        button_3 = visualization.create_button(pygame, screen, "Go Back", 100, 400, 200, 50)
        button_4 = visualization.create_button(pygame, screen, "Save Robot Data", 400, 200, 200, 50)
        button_5 = visualization.create_button(pygame, screen, "Load Robot Data", 400, 300, 200, 50)
        if button_1.collidepoint((mx, my)): #Save Map
            if click:
                current_time = time.strftime("%H:%M:%S", t)
                filename = str('MAP' + current_time + '.pkl')
                filename = filename.replace(":","")
                # print("button 1 clicked", filename)
                with open(filename, 'wb') as output:
                    pickle.dump(WALLS, output, pickle.HIGHEST_PROTOCOL)
                root.update()

        if button_2.collidepoint((mx, my)): #Load Map
            if click:
                file_path = filedialog.askopenfilename()
                root.update()
                # print("button 2 clicked")
                # print(file_path)
                if file_path != "":
                    with open(file_path, 'rb') as input:
                        temp_walls = pickle.load(input)
                        set_walls(temp_walls)
        if button_3.collidepoint((mx,my)): #Back
            if click:
                MAP_MENU = None
                keyboard.update_key(keyboard_layout, kl.Key.M, unused_key_info)
                root.update()
                return
        if button_4.collidepoint((mx,my)): #Save Robot Data
            if click:
                save_bot_data(robot)
                root.update()
        if button_5.collidepoint((mx,my)): #Load Robot Data
            if click:
                file_path = filedialog.askopenfilename()
                root.update()
                if file_path != "":
                    data = np.load(file_path)
                    root.update()
                    POSITION_HISTORY = data['position']
                    ORIENTATION_HISTORY = data['orientation']
                    REPLAY_MODE = not REPLAY_MODE
                    current_frame = 0
                    grid.reset_grid(grid_1)

        click = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                map_user_input(pygame.key.get_pressed())
            elif event.type == pygame.KEYUP:
                map_user_input(pygame.key.get_pressed())
        pygame.display.update()
        clock.tick(60)


def set_walls(walls):
    """
    Sets the WALLS global to the specified walls array. Mainly used for debugging.
    :param walls:
    :return:
    """
    global WALLS
    WALLS = walls


def save_bot_data(robot):
    """
    Saves the current robot position and orientation history based on the current hour, minute, second time.
    :param robot: the robot to save
    :return:
    """
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    filename = str('BOT' + current_time + '.npz')
    filename = filename.replace(":", "")
    np.savez(filename, position = robot.position_history, orientation = robot.orientation_history)
