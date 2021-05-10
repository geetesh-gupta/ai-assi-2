from gameUtils import getGame, drawGameLayoutMatrix, GameElements, drawGameElement
from qAgent import QAgent
import random
from constants import GRID


class Directions:
    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'


class Game:
    def __init__(self, noise=0.2):
        game = getGame()
        self.layoutMatrix = game[0]
        self.gameElemsPos = game[1]
        self.agent = QAgent(
            self.gameElemsPos[GameElements.AGENT][0], self.actionFn, self.rewardFn)
        self.noise = noise
        self.gameFinished = False

    def draw(self, screen):
        drawGameLayoutMatrix(self.layoutMatrix, screen)
        self.agent.draw(screen)

    def getLayoutElem(self, pos):
        return self.layoutMatrix[pos[0]][pos[1]]

    def isValidPos(self, pos):
        return self.getLayoutElem(pos) != '#'

    def isWinPos(self, pos):
        return self.getLayoutElem(pos) == 'G'

    def isJumpPos(self, pos):
        return pos in self.gameElemsPos[GameElements.JUMP]

    def isRestartPos(self, pos):
        return pos in self.gameElemsPos[GameElements.RESTART]

    def actionFn(self, state):
        if self.isWinPos(state):
            return ['EXIT']
        else:
            return [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]

    def rewardFn(self, state):
        elem = self.getLayoutElem(state)
        if elem == 'G':
            return 1
        elif elem == 'R':
            return -1
        elif elem == 'J':
            return 5
        elif elem == 'P':
            return 10
        elif elem == '.' or elem == 'S':
            return 0
        return 0

    def resetState(self):
        self.agent.setState(self.gameElemsPos[GameElements.AGENT][0])
        self.gameFinished = False

    def isGameFinished(self):
        return self.gameFinished

    def updateAgent(self):
        state = self.agent.getState()
        action = self.agent.getAction(state)
        if random.random() < self.noise:
            validActions = self.agent.getValidActions(state)
            action = random.choice(validActions)
        self.agent.takeAction(state, action)
        newState = self.transtionFn(state, action)
        if action == 'EXIT':
            reward = 0
        else:
            reward = self.agent.rewardFn(newState)
        self.agent.update(state, action, newState, reward)
        if action == 'EXIT':
            self.gameFinished = True
        # TODO: Rethink agents reward function knowledge

    def transtionFn(self, state, action):
        y, x = state
        # TODO: Add exit condition
        newState = state
        if action == Directions.LEFT and x > 0:
            newState = (y, x - 1)
        elif action == Directions.RIGHT and x < GRID.COL:
            newState = (y, x + 1)
        elif action == Directions.UP and y > 0:
            newState = (y - 1, x)
        elif action == Directions.DOWN and y < GRID.ROW:
            newState = (y + 1, x)
        if self.isValidPos(newState):
            if self.isJumpPos(state):
                newState = self.gameElemsPos[GameElements.POWER][0]
            elif self.isRestartPos(state):
                newState = self.gameElemsPos[GameElements.AGENT][0]
            return newState
        return state

    def reDrawAgent(self, screen):
        prevState = self.agent.prevState
        drawGameElement(self.getLayoutElem(prevState), prevState, screen)
        self.agent.draw(screen)

    def getAgent(self):
        return self.agent
