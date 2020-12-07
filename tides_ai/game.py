from .montecarlo.game_state import GameState, Board
from .montecarlo.mcts import MCTS
from .montecarlo.mcts_node import UCB1Node
from .cards import deck
import random
import math

class TidesOfMadness:
    def __init__(self):
        self.reset_game()

    def display(self, state):
        print('--PLAYER--')
        print('Hand: ', end='')
        self.display_cards(state.board.player_hand)
        print('Played: ', end='')
        self.display_cards(state.board.player_cards)
        #print('Madness:', state.calc_madness(state.board.player_cards))

        print('--OPPONENT--')
        print('Hand: ', end='')
        self.display_cards(state.board.opponent_hand)
        print('Played: ', end='')
        self.display_cards(state.board.opponent_cards)
        #print('Madness:', state.calc_madness(state.board.opponent_cards))

    def play_game(self, player, opponent, display=True):
        def game_loop(state):
            if display:
                self.display(state)
            while True:
                player_move = player(state, player=True)
                opponent_move = opponent(state, player=False)
                try:
                    state = state.result((player_move, opponent_move))
                except ValueError as e:
                    print(e)
                    continue
                if display:
                    print()
                    self.display(state)
                if state.terminal_test():
                    if display:
                        print('\n--Round Ended--')
                        print('Player')
                        print('Score:', state.calc_score(state.board, player=True))#, 'Madness:', state.calc_madness(state.board.player_cards))
                        print('Opponent')
                        print('Score:', state.calc_score(state.board, player=False))#, 'Madness:', state.calc_madness(state.board.opponent_cards))
                    return state

        # Round 1
        if display:
            print('###### ROUND 1 ######')
        game_state = self.initial
        game_state = game_loop(game_state)
        player_score = game_state.calc_score(game_state.board, player=True)
        opponent_score = game_state.calc_score(game_state.board, player=False)
        # Refresh
        next_state = self._refresh(game_state, 1)
        # Round 2
        if display:
            print('\n###### ROUND 2 ######')
        game_state = game_loop(next_state)
        player_score += game_state.calc_score(game_state.board, player=True)
        opponent_score += game_state.calc_score(game_state.board, player=False)
        # Refresh
        next_state = self._refresh(game_state, 2)
        # Round 3
        if display:
            print('\n###### ROUND 3 ######')
        game_state = game_loop(next_state)
        player_score += game_state.calc_score(game_state.board, player=True)
        opponent_score += game_state.calc_score(game_state.board, player=False)

        # Game end
        # clamp difference in scores to [-1, 1]
        utility = max(-1, min(player_score - opponent_score, 1))
        if display:
            print('\n###### Final Score ######')
            if utility > 0:
                print('Player won')
            elif utility < 0:
                print('Opponent won')
            else:
                print('Tie')
            print()
            print('Player')
            print('Score:', player_score)
            print('Opponent')
            print('Score:', opponent_score)

        return utility


    def _refresh(self, state, round):
        '''
        Takes place inbetween rounds. The following occurs:
          - players take played cards back into hand
          - if between round 1 and round 2:
             - both players play 1 card chosen at random
          - if between round 2 and 3
             - both players play 2 cards chosen at random
          - both players discard one card chosen at random
          - both players dealt 2 new cards
        '''
        player_hand = list(state.board.player_cards)
        player_cards = []
        opponent_hand = list(state.board.opponent_cards)
        opponent_cards = []

        random.shuffle(player_hand)
        random.shuffle(opponent_hand)
        for _ in range(round):
            player_cards.append(player_hand.pop())
            opponent_cards.append(opponent_hand.pop())
        
        player_hand.pop()
        opponent_hand.pop()

        for _ in range(2):
            player_hand.append(self.deck.pop())
            opponent_hand.append(self.deck.pop())

        return GameState(Board(player_hand=player_hand, 
                               opponent_hand=opponent_hand,
                               player_cards=player_cards,
                               opponent_cards=opponent_cards))

    def reset_game(self):
        self.deck = list(deck.DECK)
        random.shuffle(self.deck)

        player_hand = []
        opponent_hand = []
        for _ in range(5):
            player_hand.append(self.deck.pop())
            opponent_hand.append(self.deck.pop())

        self.initial = GameState(Board(player_hand=player_hand,
                                       opponent_hand=opponent_hand,
                                       player_cards=[],
                                       opponent_cards=[]))

    def query_player(self, state, player):
        print('\nAvailable moves: ', end='')
        if player:
            self.display_cards(state.board.player_hand)
        else:
            self.display_cards(state.board.opponent_hand)
        move_id = input('Enter card: ')
        move_id = move_id.upper()
        print()

        move = None
        for card in deck.DECK:
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

    def monte_carlo_player(self, state, player, num_simulations=100, c=math.sqrt(2)):
        '''
        if opponent, swap player and opponent cards
        '''
        if player:
            root = UCB1Node(state)
        else:
            root = UCB1Node(GameState(Board(player_hand=state.board.opponent_hand,
                                            opponent_hand=state.board.player_hand,
                                            player_cards=state.board.opponent_cards,
                                            opponent_cards=state.board.player_cards)))
        mcts = MCTS(root, c)
        best_node = mcts.search(num_simulations)
        action = best_node.action

        return action[0]

    @staticmethod
    def display_cards(cards):
        suit_color = {'Outer Gods': 'Y', 'Locations': 'R', 'Manuscripts': 'G', 'Great Old Ones': 'B', 'Races': 'P', 'None': ' '}

        print('| ', end='')
        for card in cards:
            print(f'{card.name} ({suit_color[card.suit]}) | ', end='')
        print()
