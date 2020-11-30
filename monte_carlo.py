class MCTS:
    '''
    Monte Carlo Tree Search
    '''
    def __init__(self, root):
        '''
        Params:
            root: node to start Monte Carlo Tree Search on
        '''
        self.root = root

    def search(self, num_simulations):
        '''
        Returns best node from running MCTS algorithm
        '''
        for _ in range(num_simulations):
            node = self._rollout_node()
            utility = node.rollout()
            node.backpropagation(utility)
        
        return self.root.selection(c=0)

    def _rollout_node(self):
        '''
        Returns which node to rollout
        '''
        current_node = self.root
        while not current_node.state.terminal_test():
            if len(current_node.unexplored_actions) != 0:
                return current_node.expansion()
            else:
                current_node = current_node.selection()
        
        return current_node
            

    