import random

HEIGHT = 22
WIDTH = 10

pieces = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
buffer = 3

global boardState

""" Rotation system """
with open("SRSrotation.txt") as SRSFile:
    data = [line.rstrip() for line in SRSFile.readlines()]
    tetrominos = {}
    mino = []
    rotation = []

    for line in data:
        if line != "" and line not in pieces:
            rotation.append(line)
        elif line == "":
            mino.append(rotation)
            rotation = []
        elif line in pieces:
            tetrominos[line] = mino
            mino = []
    # print(tetrominos)


class Tetromino:

    def __init__(self, piece: str):
        self.piece = piece
        self.rot = 0
        self.x = 3
        self.y = 0
        self.lockCounter = 0

    def draw(self, boardState):  # draws tetromino in board and returns updated boardState
        # . is empty, X is falling piece, O is locked piece
        rotationArray = tetrominos[self.piece][self.rot]
        length = len(rotationArray)
        toBeFilled = []
        toBeRemoved = []

        for i in range(HEIGHT):
            for j in range(buffer, WIDTH + buffer):
                if boardState[i][j] == "X":
                    # searches for Xs in board to be removed
                    toBeRemoved.append((i, j))
                if i < length and j < length + buffer:
                    newI = i + self.y
                    newJ = j + self.x
                    if rotationArray[i][j-buffer] == "X":
                        # looks at piece rotation template to find Xs
                        if boardState[newI][newJ] in [".", "X"]:
                            # if relative position of X on the board is empty or has temp block, fill
                            toBeFilled.append((newI, newJ))
                        else:
                            # if filled with locked piece or out of bounds, stop drawing attempt
                            return False, boardState  # to signify failure in order to reverse fields

        if toBeRemoved == toBeFilled:
            # print("did not move")
            return False, boardState

        for i, j in toBeRemoved:
            boardState[i] = boardState[i][:j] + "." + boardState[i][j+1:]
        # print("removed: {}".format(toBeRemoved))

        for i, j in toBeFilled:
            boardState[i] = boardState[i][:j] + "X" + boardState[i][j+1:]
        # print("filled: {}".format(toBeFilled))

        return True, boardState  # to signify success

    def rotateCW(self, boardState):
        self.rot = (self.rot + 1) % 4
        if not self.draw(boardState)[0]:
            self.rot = (self.rot - 1) % 4
        return boardState

    def rotateCCW(self, boardState):
        self.rot = (self.rot - 1) % 4
        if not self.draw(boardState)[0]:
            self.rot = (self.rot + 1) % 4
        return boardState

    def moveRight(self, boardState):
        self.x += 1
        if not self.draw(boardState)[0]:
            self.x -= 1
        return boardState

    def moveLeft(self, boardState):
        self.x -= 1
        if not self.draw(boardState)[0]:
            self.x += 1
        return boardState

    def fall(self, boardState):  # remember to add collison testing
        self.y += 1
        attemptDraw = self.draw(boardState)[0]
        if not attemptDraw:
            self.y -= 1
        return boardState, attemptDraw

    def hardDrop(self, boardState):
        print("harddrop")
        attemptDraw = self.draw(boardState)[0]
        while attemptDraw:
            print("R")
            self.y += 1
        return boardState, attemptDraw

    def incrementLock(self):
        self.lockCounter += 1

    def getPiece(self):
        return self.piece

    def getRot(self):
        return self.rot

    def getLockState(self):
        return self.lockCounter

    def getPos(self):
        print("({}, {})".format(self.x, self.y))
        return self.x, self.y