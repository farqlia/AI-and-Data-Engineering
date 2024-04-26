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
        self.camp: CAMP = CAMP.WHITE if self.flag == PLAYER.WHITE else CAMP.BLACK
        self.opponent_camp: CAMP = CAMP.BLACK if self.flag == PLAYER.WHITE else CAMP.WHITE
        self.opponent_boundaries = get_camp_boundaries(self.opponent_camp)
        self.boundaries = get_camp_boundaries(self.camp)
        self.comp = self.formula()

    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        value = 0
        for point in game_repr.get_occupied_fields(self.flag):
            value += self.find_min_distance(point, game_repr)
        return -value

    def depth_value(self, point: Field):
        return (self.comp(point[0]) + self.comp(point[0])) / 30

    def formula(self):
        return lambda x: 15 - x if self.flag == PLAYER.BLACK else x

    def find_min_distance(self, point, game_repr: GameRepresentation):
        opp_distance = sys.maxsize
        in_camp = game_repr.in_camp(*point)
        if in_camp == self.opponent_camp:
            return 0
        for boundary in self.opponent_boundaries:
            opp_distance = min(abs(point[0] - boundary[0]) + abs(point[1] - boundary[1]), opp_distance)
        if in_camp == self.camp:
            opp_distance += self.depth_value(point)
        return opp_distance

