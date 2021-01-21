import random
from typing import List, Tuple

from tictactoe import EMPTY, STEP_RESULT
class Agent:
    def __init__(self, size, win_length) -> None:
        pass
    def step(self, state: Tuple[List[List[int]], STEP_RESULT], train: bool):
        board = state[0]
        avail = []
        for y in range(3):
            for x in range(3):
                if board[y][x] == EMPTY:
                    avail.append((x, y))
        if (len(avail) > 0):
            return random.choice(avail)
            
        return