from collections import defaultdict

class MCTS:
    def __init__(self, exploration):
        self.exploration = exploration
        self.default_policy = defaultdict(lambda: 0)
        self.tree = []

    def simulate(self, board, initial_state):
        board.set_position(initial_state)
        states = self.sim_tree(board)
        z = sim_default(board)
        backup(states, z)

    def sim_tree(self, board, exploration):
        """ Tree policy """
        c = exploration
        t = 0 

        game = True

        while game:
            state = board.get_current_state()
            if state not in tree:
                self.new_node(state)
                return None # TODO: return a list of states [s_0 ... s_t]
            
            a = self.select_move(board, s, c)
            board.do_move(a)
        
        return None # TODO: return a list of states [s_0 ... s_t-1]
    
    def sim_default(self, board):
        """ Default policy. To be played during rollouts """

        game = True

        while game:
            pass

    def new_node(self, state):
        #self.tree.append(Node(state, ))
        pass


class Node:
    def __init__(self, state, win, visits, parent):
        self.state = state
        self.win = win
        self.visits = visits 
        self.parent = parent
        self.children = []
    
    def visit(self):
        self.visits += 1

    def add_child(self, child_node)
        self.children.append(child_node)


