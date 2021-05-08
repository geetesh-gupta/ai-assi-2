from gameUtils import getGame, drawGameLayoutMatrix, drawGameElements


class Game:
    def __init__(self):
        game = getGame()
        self.layoutMatrix = game[0]
        self.gameElemsPos = game[1]

    def draw(self, screen):
        drawGameLayoutMatrix(self.layoutMatrix, screen)
        drawGameElements(self.gameElemsPos, screen)
