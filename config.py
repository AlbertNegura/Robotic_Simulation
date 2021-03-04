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
import  neuralnetwork
import math
import pickle

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

# not handled by config - yet
ITERATIONS = 100
AUTONOMOUS_MODE = False
RNN = True
DRAW_GHOSTS = False

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
    visualization_settings = config['VISUALIZATION']
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

    global HIDDEN_NODES, POPULATION, MUTATION, LIFESPAN, SHOW_EVERY_X_GENERATIONS, SELECTION
    HIDDEN_NODES = int(model_settings['HIDDEN_NODES'])
    POPULATION = int(model_settings['POPULATION'])
    MUTATION = float(model_settings['MUTATION'])
    SELECTION = str(model_settings['SELECTION'])
    LIFESPAN = int(model_settings['LIFESPAN']) # in seconds? frames * tickrate?
    SHOW_EVERY_X_GENERATIONS = int(model_settings['SHOW_EVERY_X_GENERATIONS'])

    global DIRT, DIRT_VALUE, COLLISION_VALUE, SENSOR_VALUE, CLEANING_RANGE
    DIRT = int(terrain_settings['DIRT'])
    CLEANING_RANGE = int(RADIUS/GRID_SIZE)
    DIRT_VALUE = int(terrain_settings['DIRT_VALUE'])
    COLLISION_VALUE = int(terrain_settings['COLLISION_VALUE'])
    SENSOR_VALUE = int(terrain_settings['SENSOR_VALUE'])

    global KEY_SIZE, TICK_RATE, WALL_WIDTH
    KEY_SIZE = int(visualization_settings['KEY_SIZE'])
    TICK_RATE = int(visualization_settings['TICK_RATE'])
    WALL_WIDTH = int(visualization_settings['WALL_WIDTH'])

    global SHOW_VELOCITY_PER_WHEEL, SHOW_SENSORS, SHOW_SENSOR_INFO, DRAW_GRID, DRAW_TRAIL, DISAPPEARING_TRAIL, CLEANING_MODE
    SHOW_VELOCITY_PER_WHEEL = True if str(debug_settings['SHOW_VELOCITY_PER_WHEEL']) == "True" else False
    SHOW_SENSORS = True if str(debug_settings['SHOW_SENSORS']) == "True" else False
    SHOW_SENSOR_INFO = True if str(debug_settings['SHOW_SENSOR_INFO']) == "True" else False
    DRAW_GRID = True if str(debug_settings['DRAW_GRID']) == "True" else False
    DRAW_TRAIL = True if str(debug_settings['DRAW_TRAIL']) == "True" else False
    DISAPPEARING_TRAIL = True if str(debug_settings['DISAPPEARING_TRAIL']) == "True" else False
    CLEANING_MODE = True if str(debug_settings['CLEANING_MODE']) == "True" else False


# Load the configuration and set up some globals
config = configparser.ConfigParser()
config.read('config.ini')
load_config(config)
robot = robotics.create_robot(init_pos=(WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)), radius=RADIUS, acceleration=ACCELERATION, num_sensors=SENSORS, max_radius=SENSOR_LENGTH)

# POPULATION
individuals_list = []
for i in range(math.floor(POPULATION)):
    individuals_list.append(neuralnetwork.RNN(robot.sensor_values(), robot.vr_vl()))

# MAZE
WALLS = []
EDGE_WALLS = []
# keep track of borders separately to apply different rules to them
EDGE_WALLS.append([[0, 0], [0, HEIGHT - int(HEIGHT / 3)]])
EDGE_WALLS.append([[0, HEIGHT - int(HEIGHT / 3)], [WIDTH, HEIGHT - int(HEIGHT / 3)]])
EDGE_WALLS.append([[0, 0], [WIDTH, 0]])
EDGE_WALLS.append([[WIDTH - int(HEIGHT / 3), 0], [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)]])
WALLS.append([[0,0],[-1,-1]]) # need to add a dummy wall


grey = pygame.Color('grey')
black = pygame.Color('black')
dark_grey = ~pygame.Color('grey')

# On screen keyboard display
layout_name = kl.LayoutName.QWERTY
keyboard = klp.KeyboardLayout
key_size = KEY_SIZE
# Keys currently being used, needs to be updated with new keys according to keyboardlayour key key values
valid_keys_kl = [kl.Key.W, kl.Key.S, kl.Key.E, kl.Key.T, kl.Key.G, kl.Key.O, kl.Key.L, kl.Key.V, kl.Key.X, kl.Key.N, kl.Key.M,
                 kl.Key.DIGIT_1, kl.Key.DIGIT_2, kl.Key.DIGIT_3, kl.Key.DIGIT_4, kl.Key.DIGIT_5, kl.Key.DIGIT_6, kl.Key.C,
                 kl.Key.A]
