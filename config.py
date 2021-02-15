import configparser
import robotics
import pygame
import keyboardlayout as kl
import keyboardlayout.pygame as klp

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
KEY_SIZE = None
TICK_RATE = None
WALL_WIDTH = None
SHOW_VELOCITY_PER_WHEEL = None
EDIT_MODE = None
SHOW_SENSORS = None
SHOW_SENSOR_INFO = None
DRAW_GRID = None
GRID_SIZE = None

def load_config(config):
    default_settings = config['DEFAULT']
    robot_settings = config['ROBOT']
    visualization_settings = config['VISUALIZATION']
    debug_settings = config['DEBUG']

    global WIDTH, HEIGHT

    WIDTH = int(default_settings['WIDTH'])
    HEIGHT = int(default_settings['HEIGHT'])

    global RADIUS, LEFT, RIGHT, BOTH, FORWARD, BACKWARD, STOP, ACCELERATION, GRID_SIZE

    RADIUS = int(robot_settings['RADIUS'])
    LEFT = int(robot_settings['LEFT'])
    RIGHT = int(robot_settings['RIGHT'])
    BOTH = int(robot_settings['BOTH'])
    FORWARD = int(robot_settings['FORWARD'])
    BACKWARD = int(robot_settings['BACKWARD'])
    STOP = int(robot_settings['STOP'])
    ACCELERATION = float(robot_settings['ACCELERATION'])
    GRID_SIZE = float(robot_settings['GRID_SIZE'])

    global KEY_SIZE, TICK_RATE, WALL_WIDTH
    KEY_SIZE = int(visualization_settings['KEY_SIZE'])
    TICK_RATE = int(visualization_settings['TICK_RATE'])
    WALL_WIDTH = int(visualization_settings['WALL_WIDTH'])

    global SHOW_VELOCITY_PER_WHEEL, SHOW_SENSORS, SHOW_SENSOR_INFO, DRAW_GRID
    SHOW_VELOCITY_PER_WHEEL = bool(debug_settings['SHOW_VELOCITY_PER_WHEEL'])
    SHOW_SENSORS = bool(debug_settings['SHOW_SENSORS'])
    SHOW_SENSOR_INFO = bool(debug_settings['SHOW_SENSOR_INFO'])
    DRAW_GRID = bool(debug_settings['DRAW_GRID'])


config = configparser.ConfigParser()
config.read('config.ini')
load_config(config)
robot = robotics.create_robot(init_pos=(WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)), radius=RADIUS, acceleration=ACCELERATION)

grey = pygame.Color('grey')
black = pygame.Color('black')
dark_grey = ~pygame.Color('grey')

layout_name = kl.LayoutName.QWERTY
keyboard = klp.KeyboardLayout
key_size = KEY_SIZE
# set the keyboard position and color info
valid_keys_kl = [kl.Key.W, kl.Key.S, kl.Key.E, kl.Key.T, kl.Key.G, kl.Key.O, kl.Key.L, kl.Key.V, kl.Key.X,
                 kl.Key.DIGIT_1, kl.Key.DIGIT_2, kl.Key.DIGIT_3, kl.Key.DIGIT_4]