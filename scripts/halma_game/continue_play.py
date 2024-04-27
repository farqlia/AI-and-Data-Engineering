from functools import partial
from pathlib import Path

from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import continue_match
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI

if __name__ == "__main__":
    player_white = {'strategy': STRATEGY.STATIC_WEIGHTS, 'search_depth': 2}
    # player_white['algorithm'] = MinMax
    player_white['algorithm'] = partial(MetaSearch, alg_init=MinMax)
    player_black = {'strategy': STRATEGY.STATIC_WEIGHTS, 'search_depth': 2}
    # player_black['algorithm'] = MinMax
    player_black['algorithm'] = partial(MetaSearch, alg_init=MinMax)
    match_dir = Path('../../data/halma/human_minmax_minmax-26-2105-distance-distance')
    continue_match(match_dir, 200, player_white, player_black, HalmaGUI)