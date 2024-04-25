import datetime
import os
from pathlib import Path

import tkinter as tk

from ai_data_eng.halma_game.globals import STRATEGY, PLAYER, HALMA_DIR
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.players.console_player import ConsolePlayer
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.game_adapter import GameUiAdapter
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI

strategy_player = {
    STRATEGY.STATIC_WEIGHTED: StaticWeightsPlayer,
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


def play_minmax_minmax_match(strategy_black: STRATEGY, strategy_white: STRATEGY, depth: int,
                             guiInit):
    engine = Engine()
    game_repr = GameState(engine)
    match_dir = HALMA_DIR / f'human_minmax_minmax-{datetime.datetime.today().strftime("%d-%H%M")}'
    os.makedirs(match_dir)
    player_black = strategy_player[strategy_black](PLAYER.BLACK, MinMax(depth))
    player_white = strategy_player[strategy_white](PLAYER.WHITE, MinMax(depth))
    game_adapter = GameUiAdapter(game_repr, player_black, player_white,
                                 match_dir)
    game_adapter.setup()
    gui = guiInit(game_adapter)
    gui.run()