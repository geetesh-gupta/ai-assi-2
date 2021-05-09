from gameUtils import getGame, drawGameLayoutMatrix, GameElements, drawGameElement
from pygame import display
from qAgent import QAgent
# from agent import Agent
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

    def draw(self, screen):
        drawGameLayoutMatrix(self.layoutMatrix, screen)
        self.agent.draw(screen)

    def isValidPos(self, pos):
        return self.layoutMatrix[pos[0]][pos[1]] != '#'

    def isWinPos(self, pos):
        return self.layoutMatrix[pos[0]][pos[1]] == 'G'

    def isJumpPos(self, pos):
        return pos in self.gameElemsPos[GameElements.JUMP]

    def isRestartPos(self, pos):
        return pos in self.gameElemsPos[GameElements.RESTART]

    def actionFn(self, state):
        if self.isWinPos(state):
            return 'EXIT'
        else:
            return [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]

    def rewardFn(self, state):
        elem = self.layoutMatrix[state[0]][state[1]]
        if elem == 'G':
            return 200
        elif elem == 'R':
            return -5
        elif elem == 'J':
            return 1
        elif elem == 'P':
            return 5
        elif elem == '.':
            return -10
        return 0

    def resetState(self):
        self.agent.setState(self.gameElemsPos[GameElements.AGENT][0])

    def updateAgent(self):
        state = self.agent.getState()
        action = self.agent.getAction(state)
        # TODO
        if random.random() < self.noise:
            validActions = self.agent.getValidActions(state)
            noisyAction = random.choice(validActions)
            # while noisyAction == action:
            #     noisyAction = random.choice(validActions)
            action = noisyAction
        self.agent.takeAction(state, action)
        newState = self.transtionFn(state, action)
        self.agent.update(state, action, newState,
                          self.agent.rewardFn(newState))
        # TODO: Rethink agents reward function knowledge

    def update(self, screen):
        qValues = []
        while not self.isWinPos(self.agent.getState()):
            self.updateAgent()
            self.reDrawAgent(screen)
            display.flip()
            qValues.append(self.remap_keys(self.agent.qValueFunc))
            # print(self.agent.qValueFunc)
        with open('qValues.json', 'w') as f:
            import json
            json.dump(qValues, f)

    def remap_keys(self, mapping):
        return [{'key': k, 'value': v} for k, v in mapping.items()]

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
        drawGameElement(self.layoutMatrix[prevState[0]]
                        [prevState[1]], prevState, screen)
        self.agent.draw(screen)

    def getAgent(self):
        return self.agent
