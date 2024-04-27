from ai_data_eng.halma_game.matches import replay_match
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from pathlib import Path

if __name__ == "__main__":
    replay_match(Path('../../data/halma/m-minmax-m-minmax/2-2/STRATEGY.STATIC_WEIGHTS-STRATEGY.STATIC_WEIGHTS'), HalmaGUI)