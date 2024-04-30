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


def read_game_state_from_file(dir_path: Path, date_prefix: str, steps: int) -> GameRepresentation:
    files = os.listdir(dir_path)
    player_black = pd.read_csv(dir_path / [f for f in files if f.endswith(f'{date_prefix}-PLAYER.BLACK')][0],
                                       header=None, sep=';')
    player_white = pd.read_csv(dir_path / [f for f in files if f.endswith(f'{date_prefix}-PLAYER.WHITE')][0],
                                       header=None, sep=';')
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


def save_match_info(match_dir, player_black: Player, player_white: Player):
    with open(match_dir / 'info', mode='w') as f:
        f.write("player_flag;alg;depth;strategy")
        for player in [player_black, player_white]:
            f.write(f"{player.flag};{player.search_alg.name};{player.search_alg.search_depth};{player}")


def replay_match(dir_path: Path, date_prefix:str, steps: int, guiInit):
    game_repr = read_game_state_from_file(dir_path, date_prefix, steps)
    game_adapter = GameFromFileAdapter(game_repr, dir_path, date_prefix)
    gui = guiInit(game_adapter)
    gui.run()
