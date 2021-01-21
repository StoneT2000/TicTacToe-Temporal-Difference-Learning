# TicTacToe Temporal Difference Learning

Train an agent to play Tic Tac Toe using Temporal Difference Learning

The agent has a few parameters:

```
TDAgent(**game_settings, 
 include_end_game_bias=True, 
 step_size_param=0.7, 
 explore_ratio=0.5)
```

`step_size_param` is the step size parameter for updating the value function table used to make decisions

`explore_ratio` is the probability the agent will instead of choosing the action that maximizes the value function, chooses the action that leads to a state that has been explored the least

`include_end_game_bias` is set to True when we hardcode the true values of end game states (e.g. 3 X's or O's in a row)
