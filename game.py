from gameUtils import getGame, drawGameLayoutMatrix, drawGameElements, loadAndScaleImage, GameElements, drawGridItem, drawImage, drawGameElement
from colors import CustomColors
from pygame import display


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.image = loadAndScaleImage('athlete.png')

    def draw(self, screen):
        drawImage(self.image, self.pos, screen)
        # drawGameElement(GameElements.AGENT, self.pos, screen)

    def move(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos


class Game:
    def __init__(self, screen):
        game = getGame()
        self.layoutMatrix = game[0]
        self.gameElemsPos = game[1]
        self.agent = Agent(self.gameElemsPos[GameElements.AGENT][0])
        self.screen = screen

    def draw(self):
        drawGameLayoutMatrix(self.layoutMatrix, self.screen)
        # drawGameElements(self.gameElemsPos, self.screen)
        self.agent.draw(self.screen)

    def isValidPos(self, pos):
        return self.layoutMatrix[pos[0]][pos[1]] != '#'

    def isJumpPos(self, pos):
        return pos in self.gameElemsPos[GameElements.JUMP]

    def isRestartPos(self, pos):
        return pos in self.gameElemsPos[GameElements.RESTART]

    def moveAgent(self, newPos):
        if self.isValidPos(newPos):
            oldPos = self.agent.getPos()
            drawGameElement(self.layoutMatrix[oldPos[0]]
                            [oldPos[1]], oldPos, self.screen)
            self.agent.move(newPos)
            self.agent.draw(self.screen)
            display.flip()

            if self.isJumpPos(newPos):
                oldPos = newPos
                newPos = self.gameElemsPos[GameElements.POWER][0]
                drawGameElement(self.layoutMatrix[oldPos[0]]
                                [oldPos[1]], oldPos, self.screen)
                self.agent.move(newPos)
                self.agent.draw(self.screen)
            elif self.isRestartPos(newPos):
                oldPos = newPos
                newPos = self.gameElemsPos[GameElements.AGENT][0]
                drawGameElement(self.layoutMatrix[oldPos[0]]
                                [oldPos[1]], oldPos, self.screen)
                self.agent.move(newPos)
                self.agent.draw(self.screen)

    def getAgent(self):
        return self.agent
