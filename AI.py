from math import *

class Learner:
    def __init__(self, board):
        self.board = board

    def MCTS(self, episodes):
        state = board.get_initital_state()
        root = Node()

        for i in range(episodes):
            leaf = self.traverse(root)
            simulation_result = rollout(leaf)
            backpropogate(leaf, simulation_result)

        return best_child(root)

    def traverse(self, node):
        if is_fully_expanded(node):
            node = best_uct(node)
        
        return pick_unvisited(node.children) or node

    def is_fully_expanded(self, node):
        for child in node.children:
            if child.visit == 0:
                return False
        return True

    def best_uct(self, node):
        max = float('-inf')
        for child in node.children:
            utc = child.UCT
            if utc > max:
                max = utc
                winner = child
        return winner 

    def pick_unvisited(self, children):
        pass


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.black_wins = 0
        self.visits = 0
        self.parent = parent
        self.children = []
        self.explored = False
    
    def visit(self):
        self.visits += 1

    def add_child(self, child_node)
        self.children.append(child_node)

    def UCT(self, parent, player, c):
        q = self.black_wins if player == 'black' else (1-self.black_wins)
        return q / self.visits + c * sqrt(log(parent.visits) / self.visits)