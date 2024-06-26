from abc import ABC, abstractmethod
from typing import Union

from ai_data_eng.halma_game.globals import PLAYER, Field, Move, CAMP, STRATEGY
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm


class Player(ABC):
    '''Player will be passed heuristic and other algorithms
    maybe make this abstract class?'''

    def __init__(self, plr: PLAYER,
                 search_alg: SearchAlgorithm,
                 strategy: STRATEGY) -> None:
        self.flag: PLAYER = plr
        self.strategy = strategy
        self.search_alg = search_alg
        self.camp: CAMP = CAMP.WHITE if self.flag == PLAYER.WHITE else CAMP.BLACK
        self.opponent_camp: CAMP = CAMP.BLACK if self.flag == PLAYER.WHITE else CAMP.WHITE
        self.comp = self.formula()
        self.opp_comp = self.opponent_formula()

    @abstractmethod
    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        pass

    def get_weights(self):
        return None

    def update_by_move(self, game_repr: GameRepresentation):
        self.search_alg.update_by_move(game_repr)

    def repr(self) -> PLAYER:
        return self.flag

    def opponent(self) -> PLAYER:
        return PLAYER.WHITE if self.flag == PLAYER.BLACK else PLAYER.BLACK

    def depth_value(self, point: Field):
        return (self.comp(point[0]) + self.comp(point[1])) / 300

    def opp_depth_value(self, point: Field):
        return (self.opp_comp(point[0]) + self.opp_comp(point[1])) / 300

    def formula(self):
        return lambda x: 15 - x if self.flag == PLAYER.BLACK else x

    def opponent_formula(self):
        return lambda x: x if self.flag == PLAYER.BLACK else 15 - x

    def make_move(self, game_repr: GameRepresentation) -> Union[Move, None]:
        best_move, value = self.search_alg.search(game_repr, self)
        return best_move, value

    def search_tree_size(self) -> int:
        return self.search_alg.get_searched_tree_size()
