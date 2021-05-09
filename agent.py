from gameUtils import loadAndScaleImage, drawImage


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
