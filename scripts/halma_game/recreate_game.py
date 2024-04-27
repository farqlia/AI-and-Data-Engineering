from ai_data_eng.halma_game.matches import replay_match
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from pathlib import Path

if __name__ == "__main__":
    replay_match(Path('../../data/halma/alphabeta-alphabeta/2-2/STRATEGY.ADAPTIVE_WEIGHTS-STRATEGY.ADAPTIVE_WEIGHTS'), HalmaGUI)