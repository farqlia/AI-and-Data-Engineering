from ai_data_eng.halma_game.globals import PLAYER
from ai_data_eng.halma_game.logic.halmaengine import HalmaEngine
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.players.console_player import ConsolePlayer
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.utils import print_board, concat_board_state


def test_min_max():
    engine = HalmaEngine()
    game_repr = GameState(engine)
    minmax = MinMax(3)
    player = StaticWeightsPlayer(plr=PLAYER.BLACK, search_alg=minmax)
    best_move = minmax.search(game_repr, player)
    print(f"best move = {best_move}")
    print_board(game_repr.get_board())
    game_repr.move(best_move[0], best_move[1])
    print_board(game_repr.get_board())


def test_meta_search():
    engine = HalmaEngine()
    game_repr = GameState(engine)
    meta_search = MetaSearch(alg_init=MinMax, search_depth=2)
    player = StaticWeightsPlayer(plr=PLAYER.BLACK, search_alg=meta_search)
    best_move = meta_search.search(game_repr, player)
    print(f"best move = {best_move}")
    print_board(game_repr.get_board())
    game_repr.move(best_move[0], best_move[1])
    print_board(game_repr.get_board())
    best_move = meta_search.search(game_repr, player)
    game_repr.move(best_move[0], best_move[1])
    print_board(game_repr.get_board())
