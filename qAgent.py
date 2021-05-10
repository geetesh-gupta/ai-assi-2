from random import random, choice
from time import time
from agent import Agent
from gameUtils import loadAndScaleImage, drawImage


class QAgent():
    def __init__(self, startState, actionFn=None, rewardFn=None, numTraining=100, epsilon=0.3, alpha=0.5, gamma=0.6):
        # S == pos
        self.state = startState
        # pi(s) -> A
        self.policy = {}
        # # R(s)
        # self.rewardFunc = {}
        # V(s)
        self.valueFunc = {}
        # Q(s,a)
        self.qValueFunc = {}

        self.rewardFn = rewardFn
        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.image = loadAndScaleImage('athlete.png')

    def draw(self, screen):
        drawImage(self.image, self.state, screen)

    def getValidActions(self, state):
        return self.actionFn(state)

    def getAction(self, state):
        validActions = self.getValidActions(state)
        if random() < self.epsilon:
            return choice(validActions)
        else:
            return self.computeActionFromQValues(state)

    def getQValue(self, state, action):
        try:
            return self.qValueFunc[(state, action)]
        except KeyError:
            self.qValueFunc[(state, action)] = 0.0
            return 0.0

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
        # if not self.getValidActions(state):
        #     return 0.0
        maxQValue = float('-inf')
        for validAction in self.getValidActions(state):
            maxValue = max(maxQValue, self.getQValue(state, validAction))
        return maxValue

    def computeActionFromQValues(self, state):
        validActions = self.getValidActions(state)
        # if not validActions:
        #     return None
        maxQValue = float('-inf')
        optimalAction = None
        for action in validActions:
            curQValue = self.getQValue(state, action)
            if curQValue > maxQValue:
                maxQValue = curQValue
                optimalAction = action
        if optimalAction is None:
            return choice(validActions)
        return optimalAction

    def update(self, state, action, nextState, reward):
        curQValue = self.getQValue(state, action)
        nextValue = self.getValue(nextState)

        self.qValueFunc[(state, action)] = curQValue + self.alpha * \
            (reward + self.discount * nextValue - curQValue)

        # self.valueFunc[state] = self.computeValueFromQValues(state)
        # self.policy[state] = self.computeActionFromQValues(state)

        self.setState(nextState)

    def setState(self, nextState):
        self.state = nextState

    def takeAction(self, state, action):
        self.prevState = state
        self.prevAction = action

    def getDeltaReward(self, state):
        if self.prevState is not None:
            return self.rewardFn(state) - self.rewardFn(self.prevState)
        return self.rewardFn(state)

    def transition(self, state, action, nextState, deltaReward):
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def startEpisode(self):
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            self.epsilon = 0.0  # no exploration
            self.alpha = 0.0  # no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()

    def registerInitialState(self, state):
        self.startEpisode()
        if self.episodesSoFar == 0:
            print('Beginning %d episodes of Training' % self.numTraining)

    def final(self, state):
        self.transition(
            self.lastState, self.lastAction, state, self.getDeltaReward(state))
        self.stopEpisode()

        if 'episodeStartTime' not in self.__dict__:
            self.episodeStartTime = time()
        if 'lastWindowAccumRewards' not in self.__dict__:
            self.lastWindowAccumRewards = 0.0
        self.lastWindowAccumRewards += state.getReward()

        NUM_EPS_UPDATE = 100
        if self.episodesSoFar % NUM_EPS_UPDATE == 0:
            print('Reinforcement Learning Status:')
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
            if self.episodesSoFar <= self.numTraining:
                trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
                print('\tCompleted %d out of %d training episodes' %
                      (self.episodesSoFar, self.numTraining))
                print('\tAverage Rewards over all training: %.2f' % trainAvg)
            else:
                testAvg = float(self.accumTestRewards) / \
                    (self.episodesSoFar - self.numTraining)
                print('\tCompleted %d test episodes' %
                      (self.episodesSoFar - self.numTraining))
                print('\tAverage Rewards over testing: %.2f' % testAvg)
            print('\tAverage Rewards for last %d episodes: %.2f' %
                  (NUM_EPS_UPDATE, windowAvg))
            print('\tEpisode took %.2f seconds' %
                  (time.time() - self.episodeStartTime))
            self.lastWindowAccumRewards = 0.0
            self.episodeStartTime = time.time()

        if self.episodesSoFar == self.numTraining:
            msg = 'Training Done (turning off epsilon and alpha)'
            print('%s\n%s' % (msg, '-' * len(msg)))

    def getState(self):
        return self.state

    def displayQValues(self):
        states, actions = zip(*self.qValueFunc.keys())
        rows, cols = zip(*states)
        rows = set(rows)
        cols = set(cols)
        print('%5s' % (' '), end=' ')

        for col in cols:
            print('%5d' % (col), end=' ')
        print()

        print("Value Function")
        for row in rows:
            print('%5d' % (row), end=' ')
            for col in cols:
                print('%5.2f' % (self.getValue((row, col))), end=' ')
            print()

        print("Policy")
        for row in rows:
            print('%5d' % (row), end=' ')
            for col in cols:
                print('%5s' % (self.getPolicy((row, col))), end=' ')
            print()
