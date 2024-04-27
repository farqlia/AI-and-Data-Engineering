import sys
from typing import Union

from ai_data_eng.halma_game.globals import PLAYER, CAMP, Field
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm
from ai_data_eng.halma_game.utils import get_camp_boundaries


class DistancePlayer(Player):

    def __init__(self, plr: PLAYER, search_alg: SearchAlgorithm):
        super().__init__(plr, search_alg)
        self.opponent_boundaries = get_camp_boundaries(self.opponent_camp)
        self.boundaries = get_camp_boundaries(self.camp)

    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        value = 0
        for point in game_repr.get_occupied_fields(self.flag):
            value += self.find_min_distance(point, game_repr)
        return -value

    def find_min_distance(self, point, game_repr: GameRepresentation):
        opp_distance = sys.maxsize
        in_camp = game_repr.in_camp(*point)
        if in_camp == self.opponent_camp:
            return -self.opp_depth_value(point)
        for boundary in self.opponent_boundaries:
            opp_distance = min(abs(point[0] - boundary[0]) + abs(point[1] - boundary[1]), opp_distance)
        if in_camp == self.camp:
            opp_distance += self.depth_value(point)
        return opp_distance

