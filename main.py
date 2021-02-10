import pygame
import visualization
import robotics
import utils

WIDTH = 1600
HEIGHT = 900
RADIUS = 50

WALLS = []
EDIT_MODE = False
DRAWING = False

origin = None
end = None

def accelerate(wheel, direction):
    if wheel == 0:
        robot.velocity_left += robot.acceleration*direction
    if wheel == 1:
        robot.velocity_right += robot.acceleration*direction
    if wheel == 2 and direction != 0:
        robot.velocity_left += robot.acceleration*direction
        robot.velocity_right += robot.acceleration*direction
    elif wheel == 2:
        robot.velocity_left = 0
        robot.velocity_right = 0



def user_input(key):
    if key[pygame.K_w]:
        accelerate(0,1)
    if key[pygame.K_s]:
        accelerate(0,-1)
    if key[pygame.K_o]:
        accelerate(1,1)
    if key[pygame.K_l]:
        accelerate(1,-1)
    if key[pygame.K_t]:
        accelerate(2,1)
    if key[pygame.K_g]:
        accelerate(2,-1)
    if key[pygame.K_x]:
        accelerate(2,0)
    if key[pygame.K_v]:
        global current_tick
        current_tick = 0
        #reset


if __name__ == "__main__":
    pygame.init()
    game_size = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(game_size)
    tick_rate = 60

    pygame.font.init()
    pygame.display.set_caption("Robot Visualization")

    # create grid for collision detection
    robot = robotics.create_robot(init_pos=(WIDTH,HEIGHT),radius = 20)
    # create robot

    terminate = False
    current_frame = 0
    while not terminate:
        screen.fill((255,255,255))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate = True
            # press "e" to enter / leave edit mode
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    EDIT_MODE = not EDIT_MODE
                    print("Edit mode ", EDIT_MODE)

            if EDIT_MODE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not DRAWING:
                        origin = pygame.mouse.get_pos()
                        DRAWING = True
                        print('origin', origin)
                if event.type == pygame.MOUSEBUTTONUP:
                    if DRAWING:
                        end = pygame.mouse.get_pos()
                        print(origin, end)
                        if origin != None and end != None:
                            WALLS.append((origin, end))
                            print('Drawn')
                    origin = None
                    end = None
                    DRAWING = False



        user_input(pygame.key.get_pressed())
        robot.move()
        for wall in WALLS:
            visualization.draw_wall(pygame, screen, wall[0], wall[1])
        utils.clip(robot.position, [robot.radius + 1, robot.radius + 1],
                   [WIDTH - int(HEIGHT / 2) - robot.radius - 1, HEIGHT - int(HEIGHT / 2) - robot.radius - 1], robot)

        visualization.draw_wall(pygame, screen, [0, 0], [0, HEIGHT - int(HEIGHT / 2)])
        visualization.draw_wall(pygame, screen, [0, HEIGHT - int(HEIGHT / 2)], [WIDTH - int(HEIGHT / 2), HEIGHT - int(HEIGHT / 2)])
        visualization.draw_wall(pygame, screen, [0, 0], [WIDTH - int(HEIGHT / 2), 0])
        visualization.draw_wall(pygame, screen, [WIDTH - int(HEIGHT / 2), 0], [WIDTH - int(HEIGHT / 2), HEIGHT - int(HEIGHT / 2)])

        visualization.draw_robot(pygame, screen, robot)
        pygame.display.update()
        current_frame += 1

    pygame.quit()