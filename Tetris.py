import pygame
import random
from mino import Tetromino

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
fps = 24
maxLockCounter = 4
global boardState


def main():
    fillQueue()
    boardState = getBoard()
    p1 = Tetromino(nextQueue[0])
    boardState = p1.draw(boardState)[1]
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH + 200, WINDOW_HEIGHT))
    fallRate = int(1000/gravity)
    repeatRate = int(1000/fps)
    gameOver = False

    timer = 0
    while not gameOver:
        drawGrid(boardState)

        keyPresses(p1, boardState)

        if timer > fallRate:
            boardState, successFall = p1.fall(boardState)
            if not successFall:
                p1.incrementLock()
            timer = 0

        if p1.getLockState() >= maxLockCounter:
            lockPiece(p1)

        pygame.time.delay(repeatRate)  # this one
        pygame.display.update()
        timer += repeatRate


def keyPresses(curPiece, boardState):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        boardState = curPiece.moveLeft(boardState)
    if keys[pygame.K_RIGHT]:
        boardState = curPiece.moveRight(boardState)
    if keys[pygame.K_DOWN]:
        boardState = curPiece.fall(boardState)[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                boardState = curPiece.rotateCW(boardState)
            elif event.key == pygame.K_z:
                boardState = curPiece.rotateCCW(boardState)
            elif event.key == pygame.K_SPACE:
                boardState = curPiece.hardDrop(boardState)


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


def lockPiece(piece):
    x, y = piece.getPos()



if __name__ == '__main__':
    main()


# TODO 1: check if piece has locked
# if piece is locked, change color of piece
# then, get new piece from queue and fill the queue back up
#