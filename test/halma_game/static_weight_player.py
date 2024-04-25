from ai_data_eng.halma_game.globals import PLAYER
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.utils import print_board


def test_weight_initialization():
    player = StaticWeightsPlayer(PLAYER.BLACK, MinMax(100))
    print("\n\n")
    print_board(player.weights)
