import pygame
from colors import CustomColors
from constants import GRID_ELEM, GRID, WINDOW
from game import Game
import json

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

screen.fill(CustomColors.BASE)
game.draw(screen)
qValues = []
MOVEEVENT, t = pygame.USEREVENT + 1, 100
pygame.time.set_timer(MOVEEVENT, t)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (GRID_ELEM.WIDTH + GRID.MARGIN)
            row = pos[1] // (GRID_ELEM.HEIGHT + GRID.MARGIN)

            print("Click ", pos, "Grid coordinates: ", row, column)
        elif event.type == pygame.KEYUP:
            y, x = game.getAgent().getState()
            # vel = 1
            # if event.key == pygame.K_LEFT and x > 0:
            #     game.moveAgent((y, x - vel))
            # if event.key == pygame.K_RIGHT and x < GRID.COL:
            #     game.moveAgent((y, x + vel))
            # if event.key == pygame.K_UP and y > 0:
            #     game.moveAgent((y - vel, x))
            # if event.key == pygame.K_DOWN and y < GRID.ROW:
            #     game.moveAgent((y + vel, x))
        elif event.type == MOVEEVENT:
            game.updateAgent()
            game.reDrawAgent(screen)
            game.agent.displayQValues()
            qValues.append(game.remap_keys(game.agent.qValueFunc))

    if game.isWinPos(game.agent.getState()):
        done = True
        with open('qValues.json', 'w') as f:
            json.dump(qValues, f)
        game.agent.displayQValues()

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
