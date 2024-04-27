from pathlib import Path
from typing import Union, List, Tuple

from ai_data_eng.halma_game.globals import PLAYER, Field, Move, HALMA_DIR, CAMP
from abc import ABC, abstractmethod

from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm
from timeit import default_timer as timer

class Player(ABC):

    '''Player will be passed heuristic and other algorithms
    maybe make this abstract class?'''

    def __init__(self, plr: PLAYER,
                 search_alg: SearchAlgorithm) -> None:
        self.flag: PLAYER = plr
        self.search_alg = search_alg
        self.camp: CAMP = CAMP.WHITE if self.flag == PLAYER.WHITE else CAMP.BLACK
        self.opponent_camp: CAMP = CAMP.BLACK if self.flag == PLAYER.WHITE else CAMP.WHITE
        self.comp = self.formula()
        self.opp_comp = self.opponent_formula()

    @abstractmethod
    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        pass

    def update_by_move(self, game_repr: GameRepresentation):
        self.search_alg.update_by_move(game_repr)

    def repr(self) -> PLAYER:
        return self.flag

    def depth_value(self, point: Field):
        return (self.comp(point[0]) + self.comp(point[0])) / 30

    def opp_depth_value(self, point: Field):
        return (self.opp_comp(point[0]) + self.opp_comp(point[0])) / 30

    def formula(self):
        return lambda x: 15 - x if self.flag == PLAYER.BLACK else x

    def opponent_formula(self):
        return lambda x: x if self.flag == PLAYER.BLACK else 15 - x

    def make_move(self, game_repr: GameRepresentation) -> Union[Move, None]:
        best_move = self.search_alg.search(game_repr, self)
        return best_move

    def search_tree_size(self) -> int:
        '''
        Returns the depth of the searched game tree. Should be called only once per round
        '''
        return self.search_alg.get_searched_tree_size()


