from card import *
from collections import namedtuple
import random

########################################################################################################
## Cards ##
###########

nya = Card(id='NYA', name='Nyarlathotep', suit='Outer Gods', madness=False)
yog = Card(id='YOG', name='Yog Sothoth', suit='Outer Gods', madness=True)
aza = Card(id='AZA', name='Azathoth', suit='Outer Gods', madness=False)

rly = Card(id='RLY', name='R\'lyeh', suit='Locations', madness=True)
inn = Card(id='INN', name='Innsmouth', suit='Locations', madness=False)
mou = Card(id='MOU', name='Mountains of Madness', suit='Locations', madness=False)

una = Card(id='UNA', name='Unaussprechlichen Kulten', suit='Manuscripts', madness=False)
pna = Card(id='PNA', name='Pnakotic Manuscripts', suit='Manuscripts', madness=True)
nec = Card(id='NEC', name='Necronomicon', suit='Manuscripts', madness=True)

dag = Card(id='DAG', name='Dagon', suit='Great Old Ones', madness=True)
cth = Card(id='CTH', name='Cthulhu', suit='Great Old Ones', madness=False)
has = Card(id='HAS', name='Hastur', suit='Great Old Ones', madness=False)

dee = Card(id='DEE', name='Deep Ones', suit='Races', madness=True)
eld = Card(id='ELD', name='Elder Things', suit='Races', madness=False)
gre = Card(id='GRE', name='Great Race of Yith', suit='Races', madness=True)

mis = Card(id='MIS', name='Miskatonic University', suit=None, madness=True)
dre = Card(id='DRE', name='Dreamlands', suit=None, madness=False)
shu = Card(id='SHU', name='Shub Niggurath', suit=None, madness=False)

deck = (nya, yog, aza, rly, inn, mou, una, pna, nec, dag, cth, has, dee, eld, gre, mis, dre, shu)

########################################################################################################

BoardState = namedtuple('BoardState', 'player_cards, opponent_cards, player_madness, opponent_madness')
GameState = namedtuple('GameState', 'utility, board, moves')

class TidesOfMadness:
    def __init__(self):
        self.deck = list(deck)
        #random.shuffle(self.deck)

        player_hand = []
        opponent_hand = []
        for i in range(len(self.deck)):
            if i % 2 == 0 and len(player_hand) < 5:
                player_hand.append(deck[i])
            elif i % 2 != 0 and len(opponent_hand) < 5:
                opponent_hand.append(deck[i])

        self.initial = GameState(utility=0,
                                 board=BoardState(player_cards=[],
                                                  opponent_cards=[],
                                                  player_madness=0,
                                                  opponent_madness=0),
                                 moves={'player_hand': player_hand, 'opponent_hand': opponent_hand})

    def actions(self, state):
        return state.moves['player_hand']

    def result(self, state, player_move, opponent_move):
        if player_move not in state.moves['player_hand'] or opponent_move not in state.moves['opponent_hand']:
            return state

        player_cards = list(state.board.player_cards)
        player_cards.append(player_move)
        opponent_cards = list(state.board.opponent_cards)
        opponent_cards.append(opponent_move)
        board = BoardState(player_cards=player_cards,
                           opponent_cards=opponent_cards,
                           player_madness=self.calc_madness(player_cards),
                           opponent_madness=self.calc_madness(opponent_cards))

        player_hand = list(state.moves['player_hand'])
        player_hand.remove(player_move)
        opponent_hand = list(state.moves['opponent_hand'])
        opponent_hand.remove(opponent_move)

        return GameState(utility=self.utility(state),
                         board=board,
                         moves={'player_hand': player_hand, 'opponent_hand': opponent_hand})

    def utility(self, state):
        player_score = 0
        opponent_score = 0

        for player_card, opponent_card in zip(state.board.player_cards, state.board.opponent_cards):
            player_score += player_card.ability(state.board)
            opponent_score += opponent_card

        if player_score - opponent_score > 0:
            return 1
        elif player_score - opponent_score < 0:
            return -1
        else:
            return 0

    def terminal_test(self, state):
        return len(state.moves['player_hand']) == 0

    def display(self, state):
        print('Player: ')
        print('Hand: ', end='')
        self.display_cards(state.moves['player_hand'])
        print('Played: ', end='')
        self.display_cards(state.board.player_cards)
        print('Madness:', self.calc_madness(state.board.player_cards))

        print()

        print('Opponent: ')
        print('Hand: ', end='')
        self.display_cards(state.moves['opponent_hand'])
        print('Played: ', end='')
        self.display_cards(state.board.opponent_cards)
        print('Madness:', self.calc_madness(state.board.opponent_cards))

    def play_game(self, player, opponent):
        state = self.initial

        while True:
            return 0 

    @staticmethod
    def display_cards(cards):
        print('| ', end='')
        for card in cards:
            print(card.name, '| ', end='')
        print()

    @staticmethod
    def calc_madness(player_cards):
        count = 0

        for card in player_cards:
            if card.madness:
                count += 1
        
        return count

if __name__ == '__main__':
    game = TidesOfMadness()

    player_cards = [nya, rly, una, cth, aza, shu, mou]
    opponent_cards = [yog, inn, pna, cth, eld, dre, shu]

    board_state = BoardState(player_cards=player_cards, 
                             opponent_cards=opponent_cards, 
                             player_madness=game.calc_madness(player_cards),
                             opponent_madness=game.calc_madness(opponent_cards))

    game.display(game.result(game.initial, nya, yog))

