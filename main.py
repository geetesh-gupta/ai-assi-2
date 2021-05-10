import pygame
from colors import CustomColors
from constants import GRID_ELEM, GRID, WINDOW
from game import Game
import argparse


def run_game(numTraining, numTesting):

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
    game.trainAgent(numTraining)
    print("--------Training completed--------")
    print("Knowledge base: Current State and Actions in each state")
    game.agent.displayQValues()

    screen.fill(CustomColors.BASE)
    game.draw(screen)

    MOVEEVENT, t = pygame.event.custom_type(), 200
    RESETEVENT = pygame.event.custom_type()
    pygame.time.set_timer(MOVEEVENT, t)
    iteration = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (GRID_ELEM.WIDTH + GRID.MARGIN)
                row = pos[1] // (GRID_ELEM.HEIGHT + GRID.MARGIN)

                print("Click ", pos, "Grid coordinates: ", row, column)
            elif event.type == MOVEEVENT:
                game.updateAndRedrawAgent(screen)
            elif event.type == RESETEVENT:
                game.resetState()
                game.draw(screen)
        if game.isGameFinished():
            print("Average Score: %f" % game.agent.getTotalReward())
            if iteration == numTesting - 1:
                done = True
            else:
                iteration += 1
                pygame.event.post(pygame.event.Event(RESETEVENT))
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # If you forget this line, the program will 'hang' on exit.
    pygame.quit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get numTraining and numTests')
    parser.add_argument('--numTraining', type=int, nargs=1,
                        help='Define num of training iterations')
    parser.add_argument('--numTest', type=int, nargs=1,
                        help='Define num of test iterations')

    args = parser.parse_args()
    if args.numTraining is not None and args.numTest is not None:
        run_game(args.numTraining[0], args.numTest[0])
    elif args.numTraining is not None:
        run_game(args.numTraining[0], 0)
    elif args.numTest is not None:
        run_game(0, args.numTest[0])
