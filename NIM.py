from TwoPlayerBoard import Player
from random import randrange

class NIMGame:
    def __init__(self, N, K, p1, p2, P):
        self.num_stones = N
        self.remove_limit = K
        self.p1 = p1
        self.p2 = p2
        self.playing = self.p1 if P == 1 else self.p2

    def remove_stones(self, state, take):
        state -= take
        return state

    def generate_possible_actions(self, state):
        """ Finds all possible actions. The actions represent the states they lead to. """
        child_actions = []
        for removed in range(1, self.remove_limit + 1):
            if state - removed < 0:
                return child_actions
            child_actions.append(removed)
        return child_actions

    def is_terminal_state(self, state):
        return self.generate_possible_actions(state) == []

    def set_playing(self):
        self.playing = self.p2 if self.playing == self.p1 else self.p1


if __name__ == "__main__":
    N = 10
    K = 3
    P = 1

    p1 = Player("1")
    p2 = Player("2")

    board = NIMGame(N, K, p1, p2, P)

    print("Start Pile: {} stones".format(board.num_stones))

    game = True

    while game:
        actions = board.generate_possible_states()
        if len(actions) != 0:
            removed = board.remove_stones(actions[randrange(len(actions))])
            print("Player {} selects {} stones: Remaining stones = {}".format(board.playing.name, removed, board.num_stones))  
        
        if board.is_terminal_state():
            game = False
            print("Player {} wins!".format(board.playing.name))
        else:
            board.set_playing() # Change player
    
        



