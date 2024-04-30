from functools import partial
from pathlib import Path

from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import replay_match
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI

if __name__ == "__main__":
    match_dir = Path('../../data/halma/m-minmax-m-minmax/2-2/STRATEGY.STATIC_WEIGHTS-STRATEGY.STATIC_WEIGHTS')
    replay_match(match_dir, '28-0809',10, HalmaGUI)
