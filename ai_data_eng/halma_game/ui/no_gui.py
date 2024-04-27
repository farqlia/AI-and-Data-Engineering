import logging

from ai_data_eng.halma_game.ui.game_adapter import GameUiAdapter


class NoUI:

    def __init__(self, game_adapter: GameUiAdapter):
        self.game_adapter = game_adapter

    def run(self):
        self.forward()

    def forward(self):
        move = self.game_adapter.next()
        logging.info(f"Recent move of {self.game_adapter.current_player.flag} is {move[0]} -> {move[1]}")
        self.winner = self.game_adapter.is_finished()
        if self.winner is not None:
            logging.info(f"Winner is {self.winner}")
            return
        self.forward()