from ai_data_eng.halma_game.globals import STATE
from ai_data_eng.halma_game.engine import Engine


class Game:

    def __init__(self, engine, player_1, player_2):

        self._engine = engine
        self._player_1 = player_1
        self._player_2 = player_2

