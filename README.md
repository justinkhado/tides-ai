# TidesAI

TidesAI is an implementation of the card game [*Tides of Madness*](https://boardgamegeek.com/boardgame/195544/tides-madness) with modified rules. This library was specifically created to implement an AI player using a Monte Carlo tree search variant for simultaneous games. However, included in the library, there is a random player (makes random moves), greedy player (makes the move with the greatest immediate reward), and query player (input player).

The following modification were made to the ruleset (which can be found in the link above):
- all players' cards are known by all players at any given point in time
- during the *Refresh* phase, random cards are chosen to be kept and chosen to be discarded
- exceeding 9 *Madness* is not considered as a loss condition
- the ability of *Dreamlands* was changed to "For each minority, gain 1 VP"
  - an image displaying all 18 cards can be found in the link above

## Usage

```python
# TidesOfMadness class found in tides_of_madness.py
tom_game = TidesOfMadness() 
# example for query player and monte carlo player
tom_game.play_game(game.query_player, game.monte_carlo_player)
# to hide game information during gameplay, add parameter display=False to play_game()
tom_game.play_game(game.query_player, game.monte_carlo_player, display=False)
```
monte_carlo_player has 2 hyperparameters that can be modified using functools.partial()
- num_simulations: number of simulations for the monte carlo search tree to execute (default=100)
- c: exploration/exploitation parameter (default=sqrt(2))
```python
# monte carlo player with 1000 simulations and exploration/exploitation value of 1
mc_player_n1000c1 = functools.partial(game.monte_carlo_player, num_simulations=1000, c=1)
tom_game.play_game(mc_player_n1000c1, game.random_player)
```

## To-Do
Code Design:
- make GameState class abstract to allow for different implementations
- refactor TidesOfMadness
Implementation:
- reduce number of modifications necessary
- add Decoupled UCT
Code Usability:
- add setup.py file