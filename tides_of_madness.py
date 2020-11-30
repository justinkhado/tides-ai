from game_state import GameState, Board
from monte_carlo import MCTS
from mcts_node import UCB1Node
import deck
import random

class TidesOfMadness:
    def __init__(self):
        self.deck = list(deck.deck)
        random.shuffle(self.deck)

        player_hand = []
        opponent_hand = []
        while len(player_hand) < 9:
            player_hand.append(self.deck.pop())
            opponent_hand.append(self.deck.pop())

        board=Board(player_hand=player_hand,
                    opponent_hand=opponent_hand,
                    player_cards=[],
                    opponent_cards=[])

        self.initial = GameState(board)

    def display(self, state):
        print('--PLAYER--')
        print('Hand: ', end='')
        self.display_cards(state.board.player_hand)
        print('Played: ', end='')
        self.display_cards(state.board.player_cards)
        print('Madness:', state.calc_madness(state.board.player_cards))

        print('--OPPONENT--')
        print('Hand: ', end='')
        self.display_cards(state.board.opponent_hand)
        print('Played: ', end='')
        self.display_cards(state.board.opponent_cards)
        print('Madness:', state.calc_madness(state.board.opponent_cards))

    def play_game(self, player, opponent, display=True):
        def game_loop(state):
            if display:
                self.display(state)

            while True:
                if display:
                    print()
                player_move = player(state, True)
                opponent_move = opponent(state, False)
                state = state.result((player_move, opponent_move))
                if display:
                    self.display(state)
                if state.terminal_test():
                    if display:
                        print()
                        print('--Game ended--')
                        
                        if state.utility() > 0:
                            print('Player won')
                        elif state.utility() < 0:
                            print('Opponent won')
                        else:
                            print('Tie')

                        print()
                        print('Player')
                        print('Score:', state.calc_score(state.board, player=True), 'Madness:', state.calc_madness(state.board.player_cards))
                        print('Opponent')
                        print('Score:', state.calc_score(state.board, player=False), 'Madness:', state.calc_madness(state.board.opponent_cards))

                    return state.utility()

        # Round 1
        game_state = self.initial
        return game_loop(game_state)

    def query_player(self, state, player):
        print('Available moves: ', end='')
        if player:
            self.display_cards(state.board.player_hand)
        else:
            self.display_cards(state.board.opponent_hand)
        move_id = input('Enter card: ')
        move_id = move_id.upper()
        print()

        move = None
        for card in self.deck:
            if card.id == move_id:
                move = card
        
        return move

    def random_player(self, state, player):
        '''
        Makes random moves
        '''
        if player:
            move = random.choice(state.board.player_hand)
        else:
            move = random.choice(state.board.opponent_hand)
        
        return move
    
    def greedy_player(self, state, player):
        '''
        Makes the move the gives the most points for the current turn.
        If first turn of round, a random move is chosen.
        Won't make a move that leads to 'Madness' loss condition.
        '''
        if state.board.player_cards == 0:
            return self.random_player(state, player)

        greedy_move = None
        if player:
            greedy_score = -1000
        else:
            greedy_score = 1000

        for player_move in state.board.player_hand:
            for opponent_move in state.board.opponent_hand:
                result = state.result((player_move, opponent_move))
                if player and greedy_score < result.utility():
                    greedy_score = result.utility()
                    greedy_move = player_move
                elif not player and greedy_score > result.utility():
                    greedy_score = result.utility()
                    greedy_move = opponent_move
        
        return greedy_move

    def monte_carlo_player(self, state, player, variant='UCB1'):
        if variant == 'UCB1':
            return self._UCB1(state, player)
        elif variant == 'DUCT':
            return self._DUCT(state, player)

    def _UCB1(self, state, player):
        root = UCB1Node(state)
        mc = MCTS(root)
        best_node = mc.search(num_simulations=1000)
        action = best_node.action

        return action[0] if player else action[1]

    def _DUCT(self, state, player):
        pass

    @staticmethod
    def display_cards(cards):
        suit_color = {'Outer Gods': 'Y', 'Locations': 'R', 'Manuscripts': 'G', 'Great Old Ones': 'B', 'Races': 'P', 'None': ' '}

        print('| ', end='')
        for card in cards:
            print(f'{card.name} ({suit_color[card.suit]}) | ', end='')
        print()

if __name__ == '__main__':
    game = TidesOfMadness()
    stats = {1: 0, -1: 0, 0: 0}

    for i in range(100):
        print('Game', i+1)
        stats[game.play_game(game.monte_carlo_player, game.random_player, display=False)] += 1

    print(stats)