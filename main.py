from gui import *

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

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
    robot = robotics.create_robot(init_pos=(WIDTH,HEIGHT),radius = RADIUS)
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
        visualization.draw_sensors(pygame, screen, robot)
        pygame.display.update()
        current_frame += 1

    pygame.quit()

    execute()

