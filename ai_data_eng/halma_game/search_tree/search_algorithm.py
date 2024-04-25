from abc import ABC, abstractmethod

from ai_data_eng.halma_game.globals import Move
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation


class SearchAlgorithm(ABC):

    def __init__(self, search_depth):
        self.search_depth = search_depth
        self.tree_size = 0

    @abstractmethod
    def _search(self, game_repr: GameRepresentation, player) -> Move:
        pass

    def get_searched_tree_size(self):
        return self.tree_size

    def search(self, game_repr: GameRepresentation, player) -> Move:
        self.tree_size = 0
        return self._search(game_repr, player)

