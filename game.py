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
        self.agent = QAgent(self.gameElemsPos[GameElements.AGENT][0], self.actionFn)
        self.noise = noise
        self.gameFinished = False

    def draw(self, screen):
        drawGameLayoutMatrix(self.layoutMatrix, screen)
        self.agent.draw(screen)

    def getLayoutElem(self, pos):
        if pos is None:
            return None
        return self.layoutMatrix[pos[0]][pos[1]]

    def isValidPos(self, pos):
        return self.getLayoutElem(pos) != '#'

    def isWinPos(self, pos):
        return self.getLayoutElem(pos) == 'G'

    def isExitPos(self, pos):
        return self.getLayoutElem(pos) == 'G' or self.getLayoutElem(pos) == 'P'

    def isJumpPos(self, pos):
        return pos in self.gameElemsPos[GameElements.JUMP]

    def isRestartPos(self, pos):
        return pos in self.gameElemsPos[GameElements.RESTART]

    def isGameFinished(self):
        return self.gameFinished

    def actionFn(self, state):
        if state is None:
            return []
        elem = self.getLayoutElem(state)
        if self.isExitPos(state):
            return ['EXIT']
        if elem == '#':
            return []

        return [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]

    def rewardFn(self, state, action, newState):
        elem = self.getLayoutElem(newState)
        prevElem = self.getLayoutElem(state)

        if prevElem == 'G' and action == 'EXIT':
            return 1
        elif elem == 'R':
            return -1
        elif elem == 'J':
            return 5
        elif prevElem == 'P' and action == 'EXIT':
            return -1
        elif elem == '.' or elem == 'S':
            return -0.1
        return 0

    def transtionFn(self, state, action):
        if state is None:
            return None
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
            elif self.isExitPos(state):
                newState = None
            return newState
        return state

    def updateAgent(self, screen):
        state = self.agent.getState()
        action = self.agent.getAction(state)
        if random.random() < self.noise:
            validActions = self.agent.getValidActions(state)
            if len(validActions):
                action = random.choice(validActions)
        newState = self.transtionFn(state, action)
        # if action == 'EXIT':
        #     reward = 0
        # else:
        reward = self.rewardFn(state, action, newState)
        # print(state, action, newState, reward)
        self.agent.update(state, action, newState, reward)
        if action == 'EXIT':
            self.gameFinished = True
        else:
            self.reDrawAgent(screen)
        # TODO: Rethink agents reward function knowledge

    def reDrawAgent(self, screen):
        prevState = self.agent.prevState
        drawGameElement(self.getLayoutElem(prevState), prevState, screen)
        self.agent.draw(screen)

    def resetState(self):
        self.agent.setState(self.gameElemsPos[GameElements.AGENT][0])
        self.gameFinished = False

    def getAgent(self):
        return self.agent
