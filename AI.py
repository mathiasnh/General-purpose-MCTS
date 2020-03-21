from math import sqrt, log, log2
from random import randrange, choice, seed
from operator import attrgetter
from ast import literal_eval

class Learner:
    def __init__(self, game, exploration_constant):
        self.game = game
        self.exploration_constant = exploration_constant

    def MCTS(self, root, resources):
        for i in range(resources):
            leaf = self.traverse(root)
            simulation_result = self.rollout(leaf)
            self.backpropogate(leaf, simulation_result)

        return self.best_child(root)

    ### Traversing
    def traverse(self, node):
        while node.is_fully_expanded():
            node = self.best_uct(node)

        if node.children == []:
            self.expand_node(node)
            
        return self.pick_unvisited(node.children) or node  

    def best_uct(self, node):
        for child in node.children:
            child.UCT(node, self.exploration_constant)
        if node.player_to_move.name == "1":
            uct = max(node.children, key=attrgetter("uct"))
        else:
            uct = min(node.children, key=attrgetter("uct"))
        return choice([n for n in node.children if n.uct == uct.uct])
        """
        cmp, u = self.uct_compare(node, node.player_to_move.name == "1", self.exploration_constant)
        return cmp(node.children, key=u)

    def uct_compare(self, node, maximize, c):
        def u_plus(child):
            return child.p1_wins / child.visits + c * sqrt(log2(node.visits) / child.visits)
        
        def u_minus(child):
            return (child.visits - child.p1_wins) / child.visits - c * sqrt(log2(node.visits) / child.visits)

        if maximize:
            return max, u_plus
        else:
            return min, u_minus
        """

    def expand_node(self, node):
        """ Created child nodes for every legal state that can be reached from node """
        for data in self.game.generate_possible_child_states(node):
            node.add_child(Node(data["state"], data["player"], node, data["result"]))

    def pick_unvisited(self, children):
        if children == []:
            return False
        unvisited = [node for node in children if node.visits == 0]
        return choice(unvisited)

    ### Rollout 
    def rollout(self, node):
        while self.non_terminal(node):
            node = self.rollout_policy(node)

        return self.result(node)
    
    def rollout_policy(self, node):
        """ Pick random state and add it as child node """
        possible_states = self.game.generate_possible_child_states(node)
        data = choice(possible_states)
        return Node(data["state"], data["player"], node, data["result"])

    def non_terminal(self, node):
        return not self.game.env.is_terminal_state(node.get_state())

    def result(self, node):
        return 1 if node.parent.player_to_move.name == "1" else 0

    ### Backprop
    def backpropogate(self, node, result):
        node.update_stats(result)
        if node.is_root():
            return
        self.backpropogate(node.parent, result)

    ### End
    def best_child(self, node):
        """ Returns the child with the highest number of visits """
        if node.player_to_move.name == "1":
            cmp = max(node.children, key=attrgetter("q"))
        else:
            cmp = min(node.children, key=attrgetter("q"))
        return choice([n for n in node.children if n.q == cmp.q])



class Node:
    def __init__(self, state, player, parent, action):
        self.state = state
        self.player_to_move = player
        self.parent = parent
        self.p1_wins = 0
        self.visits = 0
        self.q = 0
        self.children = []
        self.uct = 0
        self.action = action


    def is_root(self):
        return self.parent == None

    def get_state(self):
        state_string = str(self.state)
        return literal_eval(state_string)

    def update_stats(self, result):
        self.visits += 1
        if result == 1:
            self.p1_wins += 1
        self.q = self.p1_wins / self.visits

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_fully_expanded(self):
        """ Returns True if all of node's children have been visited """
        for child in self.children:
            if child.visits == 0:
                return False
        return self.children != []
    """
    def UCT(self, parent, c):
        q = self.p1_wins if parent.player_to_move.name == "1" else (self.visits-self.p1_wins)
        self.uct = q / self.visits + c * sqrt(log2(parent.visits) / self.visits)
        #if self.walkthrough:  print("Node {}: UCT = {} / {} + {} * sqrt(log2({}) / {} = {}".format(self.get_state(), q, self.visits, c, parent.visits, self.visits, self.uct))
        return self.uct
    """
    def UCT(self, parent, c):
        if parent.player_to_move.name == "2":
            c = -c
        self.uct = self.q + c * sqrt(log2(parent.visits) / self.visits)
        return self.uct

    def reset(self):
        self.parent = None
        self.p1_wins = 0
        self.visits = 0
        self.uct = 0
        self.children = []