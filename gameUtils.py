import pygame
from colors import CustomColors
from constants import GRID, GRID_ELEM
import random


class GameElements:
    GOAL = 'G'
    JUMP = 'J'
    AGENT = 'S'
    POWER = 'P'
    RESTART = 'R'


def getLayoutMatrix():
    layoutMatrix = []
    with open('layouts/main.gg') as f:
        for line in f:
            layoutMatrix.append(line.strip())
    return layoutMatrix


def updateLayoutMatrix(gameLayoutMatrix, possibleGoalPositions, goalPos):
    for pos in possibleGoalPositions:
        curRow = gameLayoutMatrix[pos[0]]
        gameLayoutMatrix[pos[0]] = curRow[:pos[1]] + '.' + curRow[pos[1] + 1:]
    curRow = gameLayoutMatrix[goalPos[0]]
    gameLayoutMatrix[goalPos[0]] = curRow[:goalPos[1]] + 'G' + curRow[goalPos[1] + 1:]
    return gameLayoutMatrix


def getGame():
    gameLayoutMatrix = getLayoutMatrix()
    gameElemsPos = getGameElementPos(gameLayoutMatrix)
    posGoalPosns = gameElemsPos[GameElements.GOAL]
    goalPos = random.choice(posGoalPosns)
    gameElemsPos[GameElements.GOAL] = [goalPos]
    gameLayoutMatrix = updateLayoutMatrix(
        gameLayoutMatrix, posGoalPosns, goalPos)
    return [gameLayoutMatrix, gameElemsPos]


def getGameElementPos(gameLayoutMatrix):
    positions = {
        'G': [],
        'J': [],
        'P': [],
        'R': [],
        'S': []
    }
    for rowIndex, row in enumerate(gameLayoutMatrix):
        for colIndex, val in enumerate(row):
            if val in positions.keys():
                positions[val].append((rowIndex, colIndex))
    return positions


def getPossibleGoalPositions(gameLayoutMatrix):
    posPositions = []
    for rowIndex, row in enumerate(gameLayoutMatrix):
        for colIndex, val in enumerate(row):
            if val == 'G':
                posPositions.append((rowIndex, colIndex))
    return posPositions


def getGoalPos(gameLayoutMatrix):
    goalPos = random.choice(getPossibleGoalPositions(gameLayoutMatrix))
    return goalPos


def drawGoal(goalPos, screen):
    goalImg = loadAndScaleImage('flag.png')
    drawImage(goalImg, goalPos, screen)


def loadAndScaleImage(imagePath):
    image = pygame.image.load('images/' + imagePath).convert_alpha()
    return pygame.transform.scale(image, (GRID_ELEM.WIDTH, GRID_ELEM.HEIGHT))


def drawImage(image, imagePos, screen):
    if imagePos is None:
        return
    screen.blit(image, ((GRID.MARGIN + GRID_ELEM.WIDTH) * imagePos[1] + GRID.MARGIN,
                        (GRID.MARGIN + GRID_ELEM.HEIGHT) * imagePos[0] + GRID.MARGIN))


def drawGridItem(pos, color, screen):
    if pos is None:
        return
    pygame.draw.rect(screen,
                     color,
                     [(GRID.MARGIN + GRID_ELEM.WIDTH) * pos[1] + GRID.MARGIN,
                      (GRID.MARGIN + GRID_ELEM.HEIGHT) * pos[0] + GRID.MARGIN,
                         GRID_ELEM.WIDTH,
                         GRID_ELEM.HEIGHT])


def drawGameLayoutMatrix(gameLayoutMatrix, screen):
    for rowIndex, row in enumerate(gameLayoutMatrix):
        for colIndex, val in enumerate(row):
            drawGameElement(val, (rowIndex, colIndex), screen)


def drawGameElements(gameElemsPos, screen):
    for val, posList in gameElemsPos.items():
        for pos in posList:
            drawGameElement(val, pos, screen)


def drawGameElement(elem, pos, screen):
    if elem == '#':
        drawGridItem(pos, CustomColors.WALL, screen)
    else:
        drawGridItem(pos, CustomColors.GRID, screen)

    powerImg = loadAndScaleImage('lighting.png')
    restartImg = loadAndScaleImage('banner.png')
    # agentImg = loadAndScaleImage('athlete.png')
    jumpImg = loadAndScaleImage('portal.png')
    goalImg = loadAndScaleImage('flag.png')
    if elem == 'J':
        drawImage(jumpImg, pos, screen)
    elif elem == 'R':
        drawImage(restartImg, pos, screen)
    elif elem == 'P':
        drawImage(powerImg, pos, screen)
    elif elem == 'G':
        drawImage(goalImg, pos, screen)
    # elif elem == 'S':
    #     drawImage(agentImg, pos, screen)
