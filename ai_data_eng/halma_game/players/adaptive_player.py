from typing import Union, List, Dict, Callable

from ai_data_eng.halma_game.globals import PLAYER, STRATEGY
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm


def change_strategy_on_round(game_repr: GameRepresentation):
    if game_repr.round_number() % 2 == 0:
        return STRATEGY.DIAGONAL_WEIGHTS
    else:
        return STRATEGY.DISTANCE


class AdaptivePlayer(Player):

    def __init__(self, plr: PLAYER, search_alg: SearchAlgorithm):
        super().__init__(plr, search_alg,
                         STRATEGY.DIAGONAL_WEIGHTS)
        self.strategies = {STRATEGY.DIAGONAL_WEIGHTS: Player(plr, search_alg, STRATEGY.DIAGONAL_WEIGHTS),
                           STRATEGY.DISTANCE: Player(plr, search_alg, STRATEGY.DISTANCE)}
        self.strategy_chooser = change_strategy_on_round

    def evaluate(self, game_repr: GameRepresentation) -> Union[float, None]:
        return self.strategies[self.strategy_chooser(game_repr)].evaluate(game_repr)
