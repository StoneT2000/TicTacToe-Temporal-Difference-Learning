from tictactoe import O, STEP_RESULT, TicTacToe, X
from agents.random import Agent as RandomAgent
from agents.temporaldifference import Agent as TDAgent


game_settings = {
    "win_length": 3,
    "size": 3,
}

a1 = RandomAgent(**game_settings)
a2 = TDAgent(**game_settings, include_end_game_bias=True, step_size_param=0.7, explore_ratio=0.5)
# a2 = RandomAgent(**game_settings)


def run_agents(agent1, agent2, episodes=100, verbose=False, train=True):
    agent1wins = 0
    agent2wins = 0
    draws = 0
    for episode in range(episodes):
        game = TicTacToe(**game_settings)
        res = STEP_RESULT.NONE

        agent1_team = X
        agent2_team = O
        if episode % 2 == 1:
            agent1_team = X
            agent2_team = O

        
        
        for i in range(game_settings["size"] ** 2):
            team_this_turn = i % 2
            state = game.state(team_this_turn)
            action = None
            if (i % 2 == agent1_team):
                action = agent1.step(state, train)
            else:
                action = agent2.step(state, train)
            
            _,_, res, _ = game.apply(action)
            if (res == STEP_RESULT.DRAW):
                draws += 1
                break
            elif res == STEP_RESULT.X_WIN:
                if agent1_team == X:
                    agent1wins += 1
                else:
                    agent2wins += 1
                break
            elif res == STEP_RESULT.O_WIN:
                if agent1_team == O:
                    agent1wins += 1
                else:
                    agent2wins += 1
                break
        
        state = game.state(agent1_team)
        agent1.step(state, train)
        state = game.state(agent2_team)
        agent2.step(state, train)
        if verbose:
            print("episode {} - Score: Agent 1 {} - Agent 2 {} - Draws {} - Agent2 Pts - {}".format(episode + 1, agent1wins, agent2wins, draws, agent2wins - agent1wins - draws))

print("Training agent...")
run_agents(a1, a2, episodes=1000, train=True)
print("Testing agent")
run_agents(a1, a2, episodes=1000, verbose=True, train=False)
# print(a2.state_explore_count)
# print(a2.value_func_table)
# print("First move : ",a2.value_func_table["0----O----"])
# print("First move : ",a2.value_func_table["0O--------"])
# print("First move : ",a2.value_func_table["0-O-------"])
# print("First move : ",a2.value_func_table["0--O------"])

for i in range(9):
    serial = ["0","-","-","-","-","-","-","-","-","-"]
    serial[i + 1] = "O"
    serial = "".join(serial)
    print("First move: " + serial, a2.value_func_table[serial])
# print(a2.value_func_table)