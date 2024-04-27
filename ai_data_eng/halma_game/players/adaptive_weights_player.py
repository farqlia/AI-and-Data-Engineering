import copy
from typing import Union

from ai_data_eng.halma_game.globals import PLAYER, STATE
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm
from ai_data_eng.halma_game.utils import get_neighbourhood


class AdaptiveWeightsPlayer(Player):

    def __init__(self, plr: PLAYER, search_alg: SearchAlgorithm, delta=(1 / 16)):
        super().__init__(plr, search_alg)
        self.base_weights = [[0.0 for _ in range(16)] for _ in range(16)]
        self.weights = [[0.0 for _ in range(16)] for _ in range(16)]
        self.delta = delta
        self.set_weights()

    def set_weights(self):
        unit_val = 1 / 16
        weight = -1
        for i in range(16):
            weight += unit_val
            for j in range(i + 1):
                self.base_weights[j][i - j] = weight
        weight = 1
        for i in range(15, 0, -1):
            weight -= unit_val
            for j in range(15, i - 1, -1):
                self.base_weights[j][15 - j + i] = weight

    def get_weights(self):
        return self.weights

    def update_by_move(self, game_repr: GameRepresentation):
        super().update_by_move(game_repr)
        self.update_weights(game_repr)

    def update_weights(self, game_repr: GameRepresentation):
        self.weights = copy.deepcopy(self.base_weights)
        board = game_repr.get_board()
        for field in game_repr.get_occupied_fields(self.opponent_camp):
            neighbourhood = get_neighbourhood(field)
            for neigh in neighbourhood:
                if board[neigh[0]][neigh[1]] == STATE.EMPTY:
                    self.weights[neigh[0]][neigh[1]] = min(1.0, max(-1.0, self.weights[neigh[0]][neigh[1]]
                                                                    - (-1 if self.flag == PLAYER.WHITE else 1) * self.delta))

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
