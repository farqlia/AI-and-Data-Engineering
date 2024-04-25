from ai_data_eng.halma_game.globals import STRATEGY
from ai_data_eng.halma_game.matches import play_human_minmax_match, play_minmax_minmax_match
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from ai_data_eng.halma_game.ui.console_ui import ConsoleUI

if __name__ == "__main__":
    play_minmax_minmax_match(STRATEGY.STATIC_WEIGHTED, STRATEGY.STATIC_WEIGHTED, 2, ConsoleUI)
