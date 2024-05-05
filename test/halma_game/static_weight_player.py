from ai_data_eng.halma_game.globals import PLAYER
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.players.diagonal_road_player import DiagonalRoadPlayer
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.utils import print_board


def test_weight_init_static_player():
    engine = Engine()
    game_repr = GameState(engine)
    player_black = StaticWeightsPlayer(PLAYER.BLACK, MinMax(3))
    print_board(player_black.weights)


def test_weight_init_diagonal_player():
    engine = Engine()
    game_repr = GameState(engine)
    player_black = DiagonalRoadPlayer(PLAYER.BLACK, MinMax(3))
    print_board(player_black.weights)


def test_weight_initialization():
    engine = Engine()
    game_repr = GameState(engine)
    player_black = StaticWeightsPlayer(PLAYER.BLACK, MinMax(3))
    player_white = StaticWeightsPlayer(PLAYER.WHITE, MinMax(3))
    print(player_black.evaluate(game_repr))
    print(player_white.evaluate(game_repr))
    print(game_repr.round_number())
    game_repr.move((4, 1), (4, 2))
    print("\n\n")
    print_board(player_black.weights)
    value_board = [[0.0 for _ in range(16)] for _ in range(16)]
    for point in game_repr.get_occupied_fields(PLAYER.BLACK):
        value_board[point[0]][point[1]] = player_black.evaluate_point(point, game_repr)

    print_board(value_board)
    print(player_black.evaluate(game_repr))
    print(player_white.evaluate(game_repr))
    print(game_repr.round_number())
    game_repr.move((14, 12), (13, 11))
    print(player_black.evaluate(game_repr))
    print(player_white.evaluate(game_repr))
    value_board = [[0.0 for _ in range(16)] for _ in range(16)]
    for point in game_repr.get_occupied_fields(PLAYER.WHITE):
        value_board[point[0]][point[1]] = player_white.evaluate_point(point, game_repr)

    print_board(value_board)
