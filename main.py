from math import sqrt
from simWorld import Environment
from TwoPlayerBoard import Player
from tqdm import tqdm
from random import choice

import AI
import LedgeNoState
import NIM


class LedgeEnvironmentNoState(Environment):
    """ Attempt with no state in game file """
    def __init__(self, B, p1, p2, P):
        # Perheps have state here and do moves from the game?
        self.env = LedgeNoState.LedgeGame_(B, p1, p2, P)
        self.initial_state = B
        self.starter = P
        self.p1 = p1
        self.p2 = p2

    def produce_initial_state(self):
        return self.initial_state

    def generate_possible_child_states(self, node):
        child_states = []
        actions = self.env.generate_possible_actions(node.get_state())
        for a in actions:
            state, player, result = self.do_action(node.get_state(), a, node.player_to_move)
            child_states.append({"state": state, "player": player, "result": result})

        return child_states

    def is_terminal_state(self, state):
        return self.env.is_terminal_state(state)

    def do_action(self, state, action, p):
        state, source, target, coin = self.env.move_coin(state, action)
        type = "copper" if coin == 1 else "gold  "
        if source == target:
            result = "Player {} picks up {}:                 {}".format(p.name, type, state)
        else:
            result = "Player {} moves {} from cell {} to {}:   {}".format(p.name, type, source, target, state) 
    
        player = self.p1 if p.name == "2" else self.p2 # Change player
        return state, player, result



class NIMEnvironment(Environment):
    def __init__(self, N, K, p1, p2, P):
        self.env = NIM.NIMGame(N, K, p1, p2, P)
        self.initial_state = N
        self.starter = P
        self.p1 = p1
        self.p2 = p2

    def produce_initial_state(self):
        return self.initial_state

    def generate_possible_child_states(self, node):
        child_states = []
        actions = self.env.generate_possible_actions(node.get_state())
        for a in actions:
            state, player, result = self.do_action(node.get_state(), a, node.player_to_move)
            child_states.append({"state": state, "player": player, "result": result})

        return child_states

    def is_terminal_state(self, state):
        self.env.is_terminal_state(state)

    def do_action(self, state, action, p):
        state = self.env.remove_stones(state, action)
        result = "Player {} selects {} stones: Remaining stones = {}".format(p.name, action, state)
        player = self.p1 if p.name == "2" else self.p2 # Change player
        return state, player, result

def who_starts(p1, p2, P):
    if P == 1:
        return p1
    elif P == 2:
        return p2
    else:
        return choice([p1, p2])

if __name__ == "__main__":
    G = 10
    M = 2000
    P = 1
    verbose = True

    p1 = Player("1")
    p2 = Player("2")

    # LEDGE
    #B = [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 2, 0, 0, 1, 0, 1, 1, 0, 1]
    #B = [1, 1, 1, 1, 0, 2]
    B = [0,0,0,0,0,2,0,1,0]
    c = sqrt(2)

    # NIM
    N = 9
    K = 3

    game = LedgeEnvironmentNoState(B, p1, p2, P)
    #game = NIMEnvironment(N, K, p1, p2, P)

    mc_learner = AI.Learner(game, c)


    # Monte Carlo Tree Search:

    p1_wins = 0

    for i in tqdm(range(G)):
        starter = who_starts(p1, p2, P)
        print("Player {} starts".format(starter.name))
        root = AI.Node(game.produce_initial_state(), starter, None, None)
        if verbose: print("Start board: {}".format(root.get_state()))
        while mc_learner.non_terminal(root):
            root = mc_learner.MCTS(root, M)
            if verbose:
                print(root.action)
            winner = root.parent.player_to_move.name
            root.reset()
        p1_wins += 1 if winner == "1" else 0
    print("Player 1 won {} out of {} games ({}%)".format(p1_wins, G, p1_wins/G*100))    

