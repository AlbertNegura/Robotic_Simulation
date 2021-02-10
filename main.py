import pygame
import visualization
import robotics

WIDTH = 1600
HEIGHT = 900
RADIUS = 50

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
        visualization.draw_robot(pygame, screen, robot)
        pygame.display.update()
        current_frame += 1

    pygame.quit()