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
from ai_data_eng.halma_game.players.player import Player
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

def play_match(player_black_params, player_white_params, guiInit):
    engine = Engine()
    game_repr = GameState(engine)
    player_black = strategy_player[player_black_params['strategy']](PLAYER.BLACK,
                                                                    player_black_params['algorithm'](search_depth=player_black_params['search_depth']))
    player_white = strategy_player[player_white_params['strategy']](PLAYER.WHITE,
                                                                    player_white_params['algorithm'](search_depth=player_white_params['search_depth']))
    match_dir = HALMA_DIR / f'{player_black.search_alg.name}-{player_black_params["search_depth"]}-{player_white.search_alg.name}-{player_white_params["search_depth"]}-{player_black_params["strategy"].value}-{player_white_params["strategy"].value}-{datetime.datetime.today().strftime("%d-%H%M")}'
    os.makedirs(match_dir)
    game_adapter = GameUiAdapter(game_repr, player_black, player_white,
                                 match_dir)

    game_adapter.setup()
    gui = guiInit(game_adapter)
    gui.run()


def save_match_info(match_dir, player_black: Player, player_white: Player):
    with open(match_dir / 'info', mode='w') as f:
        f.write("player_flag;alg;depth;strategy")
        for player in [player_black, player_white]:
            f.write(f"{player.flag};{player.search_alg.name};{player.search_alg.search_depth};{player}")


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