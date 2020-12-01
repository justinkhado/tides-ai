from collections import namedtuple
import itertools

Board = namedtuple('Board', 'player_hand, opponent_hand, player_cards, opponent_cards')

class GameState:
    '''
    Defines the game state for Tides of Madness
    '''
    def __init__(self, board):
        self.board = board

    def utility(self):
        '''
        Returns:
            difference in player and opponent scores
        '''
        player_score = self.calc_score(self.board, True)
        opponent_score = self.calc_score(self.board, False)

        return player_score - opponent_score

    def terminal_test(self):
        '''
        Checks if game has ended
        '''
        return len(self.board.player_hand) == 0

    def actions(self):
        '''
        Returns list of joint actions of player and opponent.
        Each joint action is represented as a tuple where index:
            0 = player
            1 = opponent
        '''
        return list(itertools.product(self.board.player_hand, self.board.opponent_hand))

    def result(self, action):
        '''
        Params:
            action: joint action of player and opponent as tuple
        Returns GameState that results from an action.
        '''
        if action not in self.actions():
            raise ValueError('Invalid move.')

        player_hand = list(self.board.opponent_hand)
        player_hand.remove(action[1])
        opponent_hand = list(self.board.player_hand)
        opponent_hand.remove(action[0])

        player_cards = list(self.board.player_cards)
        player_cards.append(action[0])
        opponent_cards = list(self.board.opponent_cards)
        opponent_cards.append(action[1])

        board = Board(player_hand, opponent_hand, player_cards, opponent_cards)

        return GameState(board)

    @staticmethod
    def calc_score(board, player):
        '''
        Returns score of player if 'player' is True; otherwise, returns score
        of opponent.
        '''
        if not player:
            board = Board(player_hand=board.opponent_hand,
                          opponent_hand=board.player_hand,
                          player_cards=board.opponent_cards,
                          opponent_cards=board.player_cards)

        score = 0
        for card in board.player_cards:
            score += card.ability(board)

        return score

    @staticmethod
    def calc_madness(cards):
        count = 0
        for card in cards:
            count += card.madness
        
        return count