from gameUtils import getGame, drawGameLayoutMatrix, GameElements, drawGameElement
from qAgent import QAgent
import random
from constants import GRID
import time


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

    def setAgentToTest(self):
        self.agent.setPrevState

    def getLayoutElem(self, pos):
        if pos is None:
            return None
        return self.layoutMatrix[pos[0]][pos[1]]

    def isValidPos(self, pos):
        return self.getLayoutElem(pos) != '#'

    def isWinPos(self, pos):
        return self.getLayoutElem(pos) == 'G'

    def isExitPos(self, pos):
        return self.getLayoutElem(pos) == 'G'

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
        if elem == 'J':
            return ['JUMP']

        return [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]

    def rewardFn(self, state, action, newState):
        elem = self.getLayoutElem(newState)
        prevElem = self.getLayoutElem(state)

        if prevElem == 'G' and action == 'EXIT':
            return 300
        elif elem == 'R':
            return -10
        elif elem == 'J':
            return 50
        # elif elem == 'P':
        #     return 0
        elif elem == '.' or elem == 'S' or elem == 'P':
            return -1
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

    def trainAgent(self, numIterations):
        curIteration = 0
        totalRewardSoFar = 0.0
        epochSize = 100

        while curIteration < numIterations + 1:

            if curIteration % epochSize == 0:
                if curIteration == 0:
                    print("Begin training...")
                else:
                    print("Completed %d training epochs with average score %f" %
                          (curIteration, totalRewardSoFar / epochSize))
                totalRewardSoFar = 0.0
            if curIteration == numIterations:
                break
            while not self.isGameFinished():
                self.updateAgent()
            totalRewardSoFar += self.agent.getTotalReward()
            # print("Score in current iteration: %f" % self.agent.getTotalReward())
            self.resetState()
            time.sleep(1 / 10000)

            curIteration += 1

    def testAgent(self, numTests, screen):
        for t in range(numTests):
            while not self.isGameFinished():
                self.updateAndRedrawAgent(screen)
                time.sleep(1 / 60)
            self.resetState()
            print("Average Score: %f" % self.agent.getTotalReward())
            time.sleep(40 / 60)

    def updateAgent(self):
        state = self.agent.getState()
        action = self.agent.getAction(state)
        if random.random() < self.noise:
            validActions = self.agent.getValidActions(state)
            if len(validActions):
                action = random.choice(validActions)
        newState = self.transtionFn(state, action)
        reward = self.rewardFn(state, action, newState)
        self.agent.update(state, action, newState, reward)
        if action == 'EXIT':
            # self.resetState()
            self.gameFinished = True

    def updateAndRedrawAgent(self, screen):
        self.updateAgent()
        if not self.isGameFinished():
            self.reDrawAgent(screen)

    def reDrawAgent(self, screen):
        prevState = self.agent.prevState
        drawGameElement(self.getLayoutElem(prevState), prevState, screen)
        self.agent.draw(screen)

    def resetState(self):
        self.agent.setState(self.gameElemsPos[GameElements.AGENT][0])
        self.agent.totalReward = 0
        self.gameFinished = False

    def getAgent(self):
        return self.agent
