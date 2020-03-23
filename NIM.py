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
        child_actions = []
        for removed in range(1, self.remove_limit + 1):
            if state - removed < 0:
                return child_actions
            child_actions.append(removed)
        return child_actions

    def is_terminal_state(self, state):
        return self.generate_possible_actions(state) == []

        



