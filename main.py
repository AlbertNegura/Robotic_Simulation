import pygame


if __name__ == "__main__":
    pygame.init()
    game_size = (1600,900)
    screen = pygame.display.set_mode(game_size)
    tick_rate = 60

    pygame.font.init()
    pygame.display.set_caption("Robot Visualization")

    # create grid for collision detection
    # create walls
    # create robot

    terminate = False
    current_frame = 0
    while not terminate:
        current_frame += 1

    pygame.quit()