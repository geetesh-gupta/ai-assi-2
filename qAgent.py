import random
from time import time
from gameUtils import loadAndScaleImage, drawImage
from constants import GRID


class QAgent():
    def __init__(self, startState, actionFn=None, rewardFn=None, numTraining=100, epsilon=0.2, alpha=0.9, gamma=0.9):
        # State
        self.state = startState
        self.prevState = None

        # Input functions
        self.actionFn = actionFn

        # Parameters
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.image = loadAndScaleImage('athlete.png')

        # Output Functions
        self.policy = {}
        self.valueFunc = {}
        self.qValueFunc = {}

        # self.rewardFn = rewardFn
        # self.episodesSoFar = 0
        # self.accumTrainRewards = 0.0
        # self.accumTestRewards = 0.0
        # self.numTraining = int(numTraining)

    def draw(self, screen):
        drawImage(self.image, self.state, screen)

    def getValidActions(self, state):
        return self.actionFn(state)

    def getAction(self, state):
        validActions = self.getValidActions(state)
        if random.random() < self.epsilon:
            if len(validActions):
                return random.choice(validActions)
        else:
            return self.getPolicy(state)

            # return self.computeActionFromQValues(state)

    def getQValue(self, state, action):
        try:
            return self.qValueFunc[(state, action)]
        except KeyError:
            self.setQValue(state, action, 0.0)
            return 0.0

    def setQValue(self, state, action, val):
        self.qValueFunc[(state, action)] = val

    def getPolicy(self, state):
        # try:
        #     return self.policy[state]
        # except KeyError:
        #     self.policy[state] = self.computeActionFromQValues(state)
        #     return self.policy[state]
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        # try:
        #     return self.valueFunc[state]
        # except KeyError:
        #     self.valueFunc[state] = self.computeValueFromQValues(state)
        #     return self.valueFunc[state]
        return self.computeValueFromQValues(state)

    def computeValueFromQValues(self, state):
        if not len(self.getValidActions(state)):
            return 0.0
        maxQValue = float('-inf')
        for validAction in self.getValidActions(state):
            maxQValue = max(maxQValue, self.getQValue(state, validAction))

        return maxQValue

    def computeActionFromQValues(self, state):
        # validActions = self.getValidActions(state)
        # if not validActions:
        #     return None
        # maxQValue = float('-inf')
        # optimalAction = None
        # for action in validActions:
        #     curQValue = self.getQValue(state, action)
        #     if curQValue > maxQValue:
        #         maxQValue = curQValue
        #         optimalAction = action
        # if optimalAction is None:
        #     return choice(validActions)

        validActions = self.getValidActions(state)
        optimalValue = self.computeValueFromQValues(state)
        optimalActions = [action for action in validActions if self.getQValue(
            state, action) == optimalValue]

        if len(optimalActions):
            return random.choice(optimalActions)
        else:
            return None

    def update(self, state, action, nextState, reward):
        curQValue = self.getQValue(state, action)
        nextValue = self.getValue(nextState)

        # if action == 'EXIT':
        #     newQValue = reward
        # else:
        newQValue = (1 - self.alpha) * curQValue + self.alpha * \
            (reward + self.discount * nextValue)
        self.setQValue(state, action, newQValue)
        self.setPrevState(state)
        self.setState(nextState)

        # self.valueFunc[state] = self.computeValueFromQValues(state)
        # self.policy[state] = self.computeActionFromQValues(state)

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def setPrevState(self, prevState):
        self.prevState = prevState

    # def getDeltaReward(self, state):
    #     if self.prevState is not None:
    #         return self.rewardFn(state) - self.rewardFn(self.prevState)
    #     return self.rewardFn(state)

    # def transition(self, state, action, nextState, deltaReward):
    #     self.episodeRewards += deltaReward
    #     self.update(state, action, nextState, deltaReward)

    # def startEpisode(self):
    #     self.lastState = None
    #     self.lastAction = None
    #     self.episodeRewards = 0.0

    # def stopEpisode(self):
    #     if self.episodesSoFar < self.numTraining:
    #         self.accumTrainRewards += self.episodeRewards
    #     else:
    #         self.accumTestRewards += self.episodeRewards
    #     self.episodesSoFar += 1
    #     if self.episodesSoFar >= self.numTraining:
    #         # Take off the training wheels
    #         self.epsilon = 0.0  # no exploration
    #         self.alpha = 0.0  # no learning

    # def isInTraining(self):
    #     return self.episodesSoFar < self.numTraining

    # def isInTesting(self):
    #     return not self.isInTraining()

    # def registerInitialState(self, state):
    #     self.startEpisode()
    #     if self.episodesSoFar == 0:
    #         print('Beginning %d episodes of Training' % self.numTraining)

    # def final(self, state):
    #     self.transition(
    #         self.lastState, self.lastAction, state, self.getDeltaReward(state))
    #     self.stopEpisode()

    #     if 'episodeStartTime' not in self.__dict__:
    #         self.episodeStartTime = time()
    #     if 'lastWindowAccumRewards' not in self.__dict__:
    #         self.lastWindowAccumRewards = 0.0
    #     self.lastWindowAccumRewards += state.getReward()

    #     NUM_EPS_UPDATE = 100
    #     if self.episodesSoFar % NUM_EPS_UPDATE == 0:
    #         print('Reinforcement Learning Status:')
    #         windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
    #         if self.episodesSoFar <= self.numTraining:
    #             trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
    #             print('\tCompleted %d out of %d training episodes' %
    #                   (self.episodesSoFar, self.numTraining))
    #             print('\tAverage Rewards over all training: %.2f' % trainAvg)
    #         else:
    #             testAvg = float(self.accumTestRewards) / \
    #                 (self.episodesSoFar - self.numTraining)
    #             print('\tCompleted %d test episodes' %
    #                   (self.episodesSoFar - self.numTraining))
    #             print('\tAverage Rewards over testing: %.2f' % testAvg)
    #         print('\tAverage Rewards for last %d episodes: %.2f' %
    #               (NUM_EPS_UPDATE, windowAvg))
    #         print('\tEpisode took %.2f seconds' %
    #               (time.time() - self.episodeStartTime))
    #         self.lastWindowAccumRewards = 0.0
    #         self.episodeStartTime = time.time()

    #     if self.episodesSoFar == self.numTraining:
    #         msg = 'Training Done (turning off epsilon and alpha)'
    #         print('%s\n%s' % (msg, '-' * len(msg)))

    def displayQValues(self):
        states, actions = zip(*self.qValueFunc.keys())
        rows, cols = zip(*states)
        rows = set(rows)
        cols = set(cols)

        print('----------------------------------------------')
        print("Q Values")
        print('%8s' % (' '), end=' ')

        for action in self.getValidActions((1, 1)):
            print('%8s' % (action), end=' ')
        print('%8s' % ('EXIT'), end=' ')
        print()

        for row in rows:
            for col in cols:
                print('%3d,%3d' % (row, col), end=' ')
                for action in self.getValidActions((row, col)):
                    if action == 'EXIT':
                        print('%40s' % (self.getQValue((row, col), action)), end=' ')
                    else:
                        print('%8.4f' % (self.getQValue((row, col), action)), end=' ')
                print()

        print('----------------------------------------------')
        print('%8s' % (' '), end=' ')

        for col in cols:
            print('%8d' % (col), end=' ')
        print()
        print("Value Function")
        for row in rows:
            print('%8d' % (row), end=' ')
            for col in cols:
                print('%8.4f' % (self.getValue((row, col))), end=' ')
            print()

        print("Policy")
        for row in rows:
            print('%8d' % (row), end=' ')
            for col in cols:
                print('%8s' % (self.getPolicy((row, col))), end=' ')
            print()
