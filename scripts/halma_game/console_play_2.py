from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import play_human_minmax_match, play_minmax_minmax_match
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.search_tree.meta_search import MetaSearch
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from ai_data_eng.halma_game.ui.console_ui import ConsoleUI
from functools import partial

if __name__ == "__main__":
    player_white = {'strategy': STRATEGY.DISTANCE, 'search_depth': 2}
    # player_white['algorithm'] = MinMax
    player_white['algorithm'] = partial(MetaSearch, alg_init=MinMax)
    player_black = {'strategy': STRATEGY.DISTANCE, 'search_depth': 2}
    # player_black['algorithm'] = MinMax
    player_black['algorithm'] = partial(MetaSearch, alg_init=MinMax)
    play_minmax_minmax_match(player_white, player_black, ConsoleUI)
