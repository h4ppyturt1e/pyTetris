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
gravity = 1
maxLockCounter = 3
global boardState

def main():
    fillQueue()
    boardState = getBoard()
    p1 = Tetromino(nextQueue[0])
    boardState = p1.draw(boardState)[1]
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH + 200, WINDOW_HEIGHT))
    delay = int(1000/gravity)
    pressed_left = False
    pressed_right = False
    pressed_up = False
    pressed_down = False
    pressed_z = False

    while True:
        drawGrid(boardState)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:  # check for key presses
                if event.key == pygame.K_LEFT:  # left arrow turns left
                    pressed_left = True
                elif event.key == pygame.K_RIGHT:  # right arrow turns right
                    pressed_right = True
                elif event.key == pygame.K_UP:  # up arrow goes up
                    pressed_up = True
                elif event.key == pygame.K_DOWN:  # down arrow goes down
                    pressed_down = True
                elif event.key == pygame.K_z:
                    pressed_z = True
            elif event.type == pygame.KEYUP:  # check for key releases
                if event.key == pygame.K_LEFT:  # left arrow turns left
                    pressed_left = False
                elif event.key == pygame.K_RIGHT:  # right arrow turns right
                    pressed_right = False
                elif event.key == pygame.K_UP:  # up arrow goes up
                    pressed_up = False
                elif event.key == pygame.K_DOWN:  # down arrow goes down
                    pressed_down = False
                elif event.key == pygame.K_z:
                    pressed_z = False

            keys = pygame.key.get_pressed()
            # while keys != []:
            if pressed_left:
                boardState = p1.moveLeft(boardState)
            if pressed_right:
                boardState = p1.moveRight(boardState)
            if pressed_up:
                boardState = p1.rotateCW(boardState)
            if pressed_z:
                boardState = p1.rotateCCW(boardState)
            if pressed_down:
                boardState = p1.fall(boardState)

        boardState = p1.fall(boardState)
        pygame.time.wait(delay)  # this one
        pygame.display.update()


def drawGrid(boardState):
    SCREEN.fill(BLACK)
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(blockSize * 2, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
    pygame.draw.line(SCREEN, WHITE, (WIDTH * blockSize, 0), (WIDTH * blockSize, WINDOW_HEIGHT), 3)
    boardState = [x.strip("/") for x in boardState]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if boardState[y][x] == "X":
                mino = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
                pygame.draw.rect(SCREEN, (252, 3, 252), mino)


""" Board file I/O """
def getBoard():
    with open("NewBoard.txt") as boardFile:
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


# def clearBoard():
#     with open("NewBoard.txt") as clear:
#         template = clear.readlines()
#     with open("Board.txt", "w") as board:
#         board.writelines(template)


if __name__ == '__main__':
    main()
