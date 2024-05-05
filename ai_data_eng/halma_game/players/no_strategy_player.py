import random
from typing import Union

from ai_data_eng.halma_game.globals import PLAYER, STRATEGY
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm


class NoStrategyPlayer(Player):

    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        return random.random()

    def __init__(self, plr: PLAYER, search_alg: SearchAlgorithm):
        super().__init__(plr, search_alg, STRATEGY.NONE)
