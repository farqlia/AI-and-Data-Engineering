from typing import Union, List

from ai_data_eng.halma_game.globals import PLAYER, Field, Move
from abc import ABC, abstractmethod

from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm


class Player(ABC):

    '''Player will be passed heuristic and other algorithms
    maybe make this abstract class?'''

    def __init__(self, plr: PLAYER, search_alg: SearchAlgorithm) -> None:
        self.flag: PLAYER = plr
        self.search_alg = search_alg

    @abstractmethod
    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        pass

    def repr(self) -> PLAYER:
        return self.flag

    def get_occupied_fields(self, game_repr: GameRepresentation) -> List[Field]:
        fields = []
        state_board = game_repr.get_board()
        for i in range(16):
            for j in range(16):
                if state_board[i][j].value == self.flag.value:
                    fields.append((i, j))
        return fields

    def make_move(self, game_repr: GameRepresentation) -> Union[Move, None]:
        best_move = self.search_alg.search(game_repr, self)
        return best_move

    def game_search_depth(self) -> int:
        '''
        Returns the depth of the searched game tree. Should be called only once per round
        '''
        return self.search_alg.get_searched_tree_size()


