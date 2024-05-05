from ai_data_eng.halma_game.matches import replay_match
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI
from pathlib import Path

if __name__ == "__main__":
    replay_match(Path('../../data/halma/m-alphabeta-m-alphabeta/2-2/STRATEGY.STATIC_WEIGHTS-STRATEGY.ADAPTIVE_WEIGHTS'), '05-1444', 0,
                 HalmaGUI)