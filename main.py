import pygame
import visualization
import robotics

WIDTH = 1600
HEIGHT = 900
RADIUS = 50

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
    # create walls

    robot = robotics.create_robot(init_pos=(WIDTH,HEIGHT),radius = 50)
    # create robot

    terminate = False
    current_frame = 0
    while not terminate:
        screen.fill((255,255,255))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate = True

        user_input(pygame.key.get_pressed())
        robot.move()
        visualization.draw_robot(pygame, screen, robot)
        pygame.display.update()
        current_frame += 1

    pygame.quit()