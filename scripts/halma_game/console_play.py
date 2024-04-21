import tkinter as tk
from ai_data_eng.halma_game.game import *
from ai_data_eng.halma_game.globals import *

from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.players.console_player import ConsolePlayer
from ai_data_eng.halma_game.players.static_weights_player import StaticWeightsPlayer
from ai_data_eng.halma_game.search_tree.min_max import MinMax
from ai_data_eng.halma_game.ui.game_adapter import GameUiAdapter
from ai_data_eng.halma_game.ui.tkinter_ui import HalmaGUI


def main():
    root = tk.Tk()
    engine = Engine()
    game_repr = GameState(engine)
    player1 = ConsolePlayer(PLAYER.BLACK, search_alg=None)
    player2 = StaticWeightsPlayer(plr=PLAYER.WHITE, search_alg=MinMax(200))
    game_adapter = GameUiAdapter(game_repr, player1, player2)
    game_adapter.setup()
    halma_gui = HalmaGUI(root, game_adapter)
    halma_gui.update_ui()

    root.mainloop()


if __name__ == "__main__":
    main()
