from typing import Tuple, List
from enum import Enum
import copy

EMPTY = -100
X = 1
O = 0



class STEP_RESULT(Enum):
    """
    NONE means no one has won, drawn, or lost yet

    X_WIN means X wins

    O_WIN means O wins

    DRAW means both players tie
    """

    NONE = 0
    X_WIN = 1
    O_WIN = 2
    DRAW = 3


class TicTacToe:
    def __init__(self, size = 3, win_length = 3) -> None:
        self.size = size
        self.win_length = win_length
        self.turn = 0
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        pass

    def state(self, team: int) -> Tuple[List[List[int]], int, STEP_RESULT, int]:
        return copy.deepcopy(self.board), self.turn, self.getEndState(), team
    def apply(self, action: Tuple[int, int]) -> Tuple[List[List[int]], int, STEP_RESULT, int]:
        x, y = action
        if (self.turn % 2 == 0):
            self.board[y][x] = O
        else:
            self.board[y][x] = X

        self.turn += 1
        return self.state(self.turn % 2)

    def convert_val_to_str(self, val):
        if val == EMPTY:
            return " "
        elif val == X:
            return "X"
        return "O"
    def convert_vals_to_str(self, vals):
        return [self.convert_val_to_str(x) for x in vals]
    def __str__(self):
        board_str = "Turn: {} - Board:".format(self.turn)
        for i in range(self.size):
            board_str += "\n{}".format(self.convert_vals_to_str(self.board[i]))
        return board_str
    def getEndState(self) -> STEP_RESULT:
        
        for i in range(self.size):
            sum = 0
            for j in range(self.size):
                sum += self.board[i][j]
            if sum == self.win_length:
                return STEP_RESULT.X_WIN
            elif sum == 0:
                return STEP_RESULT.O_WIN
        
        for i in range(self.size):
            sum = 0
            for j in range(self.size):
                sum += self.board[j][i]
            if sum == self.win_length:
                return STEP_RESULT.X_WIN
            elif sum == 0:
                return STEP_RESULT.O_WIN

        d1 = self.board[0][0] + self.board[1][1] + self.board[2][2] 
        d2 = self.board[2][0] + self.board[1][1] + self.board[0][2] 

        for d in [d1, d2]:
            if d == self.win_length:
                return STEP_RESULT.X_WIN
            elif d == 0:
                return STEP_RESULT.O_WIN

        if (self.turn == self.size ** 2):
            return STEP_RESULT.DRAW
        return STEP_RESULT.NONE