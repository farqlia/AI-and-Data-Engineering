from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.utils import print_board


def test_weight_initialization():
    player = StaticWeightsPlayer(plr = None,
                 game_repr = None)
    player.set_weights()
    print("\n\n")
    print_board(player.weights)
