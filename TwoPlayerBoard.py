
class BasicBoard:
    def __init__(self, size, player1, player2):
        self.size = size
        self.player1 = player1
        self.player2 = player2


class Player:
    def __init__(self, name):
        self.wins = 0
        self.losses = 0
        self.name = name
        self.playing = False
    
    def set_playing(self, b):
        self.playing = b

    def won(self):
        self.wins += 1
    
    def lost(self):
        self.losses += 1
