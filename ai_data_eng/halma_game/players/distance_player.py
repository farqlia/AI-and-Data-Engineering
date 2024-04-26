import sys
from typing import Union

from ai_data_eng.halma_game.globals import PLAYER, CAMP
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm
from ai_data_eng.halma_game.utils import get_camp_boundaries


class DistancePlayer(Player):

    def __init__(self, plr: PLAYER, search_alg: SearchAlgorithm):
        super().__init__(plr, search_alg)
        self.opponent_camp: CAMP = CAMP.BLACK if self.flag == PLAYER.WHITE else CAMP.WHITE
        self.opponent_boundaries = get_camp_boundaries(self.opponent_camp)

    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        value = 0
        for point in game_repr.get_occupied_fields(self.flag):
            value += self.find_min_distance(point, game_repr)
        return value

    def find_min_distance(self, point, game_repr: GameRepresentation):
        min_distance = sys.maxsize
        if game_repr.in_camp(*point) == self.opponent_camp:
            return 0
        for boundary in self.opponent_boundaries:
            min_distance = min(abs(point[0] - boundary[0]) + abs(point[1] - boundary[1]), min_distance)
        return min_distance

