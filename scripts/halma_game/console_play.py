from functools import partial

from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import play_match
from ai_data_eng.halma_game.search_tree.alpha_beta import AlphaBeta
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.console_ui import ConsoleUI
from ai_data_eng.halma_game.ui.no_gui import NoUI
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI

if __name__ == "__main__":
    depth = 1
    player_white = {'strategy': STRATEGY.ADAPTIVE_WEIGHTS, 'search_depth': depth,
                    'algorithm': MinMax}
    player_black = {'strategy': STRATEGY.DISTANCE, 'search_depth': depth,
                    'algorithm': MinMax}
    play_match(player_white, player_black, HalmaGUI)
