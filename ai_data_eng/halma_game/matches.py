import datetime
import logging
import os
from pathlib import Path

import pandas as pd

from ai_data_eng.halma_game.globals import PLAYER, HALMA_DIR
from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.players.adaptive_weights_player import AdaptiveWeightsPlayer
from ai_data_eng.halma_game.players.console_player import ConsolePlayer
from ai_data_eng.halma_game.players.distance_player import DistancePlayer
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.adapters.game_from_file_adapter import GameFromFileAdapter
from ai_data_eng.halma_game.adapters.game_live_adapter import GameLiveUiAdapter
from ai_data_eng.halma_game.utils import split

strategy_player = {
    STRATEGY.STATIC_WEIGHTS: StaticWeightsPlayer,
    STRATEGY.ADAPTIVE_WEIGHTS: AdaptiveWeightsPlayer,
    STRATEGY.DISTANCE: DistancePlayer,
    STRATEGY.NONE: ConsolePlayer
}


def read_game_state_from_file(dir_path: Path, steps: int) -> GameRepresentation:
    player_black = pd.read_csv(dir_path / 'PLAYER.BLACK', header=None, sep=';')
    player_white = pd.read_csv(dir_path / 'PLAYER.WHITE', header=None, sep=';')
    engine = Engine()
    game_repr = GameState(engine)
    for i in range(steps):
        game_repr.move(split(player_black.iloc[i, 0]),
                       split(player_black.iloc[i, 1]))
        game_repr.move(split(player_white.iloc[i, 0]),
                       split(player_white.iloc[i, 1]))

    return game_repr


def play_match(player_black_params, player_white_params, guiInit, match_dir_suffix=''):
    engine = Engine()
    game_repr = GameState(engine)
    player_black = strategy_player[player_black_params['strategy']](PLAYER.BLACK,
                                                                    player_black_params['algorithm'](
                                                                        search_depth=player_black_params[
                                                                            'search_depth']))
    player_white = strategy_player[player_white_params['strategy']](PLAYER.WHITE,
                                                                    player_white_params['algorithm'](
                                                                        search_depth=player_white_params[
                                                                            'search_depth']))
    matches_dir = HALMA_DIR / f'{player_black.search_alg.name}-{player_white.search_alg.name}'
    match_dir = matches_dir / f'{player_black_params["search_depth"]}-{player_white_params["search_depth"]}{match_dir_suffix}'
    os.makedirs(match_dir, exist_ok=True)

    game_adapter = GameLiveUiAdapter(game_repr, player_black, player_white,
                                 match_dir)
    game_adapter.setup()
    gui = guiInit(game_adapter)
    gui.run()


def replay_match(match_dir, guiInit):
    engine = Engine()
    game_repr = GameState(engine)

    game_adapter = GameFromFileAdapter(game_repr, match_dir)
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
    game_adapter = GameLiveUiAdapter(game_repr, player_black, player_white,
                                 dir_path)
    game_adapter.setup()
    gui = guiInit(game_adapter)
    gui.run()
