import logging

from ai_data_eng.halma_game.ui.game_adapter import GameUiAdapter
from ai_data_eng.halma_game.utils import print_board


class ConsoleUI:

    def __init__(self, game_adapter: GameUiAdapter):
        self.game_adapter = game_adapter

    def forward(self):
        move = self.game_adapter.next()
        logging.info(f"Recent move of {self.game_adapter.current_player} is {move}")
        print_board(self.game_adapter.get_board())
        us = input("Continue? : ")
        if us.lower()[1] != "y":
            return
        self.winner = self.game_adapter.is_finished()
        if self.winner is not None:
            logging.info(f"Winner is {self.winner}")
            return
        self.forward()
