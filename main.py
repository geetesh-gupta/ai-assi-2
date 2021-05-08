import pygame
from colors import CustomColors
from constants import GRID_ELEM, GRID, WINDOW
from game import Game

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
screen = pygame.display.set_mode((WINDOW.WIDTH, WINDOW.HEIGHT))

# Set title of screen
pygame.display.set_caption("Reinforcement Learning - Geetesh Gupta")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Get game layout and goal position
game = Game()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (GRID_ELEM.WIDTH + GRID.MARGIN)
            row = pos[1] // (GRID_ELEM.HEIGHT + GRID.MARGIN)

            print("Click ", pos, "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(CustomColors.BASE)
    game.draw(screen)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
