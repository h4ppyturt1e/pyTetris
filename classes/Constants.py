"""
constants.py -- Constants for tetris

Author: Ryan Nicholas Permana (2024)
"""

import numpy as np

# board constants
WIDTH = 10
HEIGHT = 20
HIDDEN_ROWS = 2

# screen constants
SCREEN_SIZE = (1600, 900)
BLOCK_SIZE = int(SCREEN_SIZE[1] / 24)
FRAME_RATE = 24
REPEAT_RATE = int(1000/FRAME_RATE)

# color constants
COLOR_DICT = {
    0: "black",
    1: "cyan",
    2: "blue",
    3: "orange",
    4: "yellow",
    5: "green",
    6: "purple",
    7: "red"
}

# mino constants
MINO_DICT = {
    "I_PIECE": np.array(
                       [[0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]]
                       ),
    "J_PIECE": np.array(
                       [[2, 0, 0],
                        [2, 2, 2],
                        [0, 0, 0]]),
    "L_PIECE": np.array(
                       [[0, 0, 3],
                        [3, 3, 3],
                        [0, 0, 0]]
                        ),
    "O_PIECE": np.array(
                       [[4, 4],
                        [4, 4]]
                        ),
    "S_PIECE": np.array(
                       [[0, 5, 5],
                        [5, 5, 0],
                        [0, 0, 0]]
                        ),
    "T_PIECE": np.array(
                       [[0, 6, 0],
                        [6, 6, 6],
                        [0, 0, 0]]
                        ),
    "Z_PIECE": np.array(
                       [[7, 7, 0],
                        [0, 7, 7],
                        [0, 0, 0]]
                        )
}

# in ms
LOCK_TIMER_MAX = 4000

# settings constants
KEY_REPEAT_DELAY = 200
ACCELERATED_CHANGE_DELAY = 1000

DAS_MIN = 100
DAS_MAX = 200
ARR_MIN = 0
ARR_MAX = 10
SDF_MIN = 0
SDF_MAX = 20