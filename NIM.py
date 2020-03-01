from TwoPlayerBoard import Player
from random import randrange

class NIMBoard:
    def __init__(self, N, K, player1, player2, P):
        self.num_stones = N
        self.remove_limit = K
        self.player1 = player1
        self.player2 = player2
        self.playing = self.player1 if P == 1 else self.player2

    def remove_stones(self, num):
        self.num_stones -= num
        return num

    def generate_possible_states(self):
        """ Finds all possible actions. The actions represent the states they lead to. """
        child_states = []
        for removed in range(1, self.remove_limit + 1):
            if self.num_stones - removed < 0:
                return child_states
            child_states.append(removed)
        return child_states

    def is_terminal_state(self):
        return self.generate_possible_states() == []

    def set_playing(self):
        self.playing = self.player2 if self.playing == self.player1 else self.player1


if __name__ == "__main__":
    N = 10
    K = 3
    P = 1

    player1 = Player("1")
    player2 = Player("2")

    board = NIMBoard(N, K, player1, player2, P)

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
    
        



