from pathlib import Path

from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import continue_match
from ai_data_eng.halma_game.search_tree.alpha_beta import AlphaBeta
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.no_gui import NoUI
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI

if __name__ == "__main__":
    player_white = {'strategy': STRATEGY.DISTANCE, 'search_depth': 1,
                    'algorithm': MinMax}
    player_black = {'strategy': STRATEGY.DISTANCE, 'search_depth': 1,
                    'algorithm': MinMax}
    dir_path = Path('../../data/halma/minmax-minmax/3-3/')
    continue_match(player_white, player_black, dir_path, '28-1002', 15, HalmaGUI)