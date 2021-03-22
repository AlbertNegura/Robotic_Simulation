"""Robotic Simulation Software Config Reader
Authors:
Kamil Inglot
Albert Negura
"""
import configparser
import robotics
import pygame
import keyboardlayout as kl
import keyboardlayout.pygame as klp
import neuralnetwork
import math
import pickle
import visualization
import utils
import numpy as np

# Constants loaded via configs.
WIDTH = None
HEIGHT = None
RADIUS = None
LEFT = None
RIGHT = None
BOTH = None
FORWARD = None
BACKWARD = None
STOP = None
ACCELERATION = None
SENSORS = None
SENSOR_LENGTH = None
GRID_SIZE = None
HIDDEN_NODES = None
POPULATION = None
MUTATION = None
SELECTION = None
LIFESPAN = None
SHOW_EVERY_X_GENERATIONS = None
DIRT = None
CLEANING_RANGE = None
DIRT_VALUE = None
COLLISION_VALUE = None
SENSOR_VALUE = None
KEY_SIZE = None
TICK_RATE = None
WALL_WIDTH = None
SHOW_VELOCITY_PER_WHEEL = None
EDIT_MODE = None
SHOW_SENSORS = None
SHOW_SENSOR_INFO = None
DRAW_GRID = None
DRAW_TRAIL = None
DISAPPEARING_TRAIL = None
CLEANING_MODE = None
REPLAY_MODE = None
ITERATIONS = None
MUTATIONS = None
MUTATION_RATE = None
AUTONOMOUS_MODE = None
EVOLVE = None
RNN = None
DRAW_GHOSTS = None
MULTIPROCESSING = None
PROCESSES = None
SENSOR_EXPONENTIAL = None
SELECTED_WALLS = None
KALMAN_MODE = None
TURN_RIGHT = None
TURN_LEFT = None
NO_TURN = None
OBSTACLE_GRID = None
ANTIALIASING = None
SHOW_SENSOR_CIRCLE = None
DEAD_RECKONING_PATH = None
DEAD_RECKONING_GHOST = None
SENSOR_NOISE = None
MOTION_NOISE = None
BEACON_SENSORS = None
ELLIPSES = None

def load_config(config):
    """
    Loads the parameters for this simulation from the specified config file loaded with configparser.
    :param config: configparser.ConfigParser object with the loaded config file
    :return:
    """
    default_settings = config['DEFAULT']
    robot_settings = config['ROBOT']
    model_settings = config['MODEL']
    terrain_settings = config['TERRAIN']
    kalman_settings = config['KALMAN']
    visualization_settings = config['VISUALIZATION']
    multiprocessing_settings = config['MULTIPROCESSING']
    debug_settings = config['DEBUG']

    global WIDTH, HEIGHT

    WIDTH = int(default_settings['WIDTH'])
    HEIGHT = int(default_settings['HEIGHT'])

    global RADIUS, LEFT, RIGHT, BOTH, FORWARD, BACKWARD, STOP, ACCELERATION, SENSORS, SENSOR_LENGTH, GRID_SIZE

    RADIUS = int(robot_settings['RADIUS'])
    LEFT = int(robot_settings['LEFT'])
    RIGHT = int(robot_settings['RIGHT'])
    BOTH = int(robot_settings['BOTH'])
    FORWARD = int(robot_settings['FORWARD'])
    BACKWARD = int(robot_settings['BACKWARD'])
    STOP = int(robot_settings['STOP'])
    ACCELERATION = float(robot_settings['ACCELERATION'])
    SENSORS = int(robot_settings['SENSORS'])
    SENSOR_LENGTH = int(robot_settings['SENSOR_LENGTH'])
    GRID_SIZE = int(robot_settings['GRID_SIZE'])

    global HIDDEN_NODES, POPULATION, ITERATIONS, MUTATION, MUTATIONS, MUTATION_RATE, LIFESPAN, SHOW_EVERY_X_GENERATIONS, SELECTION, SELECTED_WALLS
    HIDDEN_NODES = int(model_settings['HIDDEN_NODES'])
    POPULATION = int(model_settings['POPULATION'])
    ITERATIONS = int(model_settings['ITERATIONS'])
    LIFESPAN = int(model_settings['LIFESPAN'])
    MUTATION = float(model_settings['MUTATION'])
    MUTATIONS = int(model_settings['MUTATIONS'])
    MUTATION_RATE = float(model_settings['MUTATION_RATE'])
    SELECTION = str(model_settings['SELECTION'])
    SHOW_EVERY_X_GENERATIONS = int(model_settings['SHOW_EVERY_X_GENERATIONS'])
    SELECTED_WALLS = str(model_settings['SELECTED_WALLS'])

    global DIRT, DIRT_VALUE, COLLISION_VALUE, SENSOR_VALUE, CLEANING_RANGE, SENSOR_EXPONENTIAL
    DIRT = int(terrain_settings['DIRT'])
    CLEANING_RANGE = int(RADIUS/GRID_SIZE)
    DIRT_VALUE = int(terrain_settings['DIRT_VALUE'])
    COLLISION_VALUE = int(terrain_settings['COLLISION_VALUE'])
    SENSOR_VALUE = int(terrain_settings['SENSOR_VALUE'])
    SENSOR_EXPONENTIAL = True if str(terrain_settings['SENSOR_EXPONENTIAL']) == "True" else False

    global KALMAN_MODE, OBSTACLE_GRID, TURN_LEFT, TURN_RIGHT, NO_TURN, DEAD_RECKONING_PATH, DEAD_RECKONING_GHOST, SENSOR_NOISE, MOTION_NOISE, ELLIPSES, BEACON_SENSORS
    KALMAN_MODE = True if str(kalman_settings['KALMAN_MODE']) == "True" else False
    OBSTACLE_GRID = True if str(kalman_settings['OBSTACLE_GRID']) == "True" else False
    TURN_LEFT = int(kalman_settings['TURN_LEFT'])
    TURN_RIGHT = int(kalman_settings['TURN_RIGHT'])
    NO_TURN = int(kalman_settings['NO_TURN'])
    ELLIPSES = True if str(kalman_settings['ELLIPSES']) == "True" else False
    BEACON_SENSORS = True if str(kalman_settings['BEACON_SENSORS']) == "True" else False
    DEAD_RECKONING_PATH = True if str(kalman_settings['DEAD_RECKONING_PATH']) == "True" else False
    DEAD_RECKONING_GHOST = True if str(kalman_settings['DEAD_RECKONING_GHOST']) == "True" else False
    SENSOR_NOISE = float(kalman_settings['SENSOR_NOISE'])
    MOTION_NOISE = float(kalman_settings['MOTION_NOISE'])

    global KEY_SIZE, TICK_RATE, WALL_WIDTH, ANTIALIASING
    KEY_SIZE = int(visualization_settings['KEY_SIZE'])
    TICK_RATE = int(visualization_settings['TICK_RATE'])
    WALL_WIDTH = int(visualization_settings['WALL_WIDTH'])
    ANTIALIASING = True if str(visualization_settings['ANTIALIASING']) == "True" else False

    global MULTIPROCESSING, PROCESSES
    MULTIPROCESSING = True if str(multiprocessing_settings['MULTIPROCESSING']) == "True" else False
    PROCESSES = int(multiprocessing_settings['PROCESSES'])

    global SHOW_VELOCITY_PER_WHEEL, SHOW_SENSORS, SHOW_SENSOR_CIRCLE, SHOW_SENSOR_INFO, DRAW_GRID, DRAW_TRAIL, DISAPPEARING_TRAIL, DRAW_GHOSTS, RNN, CLEANING_MODE, AUTONOMOUS_MODE, EVOLVE
    SHOW_VELOCITY_PER_WHEEL = True if str(debug_settings['SHOW_VELOCITY_PER_WHEEL']) == "True" else False
    SHOW_SENSORS = True if str(debug_settings['SHOW_SENSORS']) == "True" else False
    SHOW_SENSOR_CIRCLE = True if str(debug_settings['SHOW_SENSOR_CIRCLE']) == "True" else False
    SHOW_SENSOR_INFO = True if str(debug_settings['SHOW_SENSOR_INFO']) == "True" else False
    DRAW_GRID = True if str(debug_settings['DRAW_GRID']) == "True" else False
    DRAW_TRAIL = True if str(debug_settings['DRAW_TRAIL']) == "True" else False
    DISAPPEARING_TRAIL = True if str(debug_settings['DISAPPEARING_TRAIL']) == "True" else False
    DRAW_GHOSTS = True if str(debug_settings['DRAW_GHOSTS']) == "True" else False
    RNN = True if str(debug_settings['RNN']) == "True" else False
    CLEANING_MODE = True if str(debug_settings['CLEANING_MODE']) == "True" else False
    AUTONOMOUS_MODE = True if str(debug_settings['AUTONOMOUS_MODE']) == "True" else False
    EVOLVE = True if str(debug_settings['EVOLVE']) == "True" else False


# Load the configuration and set up some globals
config = configparser.ConfigParser()
config.read('config.ini')
load_config(config)
robot = robotics.create_robot(init_pos=(WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)), radius=RADIUS, acceleration=ACCELERATION, num_sensors=SENSORS, max_radius=SENSOR_LENGTH, grid_size=GRID_SIZE)

# MAZE
WALLS = []
EDGE_WALLS = []
# keep track of borders separately to apply different rules to them
EDGE_WALLS.append([[0, 0], [0, HEIGHT - int(HEIGHT / 3)]])
EDGE_WALLS.append([[0, HEIGHT - int(HEIGHT / 3)], [WIDTH, HEIGHT - int(HEIGHT / 3)]])
EDGE_WALLS.append([[0, 0], [WIDTH, 0]])
EDGE_WALLS.append([[WIDTH - int(HEIGHT / 3)-5, 5], [WIDTH - int(HEIGHT / 3)-5, HEIGHT - int(HEIGHT / 3)-5]])
WALLS = [[[5, 5], [5, HEIGHT - int(HEIGHT / 3)-5]], [[5, HEIGHT - int(HEIGHT / 3)-5], [WIDTH, HEIGHT - int(HEIGHT / 3)-5]],
         [[5, 5], [WIDTH, 5]], [[WIDTH - int(HEIGHT / 3)-5, 5], [WIDTH - int(HEIGHT / 3)-5, HEIGHT - int(HEIGHT / 3)-5]],
         [[5, 5], [0, 0]]]
WALLS.extend(EDGE_WALLS)
grid_1 = visualization.create_grid(GRID_SIZE, WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3))

grey = pygame.Color('grey')
black = pygame.Color('black')
dark_grey = ~pygame.Color('grey')

# On screen keyboard display
layout_name = kl.LayoutName.QWERTY
keyboard = klp.KeyboardLayout
key_size = KEY_SIZE
# Keys currently being used, needs to be updated with new keys according to keyboardlayour key key values
valid_keys_kl = [kl.Key.W, kl.Key.S, kl.Key.E, kl.Key.T, kl.Key.G, kl.Key.O, kl.Key.L, kl.Key.V, kl.Key.X, kl.Key.N, kl.Key.M,
                 kl.Key.DIGIT_1, kl.Key.DIGIT_2, kl.Key.DIGIT_3, kl.Key.DIGIT_4, kl.Key.DIGIT_5, kl.Key.DIGIT_6, kl.Key.DIGIT_7,
                 kl.Key.DIGIT_8, kl.Key.DIGIT_9, kl.Key.DIGIT_0, kl.Key.MINUS, kl.Key.EQUALS, kl.Key.BACKSPACE,
                 kl.Key.C, kl.Key.A, kl.Key.Q, kl.Key.D, kl.Key.K, kl.Key.Z, kl.Key.LEFTBRACKET,kl.Key.RIGHTBRACKET, kl.Key.B]

