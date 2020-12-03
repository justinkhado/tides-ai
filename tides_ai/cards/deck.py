from .card import Card

########################################################################################################
## Cards ##
###########

nya = Card(id='NYA', name='Nyarlathotep', suit='Outer Gods', madness=False)
yog = Card(id='YOG', name='Yog Sothoth', suit='Outer Gods', madness=True)
aza = Card(id='AZA', name='Azathoth', suit='Outer Gods', madness=False)

rly = Card(id='RLY', name='Rlyeh', suit='Locations', madness=True)
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

mis = Card(id='MIS', name='Miskatonic University', suit='None', madness=True)
dre = Card(id='DRE', name='Dreamlands', suit='None', madness=False)
shu = Card(id='SHU', name='Shub Niggurath', suit='None', madness=False)

########################################################################################################

DECK = (nya, yog, aza, rly, inn, mou, una, pna, nec, dag, cth, has, dee, eld, gre, mis, dre, shu)
