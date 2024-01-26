"""
mino.py -- Mino class for tetris

Author: Ryan Nicholas Permana (2024)

Based off of modern guideline tetris.

Includes the typical 7-bag system, and the hold system.
Rotation system is SRS.
"""
import random as r
import numpy as np
from classes.Constants import *
from classes.Exceptions import *

class Tetromino:

    def __init__(self, boardObject):
        self.pos = (4, 0)
        self.mino = MINO_DICT[Tetromino.getNewPiece()]
        self.lockCounter = LOCK_TIMER_MAX
        self.boardObject = boardObject
        self.bag = [piece for piece in MINO_DICT.keys()]

    def rotate(self, direction):
        if direction == "CW":
            self.mino = self.rotateCW()
        elif direction == "CCW":
            self.mino = self.rotateCCW()
        elif direction == "180":
            self.mino = self.rotate180()

    def rotateCW(self):
        # Rotates the mino clockwise
        new_mino = np.rot90(self.mino)
        if self.checkCollision(self.pos, new_mino):
            raise InvalidMove("Collision detected on clockwise rotation")
        self.mino = new_mino

    def rotate180(self):
        # Rotates the mino 180 degrees
        new_mino = np.rot90(self.mino, 2)
        if self.checkCollision(self.pos, new_mino):
            raise InvalidMove("Collision detected on 180 degree rotation")
        self.mino = new_mino

    def rotateCCW(self):
        # Rotates the mino counter-clockwise
        new_mino = np.rot90(self.mino, 3)
        if self.checkCollision(self.pos, new_mino):
            raise InvalidMove("Collision detected on counter-clockwise rotation")
        self.mino = new_mino

    def fall(self):
        # moves the mino down by 1
        currentBoard = self.boardObject.board
        newPos = (self.pos[0], self.pos[1] + 1)
        if self.checkCollision(currentBoard, newPos):
            raise InvalidMove()
        self.pos = newPos

    def hardDrop(self):
        # moves the mino down until it hits something
        while True:
            try:
                self.fall()
            except InvalidMove:
                break
            
    def moveLeft(self):
        # moves the mino left by 1
        currentBoard = self.boardObject.board
        newPos = (self.pos[0] - 1, self.pos[1])
        if self.checkCollision(currentBoard, newPos):
            raise InvalidMove()
        self.pos = newPos
        
    def moveRight(self):
        # moves the mino right by 1
        currentBoard = self.boardObject.board
        newPos = (self.pos[0] + 1, self.pos[1])
        if self.checkCollision(currentBoard, newPos):
            raise InvalidMove()
        self.pos = newPos

    def incrementLockCounter(self):
        # if mino is sitting on a block/ground, increment lock counter
        if not self.isFloating():
            self.lockCounter += REPEAT_RATE
        
        if self.lockCounter <= 0:
            self.hardDrop()

    def checkCollision(self, newPos, newMino=None):
        # checks for mino collision with the board boundaries and other non-empty blocks
        currentBoard = self.boardObject.board
        
        mino = newMino if newMino is not None else self.mino
        rows, cols = mino.shape

        for y in range(rows):
            for x in range(cols):
                # Check if mino block is filled
                if mino[y][x] == 0:
                    continue

                # Calculate the absolute position on the board
                board_y = newPos[1] + y
                board_x = newPos[0] + x

                # Check for collision with board boundaries
                if board_x < 0 or board_x >= len(currentBoard[0]) or board_y >= len(currentBoard):
                    return True

                # Check for collision with other blocks on the board
                if board_y >= 0 and currentBoard[board_y][board_x] != 0:
                    return True

        return False
    
    def isFloating(self):
        # checks only for the bottom row of the mino for collision
        currentBoard = self.boardObject.board
        
        rows, cols = self.mino.shape
        
        for x in range(cols):
            board_y = self.pos[1] + rows
            board_x = self.pos[0] + x
            
            if board_y >= len(currentBoard):
                return False
            
            if currentBoard[board_y][board_x] != 0:
                return False

        return True

    def getNewPiece(self):
        # returns a random mino from the mino dict
        piece = r.choice(self.bag)
        self.bag.remove(piece)
        
        if not self.bag:
            self.bag = [piece for piece in MINO_DICT.keys()]
        
        return piece

class Playfield:
    
    def __init__(self):
        self.board = np.zeros((HEIGHT + HIDDEN_ROWS, WIDTH), dtype=int)
        self.totalLinesCleared = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.tetrises = 0
    
    def insertPiece(self, piece: Tetromino):
        mino = piece.mino
        rows, cols = mino.shape
        
        for y in range(rows):
            for x in range(cols):
                if mino[y][x] == 0:
                    continue
                
                self.board[piece.pos[1] + y][piece.pos[0] + x] = mino[y][x]
        
        # check for full lines and clear
        self.clearLines()
        
    def clearLines(self):
        # clears full lines and updates line clear stats
        linesCleared = 0
        for y in range(HEIGHT + HIDDEN_ROWS):
            if np.all(self.board[y]):
                self.board = np.delete(self.board, y, axis=0)
                self.board = np.insert(self.board, 0, np.zeros(WIDTH, dtype=int), axis=0)
                linesCleared += 1
        
        # match cases to update line clear stats
        match linesCleared:
            case 1:
                self.singles += 1
            case 2:
                self.doubles += 1
            case 3:
                self.triples += 1
            case 4:
                self.tetrises += 1