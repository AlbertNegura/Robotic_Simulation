import pygame
import visualization
import robotics
import utils
import keyboardlayout as kl
import keyboardlayout.pygame as klp
import configparser


def load_config(config):
    default_settings = config['DEFAULT']
    robot_settings = config['ROBOT']
    visualization_settings = config['VISUALIZATION']
    debug_settings = config['DEBUG']

    global WIDTH, HEIGHT

    WIDTH = int(default_settings['WIDTH'])
    HEIGHT = int(default_settings['HEIGHT'])

    global RADIUS, LEFT, RIGHT, BOTH, FORWARD, BACKWARD, STOP, ACCELERATION

    RADIUS = int(robot_settings['RADIUS'])
    LEFT = int(robot_settings['LEFT'])
    RIGHT = int(robot_settings['RIGHT'])
    BOTH = int(robot_settings['BOTH'])
    FORWARD = int(robot_settings['FORWARD'])
    BACKWARD = int(robot_settings['BACKWARD'])
    STOP = int(robot_settings['STOP'])
    ACCELERATION = float(robot_settings['ACCELERATION'])

    global KEY_SIZE, TICK_RATE
    KEY_SIZE = int(visualization_settings['KEY_SIZE'])
    TICK_RATE = int(visualization_settings['TICK_RATE'])

    global SHOW_VELOCITY_PER_WHEEL
    SHOW_VELOCITY_PER_WHEEL = bool(debug_settings['SHOW_VELOCITY_PER_WHEEL'])


def accelerate(wheel, direction):
    if wheel == LEFT:
        robot.velocity_left += robot.acceleration*direction
    if wheel == RIGHT:
        robot.velocity_right += robot.acceleration*direction
    if wheel == BOTH and direction != STOP:
        robot.velocity_left += robot.acceleration*direction
        robot.velocity_right += robot.acceleration*direction
    elif wheel == BOTH:
        robot.velocity_left = STOP
        robot.velocity_right = STOP


def user_input(pgkey):
    global EDIT_MODE
    if pgkey[pygame.K_w]:
        accelerate(LEFT,FORWARD)
        keyboard.update_key(keyboard_layout, kl.Key.W, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.W, unused_key_info)
    if pgkey[pygame.K_s]:
        accelerate(LEFT,BACKWARD)
        keyboard.update_key(keyboard_layout, kl.Key.S, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.S, unused_key_info)
    if pgkey[pygame.K_o]:
        accelerate(RIGHT,FORWARD)
        keyboard.update_key(keyboard_layout, kl.Key.O, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.O, unused_key_info)
    if pgkey[pygame.K_l]:
        accelerate(RIGHT,BACKWARD)
        keyboard.update_key(keyboard_layout, kl.Key.L, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.L, unused_key_info)
    if pgkey[pygame.K_t]:
        accelerate(BOTH,FORWARD)
        keyboard.update_key(keyboard_layout, kl.Key.T, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.T, unused_key_info)
    if pgkey[pygame.K_g]:
        accelerate(BOTH,BACKWARD)
        keyboard.update_key(keyboard_layout, kl.Key.G, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.G, unused_key_info)
    if pgkey[pygame.K_x]:
        accelerate(BOTH,STOP)
        keyboard.update_key(keyboard_layout, kl.Key.X, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.X, unused_key_info)
    if pgkey[pygame.K_v]:
        global current_tick
        current_tick = STOP
        accelerate(BOTH,STOP)
        robot.velocity_left=STOP
        robot.velocity_right=STOP
        #reset
        keyboard.update_key(keyboard_layout, kl.Key.V, used_key_info)
    else:
        keyboard.update_key(keyboard_layout, kl.Key.V, unused_key_info)
    if pgkey[pygame.K_e]:
        EDIT_MODE = not EDIT_MODE
        # print("Edit mode ", EDIT_MODE)
        keyboard.update_key(keyboard_layout, kl.Key.E, used_key_info)
    else:
        if not EDIT_MODE:
            keyboard.update_key(keyboard_layout, kl.Key.E, unused_key_info)


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')
    load_config(config)

    WALLS = []
    EDIT_MODE = False
    DRAWING = False

    origin = None
    end = None

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    info_font = pygame.font.SysFont("Arial",11)
    pygame.font.init()
    pygame.display.set_caption("Robot Visualization")

    grey = pygame.Color('grey')
    black = pygame.Color('black')
    dark_grey = ~pygame.Color('grey')


    layout_name = kl.LayoutName.QWERTY
    keyboard = klp.KeyboardLayout
    key_size = KEY_SIZE
    # set the keyboard position and color info
    valid_keys_kl = [kl.Key.W, kl.Key.S, kl.Key.E, kl.Key.T, kl.Key.G, kl.Key.O, kl.Key.L, kl.Key.V, kl.Key.X]

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

    unused_key_info = kl.KeyInfo(
        margin=14,
        color=grey,
        txt_color=dark_grey,
        txt_font=pygame.font.SysFont('Arial', key_size // 4),
        txt_padding=(key_size // 6, key_size // 10)
    )
    used_key_info = kl.KeyInfo(
        margin=14,
        color=pygame.Color('green'),
        txt_color=pygame.Color('white'),
        txt_font=pygame.font.SysFont('Arial', key_size // 4),
        txt_padding=(key_size // 6, key_size // 10)
    )
    for key in valid_keys_kl:
        keyboard.update_key(keyboard_layout, key, unused_key_info)
    # create grid for collision detection
    robot = robotics.create_robot(init_pos=(WIDTH,HEIGHT),radius = RADIUS, acceleration=ACCELERATION)
    # create robot

    terminate = False
    current_frame = 0
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
                        #print('origin', origin)
                if event.type == pygame.MOUSEBUTTONUP:
                    if DRAWING:
                        end = pygame.mouse.get_pos()
                        #print(origin, end)
                        if origin != None and end != None:
                            WALLS.append((origin, end))
                            #print('Drawn')
                    origin = None
                    end = None
                    DRAWING = False
            if event.type == pygame.KEYDOWN:
                user_input(pygame.key.get_pressed())
            elif event.type == pygame.KEYUP:
                user_input(pygame.key.get_pressed())

        robot.move()
        for wall in WALLS:
            visualization.draw_wall(pygame, screen, wall[0], wall[1])
        utils.clip(robot.position, [robot.radius + 1, robot.radius + 1],
                   [WIDTH - int(HEIGHT / 3) - robot.radius - 1, HEIGHT - int(HEIGHT / 3) - robot.radius - 1], robot)

        visualization.draw_wall(pygame, screen, [0, 0], [0, HEIGHT - int(HEIGHT / 3)])
        visualization.draw_wall(pygame, screen, [0, HEIGHT - int(HEIGHT / 3)], [WIDTH, HEIGHT - int(HEIGHT / 3)])
        visualization.draw_wall(pygame, screen, [0, 0], [WIDTH, 0])
        visualization.draw_wall(pygame, screen, [WIDTH - int(HEIGHT / 3), 0], [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)])

        visualization.draw_robot(pygame, screen, robot)
        if SHOW_VELOCITY_PER_WHEEL:
            left_vel = info_font.render(str(int(robot.velocity_left/ACCELERATION)), True, (0, 0, 0))
            screen.blit(left_vel, (robot.position[0]-10, robot.position[1]-5))
            right_vel = info_font.render(str(int(robot.velocity_right/ACCELERATION)), True, (0, 0, 0))
            screen.blit(right_vel, (robot.position[0]+10, robot.position[1]-5))
        pygame.display.update()
        current_frame += 1

    pygame.quit()