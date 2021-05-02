import pygame
import random
from mino import *

BLACK = (50, 50, 50)
WHITE = (200, 200, 200)
blockSize = 30
HEIGHT = 22
WIDTH = 10
WINDOW_HEIGHT = blockSize * HEIGHT
WINDOW_WIDTH = blockSize * WIDTH
pieces = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
piecesInQueue = 5


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH + 200, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


def drawGrid():
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(blockSize * 2, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
    pygame.draw.line(SCREEN, WHITE, (WIDTH * blockSize, 0), (WIDTH * blockSize, WINDOW_HEIGHT), 3)


""" Board file I/O """
def getBoard():
    with open("Board.txt") as boardFile:
        return boardFile.readlines()

""" 7-Bag system """
unseen = []
nextQueue = []  # current piece + next pieces in queue
heldPiece = ""


def getNewPiece() -> str:
    if unseen == []:
        [unseen.append(x) for x in pieces]
        # print(unseen)
    chosenPiece = random.choice(unseen)
    unseen.remove(chosenPiece)
    return chosenPiece


def fillQueue():
    while len(nextQueue) != piecesInQueue + 1:
        nextQueue.append(getNewPiece())


def hold():
    global heldPiece
    if heldPiece == "":
        heldPiece = nextQueue.pop(0)
        fillQueue()
    else:
        temp = nextQueue[0]
        nextQueue[0] = heldPiece
        heldPiece = temp
    print("held:{}\ncurrent:{}\nnext:{}".format(heldPiece, nextQueue[0], nextQueue[1:]))


def startGame():
    clearBoard()
    fillQueue()
    boardState = getBoard()
    isPlaying = True
    # p1 = Tetromino(nextQueue.pop(0))
    # drawPiece(p1)

    # while isPlaying:
    #     if len(nextQueue) != piecesInQueue + 1:
    #         fillQueue()




def clearBoard():
    with open("NewBoard.txt") as clear:
        template = clear.readlines()
    with open("Board.txt", "w") as board:
        board.writelines(template)


if __name__ == '__main__':
    startGame()