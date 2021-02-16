import visualization
import utils
import physics
from config import *


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
    global EDIT_MODE, SHOW_VELOCITY_PER_WHEEL, SHOW_SENSORS, SHOW_SENSOR_INFO, DRAW_GRID
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


def execute():
    global EDIT_MODE
    WALLS = []
    EDIT_MODE = False
    DRAWING = False
    origin = None
    end = None

    WALLS.append([[0, 0], [0, HEIGHT - int(HEIGHT / 3)]])
    WALLS.append([[0, HEIGHT - int(HEIGHT / 3)], [WIDTH, HEIGHT - int(HEIGHT / 3)]])
    WALLS.append([[0, 0], [WIDTH, 0]])
    WALLS.append([[WIDTH - int(HEIGHT / 3), 0], [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)]])

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    info_font = pygame.font.SysFont("Arial",11)
    mini_info_font = pygame.font.SysFont("Arial",8)
    pygame.display.set_caption("Robot Visualization")

    terminate = False
    current_frame = 0

    grid = visualization.create_grid(10, WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3))
    visualization.draw_grid(pygame, screen, grid)

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
                            WALLS.append((origin, end))
                            # print('Drawn')
                    origin = None
                    end = None
                    DRAWING = False

            if event.type == pygame.KEYDOWN:
                user_input(pygame.key.get_pressed())
            elif event.type == pygame.KEYUP:
                user_input(pygame.key.get_pressed())

        robot.move()
        robot.adjust_sensors(WALLS)

        for wall in WALLS:
            visualization.draw_wall(pygame, screen, wall[0], wall[1], WALL_WIDTH)
            tangent_coords = utils.circle_line_tangent_point(wall[0], wall[1], robot.position, robot.radius)
            tangent = pygame.Surface((5, 5))
            tangent.fill((200, 0, 0))
            if tangent_coords is not None:
                for t_coords in tangent_coords:
                    screen.blit(tangent, (t_coords[0], t_coords[1]))

            is_intersection, new_position, new_velocity = physics.resolve_wall_collision(wall[0], wall[1], robot.position, robot.velocity, robot.radius, robot.orientation)
            if is_intersection:
                robot.position = new_position
                robot.velocity = new_velocity

        visualization.draw_robot(pygame, screen, robot)
        if SHOW_SENSORS:
            visualization.draw_sensors(pygame, screen, robot)
        if SHOW_SENSOR_INFO:
            visualization.draw_sensor_info(screen, robot, mini_info_font)

        if SHOW_VELOCITY_PER_WHEEL:
            left_vel = info_font.render(str(int(robot.velocity_left/ACCELERATION)), True, (0, 0, 0))
            screen.blit(left_vel, (robot.position[0]-10, robot.position[1]-5))
            right_vel = info_font.render(str(int(robot.velocity_right/ACCELERATION)), True, (0, 0, 0))
            screen.blit(right_vel, (robot.position[0]+10, robot.position[1]-5))

        if DRAW_GRID:
            visualization.draw_grid(pygame, screen, grid)

        # Position text
        visualization.write_text(pygame,screen,"- Frame: ",(1320,70))
        visualization.write_text(pygame,screen,str(current_frame),(1410,70))
        # Position text
        visualization.write_text(pygame,screen,"- Position: ",(1320,100))
        circle_pos = [int(robot.position[0]),int(robot.position[1])]
        visualization.write_text(pygame,screen,str(circle_pos),(1410,100))
        # Vr, Vl
        visualization.write_text(pygame,screen,"- Vl, Vr: ",(1320,130))
        visualization.write_text(pygame,screen,str(round(robot.velocity_left,3)),(1410,130))
        visualization.write_text(pygame,screen,str(round(robot.velocity_right,3)),(1460,130))

        pygame.display.update()
        current_frame += 1

    pygame.quit()
