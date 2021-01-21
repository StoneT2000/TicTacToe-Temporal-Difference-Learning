import copy
import random
from typing import List, Tuple

from tictactoe import EMPTY, O, STEP_RESULT, X
class Agent:
    def __init__(self, size, win_length, step_size_param=0.4, explore_ratio=0.25, include_end_game_bias=True) -> None:
        """
        `explore_ratio` is probability of instead of choosing action based on highest value, but choose an action that leads to the least explored state

        include_end_game_bias is whether or not to tell the agent the rules of the game and use that to aid it's learniing. If false, the agent will learn the winning rules of TicTacToe from scratch (and it can do it! just needs time)
        """
        self.value_func_table = dict()
        self.state_explore_count = dict()


        self.size = size
        self.win_length = win_length
        self.step_size_param = step_size_param
        self.explore_ratio = explore_ratio
        self.include_end_game_bias = include_end_game_bias

        self.curr_state_history = []
        # how many possible states are there???? a lot
        # state serialzation method:
        # a 0 = empty, 1 = O, 2 = X
        # condense these numbers into one string of size ** 2 characters gives board config in a row by row format

        # e.g. 000000000 is an empty board
        # assuming we're always playing 2nd and are X

        # horizontal solutions
        # for x in range(size - win_length):
    def value(self, state):
        # check if in end state
        board = state[0]
        turn = state[1]
        team = state[3]
        serialization = self.serialize_board(team, board)
        if serialization in self.value_func_table:
            return self.value_func_table[serialization]

        if self.include_end_game_bias:
            win_sum = self.win_length
            lose_sum = 0
            if team == O:
                win_sum = 0
                lose_sum = self.win_length

            for i in range(self.size):
                sum = 0
                for j in range(self.size):
                    sum += board[i][j]
                if sum == win_sum:
                    return 1
                elif sum == lose_sum:
                    return 0
            
            for i in range(self.size):
                sum = 0
                for j in range(self.size):
                    sum += board[j][i]
                if sum == win_sum:
                    return 1
                elif sum == lose_sum:
                    return 0

            d1 = board[0][0] + board[1][1] + board[2][2] 
            d2 = board[2][0] + board[1][1] + board[0][2] 

            for d in [d1, d2]:
                if d == win_sum:
                    return 1
                elif d == lose_sum:
                    return 0

            if (turn == self.size ** 2):
                return 0

        if serialization not in self.value_func_table:
            self.value_func_table[serialization] = 0.5
            return 0.5

    def serialize_board(self, team: int, board: List[List[int]]):
        serialization = str(team)
        for i in range(self.size):
            for j in range(self.size):
                val =  board[i][j]
                if val == X:
                    serialization += "X"
                elif val == O:
                    serialization += "O"
                else:
                    serialization += "-"
        return serialization

    def step(self, state: Tuple[List[List[int]], int, STEP_RESULT, int], train: bool):
        """
        When training is on, the agent will do more exploration and also calculate updates to value function table

        """


        if train:
            # when training, we keep track of past state for TD learning later
            self.curr_state_history.append(state)
       
        board = state[0]
        turn = state[1]
        curr_res = state[2]
        team = state[3]

        # curr_res not equal to NONE means that episode is finished
        if curr_res != STEP_RESULT.NONE:
            
            if train:
                
                reward = 0
                if team == X and curr_res == STEP_RESULT.X_WIN:
                    reward = 1
                elif team == O and curr_res == STEP_RESULT.O_WIN:
                    reward = 1
                # if train is also true, we proceed to update our value function
                self.update_value_func(reward)
                # reset accumulated history
                self.curr_state_history = []
            return
        

        # find all possible moves
        possible_moves = []
        for y in range(self.size):
            for x in range(self.size):
                if board[y][x] == EMPTY:
                    possible_moves.append((x, y))

        
        chosen_move = possible_moves[0]
        chosen_state = None

        # if training, a percent of the time we will explore the least explored state as opposed to maxmizing value
        if train and random.random() < self.explore_ratio:
            least_explored_count = None
            for x, y in possible_moves:
                # create a potential state if we were to do this particular move
                temp_board = copy.deepcopy(board)
                temp_board[y][x] = team
                temp_state = (temp_board, turn + 1, None, team)

                serialization = self.serialize_board(team, temp_board)
                if serialization not in self.state_explore_count:
                    self.state_explore_count[serialization] = 0

                c = self.state_explore_count[serialization]
                if least_explored_count == None or c < least_explored_count:
                    least_explored_count = c
                    chosen_move = (x, y)
                    chosen_state = temp_state
        
        else:
            # iterate over all possible moves and find the move that maximizes our value function
            bestval = -1
            for x, y in possible_moves:
                # create a potential state if we were to do this particular move
                temp_board = copy.deepcopy(board)
                temp_board[y][x] = team
                temp_state = (temp_board, turn + 1, None, team)

                # find our valuation and choose the move that maximizes our value function
                val = self.value(temp_state)
                if val > bestval:
                    bestval = val
                    chosen_move = (x, y)
                    chosen_state = temp_state
        if train:
            # when training, we keep track of past state for TD learning later
            self.curr_state_history.append(chosen_state)
            
            # also keep track of explore count and increment it since we chose to move to this new state
            serialization = self.serialize_board(team, chosen_state[0])
            if serialization not in self.state_explore_count:
                self.state_explore_count[serialization] = 1
            else:
                self.state_explore_count[serialization] += 1
            
        return chosen_move
    
    def update_value_func(self, reward):

        # use our reward to update our value func table to allow us to learn
        final_state = self.curr_state_history[-1]
        final_serialization = self.serialize_board(final_state[3], final_state[0])
        self.value_func_table[final_serialization] = reward

        for i in range(len(self.curr_state_history) - 1):

            curr_state = self.curr_state_history[-(i + 1)]
            prev_state = self.curr_state_history[-(i + 2)]
            
            val_t_1 = self.value(curr_state)
            val_t = self.value(prev_state)
            serialization = self.serialize_board(prev_state[3], prev_state[0])
            estimated_val_t = val_t + self.step_size_param * (val_t_1 - val_t)
            self.value_func_table[serialization] = estimated_val_t
