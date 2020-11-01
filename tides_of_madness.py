from card import *
from collections import namedtuple

######################################################################################################
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

######################################################################################################

BoardState = namedtuple('BoardState', 'player_cards, opponent_cards, player_madness, opponent_madness')

class TidesOfMadness:
    def __init__(self):
        pass

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
                             opponent_madness=game.calc_madness(opponent_cards)
                             )

    print(shu.ability(board_state))
