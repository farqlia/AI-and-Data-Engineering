import datetime
import os
from pathlib import Path

import tkinter as tk

from ai_data_eng.halma_game.globals import STRATEGY, PLAYER, HALMA_DIR
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.players.console_player import ConsolePlayer
from ai_data_eng.halma_game.players.distance_player import DistancePlayer
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.game_adapter import GameUiAdapter
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from ai_data_eng.halma_game.utils import read_game_state_from_file

strategy_player = {
    STRATEGY.STATIC_WEIGHTED: StaticWeightsPlayer,
    STRATEGY.DISTANCE: DistancePlayer,
    STRATEGY.NONE: ConsolePlayer
}


def play_human_minmax_match(strategy_white: STRATEGY, depth: int):
    engine = Engine()
    game_repr = GameState(engine)
    match_dir = HALMA_DIR / f'human_minmax_match-{datetime.datetime.today().strftime("%d-%H%M")}'
    os.makedirs(match_dir)
    player_black = ConsolePlayer(PLAYER.BLACK, None)
    player_white = strategy_player[strategy_white](PLAYER.WHITE, MinMax(depth))
    game_adapter = GameUiAdapter(game_repr, player_black, player_white,
                                 match_dir)
    game_adapter.setup()
    root = tk.Tk()
    halma_gui = HalmaGUI(root, game_adapter)
    halma_gui.update_ui()

    root.mainloop()


def play_minmax_minmax_match(player_black_params, player_white_params, guiInit):
    engine = Engine()
    game_repr = GameState(engine)
    match_dir = HALMA_DIR / f'human_minmax_minmax-{datetime.datetime.today().strftime("%d-%H%M")}-{player_black_params["strategy"].value}-{player_white_params["strategy"].value}'
    os.makedirs(match_dir)
    player_black = strategy_player[player_black_params['strategy']](PLAYER.BLACK,
                                                                    player_black_params['algorithm'](search_depth=player_black_params['search_depth']))
    player_white = strategy_player[player_white_params['strategy']](PLAYER.WHITE,
                                                                    player_white_params['algorithm'](search_depth=player_white_params['search_depth']))
    game_adapter = GameUiAdapter(game_repr, player_black, player_white,
                                 match_dir)

    game_adapter.setup()
    gui = guiInit(game_adapter)
    gui.run()


def continue_match(dir_path: Path, steps: int, player_black_params, player_white_params, guiInit):
    game_repr = read_game_state_from_file(dir_path, steps)
    player_black = strategy_player[player_black_params['strategy']](PLAYER.BLACK,
                                                                    player_black_params['algorithm'](
                                                                        search_depth=player_black_params[
                                                                            'search_depth']))
    player_white = strategy_player[player_white_params['strategy']](PLAYER.WHITE,
                                                                    player_white_params['algorithm'](
                                                                        search_depth=player_white_params[
                                                                            'search_depth']))
    player_white.update_by_move(game_repr)
    player_black.update_by_move(game_repr)
    game_adapter = GameUiAdapter(game_repr, player_black, player_white,
                                 dir_path)
    game_adapter.setup()
    gui = guiInit(game_adapter)
    gui.run()