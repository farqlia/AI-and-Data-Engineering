from typing import Union

from ai_data_eng.halma_game.globals import Move, PLAYER
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm


class StaticWeightsPlayer(Player):

    def __init__(self, plr: PLAYER, search_alg: SearchAlgorithm):
        super().__init__(plr, search_alg)
        self.weights = [[0.0 for _ in range(16)] for _ in range(16)]
        self.set_weights()

    def set_weights(self):
        unit_val = 1 / 16
        weight = -1
        for i in range(16):
            weight += unit_val
            for j in range(i + 1):
                self.weights[j][i - j] = weight
        weight = 1
        for i in range(15, 0, -1):
            weight -= unit_val
            for j in range(15, i - 1, -1):
                self.weights[j][15 - j + i] = weight

    def get_weights(self):
        return self.weights

    def sum_weights(self, game_repr: GameRepresentation):
        value = 0
        for point in game_repr.get_occupied_fields(self.flag):
            value += (-1 if self.flag == PLAYER.WHITE else 1) * self.weights[point[0]][point[1]]
            camp = game_repr.in_camp(*point)
            if camp == self.opponent_camp:
                value += self.opp_depth_value(point)
            elif camp == self.camp:
                value -= self.depth_value(point)
        return value

    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        return self.sum_weights(game_repr)
