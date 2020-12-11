from tides.game import TidesOfMadness
import functools

if __name__ == '__main__':
    game = TidesOfMadness()
    num_games = 1
    stats = {1: 0, -1: 0, 0: 0}

    # players included with TidesOfMadness class:
    #   query_player
    #   random_player
    #   greedy_player
    #   monte_carlo_player

    # monte carlo players with different number of simulations, n, and same exploration parameter (c=sqrt(2))
    mc_player_1 = functools.partial(game.monte_carlo_player, num_simulations=1)
    mc_player_10 = functools.partial(game.monte_carlo_player, num_simulations=10)
    mc_player_100 = functools.partial(game.monte_carlo_player, num_simulations=100)
    mc_player_1000 = functools.partial(game.monte_carlo_player, num_simulations=1000)
    mc_player_5000 = functools.partial(game.monte_carlo_player, num_simulations=5000)
    # monte carlo with same number of simulations (n=100) and different exploration parameters, c
    mc_player_c0 = functools.partial(game.monte_carlo_player, c=0)
    mc_player_c04 = functools.partial(game.monte_carlo_player, c=0.4)
    mc_player_c08 = functools.partial(game.monte_carlo_player, c=0.8)
    mc_player_c12 = functools.partial(game.monte_carlo_player, c=1.2)
    mc_player_c16 = functools.partial(game.monte_carlo_player, c=1.6)
    mc_player_c20 = functools.partial(game.monte_carlo_player, c=2.0)
    
    for i in range(num_games):
        print('Game', i+1)
        game.reset_game()
        stats[game.play_game(game.random_player, game.monte_carlo_player, display=True)] += 1
    print(stats)