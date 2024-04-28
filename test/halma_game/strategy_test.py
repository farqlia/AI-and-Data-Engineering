from ai_data_eng.halma_game.globals import PLAYER
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.players.console_player import ConsolePlayer
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.utils import print_board, concat_board_state


def test_min_max():
    engine = Engine()
    game_repr = GameState(engine)
    minmax = MinMax(3)
    player_black = StaticWeightsPlayer(plr=PLAYER.BLACK, search_alg=minmax)
    player_white = StaticWeightsPlayer(plr=PLAYER.WHITE, search_alg=minmax)
    best_move = minmax.search(game_repr, player_black)
    print(f"best move = {best_move}")
    print_board(game_repr.get_board())
    game_repr.move(best_move[0], best_move[1])
    print_board(game_repr.get_board())
    best_move = minmax.search(game_repr, player_white)
    print(f"best move = {best_move}")
    print_board(game_repr.get_board())
    game_repr.move(best_move[0], best_move[1])
    print_board(game_repr.get_board())