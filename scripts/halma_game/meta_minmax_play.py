import logging
from functools import partial

from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import play_match
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.no_gui import NoUI
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from multiprocessing import Process

if __name__ == "__main__":
    depth = 3
    match_params = [
        {'player_white': {'strategy': STRATEGY.STATIC_WEIGHTS, 'search_depth': depth,
                            'algorithm': partial(MetaSearch, alg_init=MinMax)},
         'player_black': {'strategy': STRATEGY.STATIC_WEIGHTS, 'search_depth': depth,
                            'algorithm': partial(MetaSearch, alg_init=MinMax)}},
        {'player_white': {'strategy': STRATEGY.DISTANCE, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=MinMax)},
         'player_black': {'strategy': STRATEGY.DISTANCE, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=MinMax)}},
        {'player_white': {'strategy': STRATEGY.ADAPTIVE_WEIGHTS, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=MinMax)},
         'player_black': {'strategy': STRATEGY.ADAPTIVE_WEIGHTS, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=MinMax)}}
    ]
    processes = [Process(target=play_match, args=(params['player_black'], params['player_white'], NoUI))
                 for params in match_params]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
