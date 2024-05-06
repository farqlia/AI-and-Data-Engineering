from functools import partial
from pathlib import Path

from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import continue_match
from ai_data_eng.halma_game.search_tree.alpha_beta import AlphaBeta
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.no_gui import NoUI
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI

if __name__ == "__main__":
    player_white = {'strategy': STRATEGY.STATIC_WEIGHTS, 'search_depth': 3,
                    'algorithm': partial(MetaSearch, alg_init=AlphaBeta)}
    player_black = {'strategy': STRATEGY.DISTANCE, 'search_depth': 3,
                    'algorithm': partial(MetaSearch, alg_init=AlphaBeta)}
    dir_path = Path('../../data/halma/m-alphabeta-m-alphabeta/3-3')
    continue_match(player_black, player_white, dir_path, '05-1642', 35, HalmaGUI)