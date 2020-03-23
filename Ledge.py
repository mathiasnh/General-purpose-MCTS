class LedgeGame:
    def __init__(self, B, p1, p2, P):
        self.state = B
        self.p1 = p1
        self.p2 = p2
        self.playing = self.p1 if P == 1 else self.p2

    def move_coin(self, state, action):
        s = action['source']
        t = action['target']
        coin = action['coin']
        
        state[s] = 0
        if s != t:
            state[t] = coin

        return state, s, t, coin

    def generate_possible_actions(self, state):
        child_actions = []
        k = 0
        for i, cell in enumerate(state):
            if cell != 0:
                if i == 0:
                    child_actions.append({'source': i, 'target': i, 'coin': cell})
                else:
                    for j in range(i - 1, i - k - 1, -1):
                        child_actions.append({'source': i, 'target': j, 'coin': cell})
                    k = 0
            else:
                k += 1

        return child_actions
    
    def is_terminal_state(self, state):
        return 2 not in state
