import logging
import os
from pathlib import Path
from typing import Union

import pandas as pd

from ai_data_eng.halma_game.adapters.game_adapter import GameAdapter
from ai_data_eng.halma_game.globals import STRATEGY, PLAYER, Board
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.empty_player import EmptyPlayer
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.utils import split


class GameFromFileAdapter(GameAdapter):

    def moving_player(self) -> int:
        return self.game_repr.moving_player().value

    def __init__(self, game_repr: GameRepresentation, from_dir: Path, date_prefix: str):
        self.game_repr = game_repr
        strategies = str(from_dir).split('/')[-1].split('-')
        self.strategy_1 = strategies[0]
        self.strategy_2 = strategies[1]
        files = os.listdir(from_dir)
        self.player_black_df = pd.read_csv(from_dir / [f for f in files if f.endswith(f'{date_prefix}-PLAYER.BLACK')][0], header=None, sep=';')
        self.player_white_df = pd.read_csv(from_dir / [f for f in files if f.endswith(f'{date_prefix}-PLAYER.WHITE')][0], header=None, sep=';')
        self.current_player = PLAYER.BLACK
        self.dfs = {PLAYER.BLACK: self.player_black_df, PLAYER.WHITE: self.player_white_df}
        self.player1 = EmptyPlayer()
        self.player2 = EmptyPlayer()
        logging.info(f"{len(self.player_black_df)} {len(self.player_white_df)}")

    def next(self):
        self.current_player = self.game_repr.moving_player()
        logging.info(f"[{self.round_number()}] Current player: {self.current_player}")
        field_from, field_to = (split(self.dfs[self.current_player].iloc[self.round_number() // 2, 0]),
                                split(self.dfs[self.current_player].iloc[self.round_number() // 2, 1]))
        if not self.game_repr.move(field_from, field_to):
            logging.warning(f"Attempted move {field_from} -> {field_to} was invalid")
        return field_from, field_to

    def is_finished(self) -> Union[PLAYER, None]:
        winner = self.game_repr.get_winner()
        return winner

    def to_be_moved(self) -> Player:
        return self.player1

    def round_number(self) -> int:
        return self.game_repr.move_number()

    def get_board(self) -> Board:
        return self.game_repr.get_board()