from abc import ABC, abstractmethod
import math
import random
import game_state

class MCTSNode(ABC):
    '''
    Abstract Monte Carlo Tree Search Node
    '''
    @abstractmethod
    def __init__(self, state, parent=None, action=None):
        '''
        Params:
            state: GameState corresponding to this node
            action: action that parent of this node took to get to this node
            parent: parent of this node
        '''
        self.state = state
        self.parent = parent
        self.action = action

        self.children = []

    @abstractmethod
    def selection(self, c=math.sqrt(2)):
        '''
        Params:
            c: exploration/exploitation constant; c = 0 => exploitation only

        Returns the child with the highest UCT value
        '''
        pass

    @abstractmethod
    def expansion(self):
        '''
        Add child and return it
        '''
        pass

    @abstractmethod 
    def rollout(self):
        '''
        Returns utility of game after selecting random moves until terminal state
        '''
        pass

    @abstractmethod 
    def backpropagation(self, utility):
        '''
        Update number of visits 'n' and number of wins 'w' and do the same
        for parent
        '''
        pass

class UCB1Node(MCTSNode):
    '''
    UCB1 variant of MCTS node
    '''
    def __init__(self, state, parent=None, action=None):
        super().__init__(state, parent, action)
        self.x = 0
        self.n = 0
        self.unexplored_actions = state.actions()

    def selection(self, c=math.sqrt(2)):
        possible_choices = []
        for child in self.children:
            possible_choices.append(self.ucb1(child.x, child.n, self.n, c))

        return self.children[possible_choices.index(max(possible_choices))]
    
    def expansion(self):
        action = self.unexplored_actions.pop()
        next_state = self.state.result(action)
        child = UCB1Node(state=next_state, parent=self, action=action)
        self.children.append(child)
        
        return child

    def rollout(self):
        current_state = self.state
        while not current_state.terminal_test():
            action = random.choice(current_state.actions())
            current_state = current_state.result(action)

        return current_state.utility()
    
    def backpropagation(self, utility):
        self.n += 1
        self.x += utility
        
        if self.parent:
            self.parent.backpropagation(utility)
        
    @staticmethod
    def ucb1(x, n, N, c):
        '''
        Parameters:
            x: cumulative rewards sum for node 
            n: number of simulations for node 
            N: total number of simulations by parent of node 
            c: exploration/exploitation parameter

        Returns the value from the UCB1 formula
        '''
        return (x / n) + c * math.sqrt(math.log(N) / n)

class DUCTNode(MCTSNode):
    '''
    Decoupled UCT Variant of MCTS node
    '''
    def __init__(self, state, parent=None, action=None):
        super().__init__(state, parent, action)
        
        #reward sum and count for each player
        self.x1 = 0
        self.n1 = 0
        self.x2 = 0
        self.n2 = 0

        self.unexplored_actions = state.actions()

        