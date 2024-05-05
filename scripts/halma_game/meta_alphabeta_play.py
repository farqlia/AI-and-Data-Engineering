import logging
from functools import partial
from pathlib import Path

from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import play_match, continue_match
from ai_data_eng.halma_game.search_tree.alpha_beta import AlphaBeta
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.no_gui import NoUI
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from multiprocessing import Process

if __name__ == "__main__":
    depth = 3
    match_params = [
        {'player_white': {'strategy': STRATEGY.STATIC_WEIGHTS, 'search_depth': depth,
                            'algorithm': partial(MetaSearch, alg_init=AlphaBeta)},
         'player_black': {'strategy': STRATEGY.ADAPTIVE_WEIGHTS, 'search_depth': depth,
                            'algorithm': partial(MetaSearch, alg_init=AlphaBeta)}},
        {'player_white': {'strategy': STRATEGY.STATIC_WEIGHTS, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=AlphaBeta)},
         'player_black': {'strategy': STRATEGY.DISTANCE, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=AlphaBeta)}},
        {'player_white': {'strategy': STRATEGY.DISTANCE, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=AlphaBeta)},
         'player_black': {'strategy': STRATEGY.ADAPTIVE_WEIGHTS, 'search_depth': depth,
                          'algorithm': partial(MetaSearch, alg_init=AlphaBeta)}}
    ]
    processes = [Process(target=play_match, args=(params['player_black'], params['player_white'], NoUI))
                  for params in match_params]
    # dir_path = Path('../../data/halma/m-alphabeta-m-alphabeta/2-2')
    # processes = [Process(target=continue_match, args=(params['player_black'], params['player_white'],
      #                                                 dir_path, '05-1503', 35, NoUI))
        #          for params in match_params][:1]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
