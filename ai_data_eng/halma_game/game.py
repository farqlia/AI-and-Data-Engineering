import logging
from typing import Tuple

from ai_data_eng.halma_game.globals import Move
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player


class GamePlaying:

    def __init__(self, game_repr: GameRepresentation,
                 player1: Player, player2: Player):

        self.game_repr = game_repr
        self._player_1: Player = player1
        self._player_2: Player = player2

    def next(self) -> Tuple[Move, float]:
        logging.info(f"({self.game_repr.move_number()}) Player {self.game_repr.moving_player()} turn")
        if self.game_repr.moving_player() == self._player_1.flag:
            move = self.apply_player_move(self._player_1)
        else:
            move = self.apply_player_move(self._player_2)
        self._player_1.update_by_move(game_repr=self.game_repr)
        self._player_2.update_by_move(game_repr=self.game_repr)
        return move

    def apply_player_move(self, player: Player):
        '''
        Apply current player move and return it, plus some metadata info
        '''
        next_move, value = player.make_move(self.game_repr)
        curr_player = self.game_repr.moving_player()
        if next_move:
            self.game_repr.move(*next_move)
            logging.debug(f"Player {curr_player} move : {next_move[0]} -> {next_move[1]}")
        else:
            logging.warning(f"Player {curr_player} move was invalid")
        logging.debug(f"Player {curr_player} tree depth is {player.search_tree_size()}")
        return next_move, value
