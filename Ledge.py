from TwoPlayerBoard import Player
from random import randrange
from time import sleep

class LedgeBoard:
    def __init__(self, B, player1, player2, P):
        self.state = B
        self.player1 = player1
        self.player2 = player2
        self.playing = self.player1 if P == 1 else self.player2

    def move_coin(self, action):
        s = action['source']
        t = action['target']
        coin = action['coin']

        self.state[s] = 0
        if s != t:
            self.state[t] = coin

        return s, t, coin

    def generate_possible_states(self):
        """ Finds all possible actions. The actions represent the states they lead to. """
        child_states = []
        k = 0
        for i, cell in enumerate(self.state):
            if cell != 0:
                if i == 0:
                    child_states.append({'source': i, 'target': i, 'coin': cell})
                else:
                    for j in range(i - 1, i - k - 1, -1):
                        child_states.append({'source': i, 'target': j, 'coin': cell})
                    k = 0
            else:
                k += 1

        return child_states
    
    def is_terminal_state(self):
        return 2 not in self.state

    def set_playing(self):
        self.playing = self.player2 if self.playing == self.player1 else self.player1

class LedgeCell:
    def __init__(self):
        pass


if __name__ == "__main__":
    B = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
    K = 3
    P = 1

    player1 = Player("1")
    player2 = Player("2")

    board = LedgeBoard(B, player1, player2, P)

    print("Start Board: {}".format(board.state))

    game = True

    while game:
        actions = board.generate_possible_states()
        if len(actions) != 0:
            for a in actions:
                print(a)
            sleep(0.05)
            source, target, coin = board.move_coin(actions[randrange(len(actions))])
            type = "copper" if coin == 1 else "gold"
            if source == target:
                print("Player {} picks up {}:                 {}".format(board.playing.name, type, board.state))
            else:
                print("Player {} moves {} from cell {} to {}:   {}".format(board.playing.name, type, source, target, board.state))  
        
        if board.is_terminal_state():
            game = False
            print("Player {} wins!".format(board.playing.name))
        else:
            board.set_playing() # Change player 
    
        


