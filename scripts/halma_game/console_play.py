from ai_data_eng.halma_game.engine import *
from ai_data_eng.halma_game.game import *
from ai_data_eng.halma_game.gameui import *
from ai_data_eng.halma_game.globals import *
from ai_data_eng.halma_game.player import *

if __name__ == "__main__":
    engine = Engine()
    game_ui = GameUI(engine)

    print("Game starts")
    game_ui.print_board()
    print(f"Current player {engine.moving_player}")
    result = game_ui.move((1, 4), (2, 4))
    print(result)
    game_ui.print_board()
