from typing import Union

from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player


class EmptyPlayer(Player):

    def __init__(self):
        super().__init__(None, None, None)

    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        pass

    def search_tree_size(self) -> int:
        return 0