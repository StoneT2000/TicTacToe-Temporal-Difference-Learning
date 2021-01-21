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


Run `src/run.py` to train and test an agent against a random agent

## Interesting Behaviors

After enough episodes of training, the TD agent learns that in the first move, placing an "O" in the corners are of higher value than other positions. 

Interestingly, since the agent the TD agent trains against is random, the TD agent doesn't realize that placing "O" in anywhere but the corner is generally a losing position. Goes to show that a bad teacher (the random agent) means the student (the TD agent) cannot learn the best strategies
