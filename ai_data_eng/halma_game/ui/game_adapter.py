import logging
from pathlib import Path
from typing import Union

from ai_data_eng.halma_game.game import GamePlaying
from ai_data_eng.halma_game.globals import Board, PLAYER, Move
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from timeit import default_timer as timer


class GameUiAdapter:

    '''
    Adapter between game and game ui
    '''
    def __init__(self, game_repr: GameRepresentation,
                 player1: Player, player2: Player,
                 save_dir: Path):
        self.game_repr = game_repr
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.save_dir = save_dir

    def setup(self):
        self.game_playing = GamePlaying(self.game_repr, self.player1, self.player2)

    def next(self):
        self.current_player = self.player1 if self.game_repr.moving_player() == self.player1.flag else self.player2
        start = timer()
        move = self.game_playing.next()
        end = timer()
        time = end - start
        self.save_player_stats(self.game_repr.moving_player(), time, move, self.current_player.search_tree_size())
        return move

    def is_finished(self) -> Union[PLAYER, None]:
        winner = self.game_repr.get_winner()
        if winner is not None:
            logging.info(f"The winner is {winner}")
            self.save_match_stats(winner)
        return winner

    def save_match_stats(self, winner):
        with open(self.save_dir / 'match-stats', mode='a') as f:
            f.write(f"{self.game_repr.round_number()},{winner}")

    def save_player_stats(self, player: PLAYER, time: float, move: Move, tree_size: int):
        with open(self.save_dir / str(player), mode='a') as f:
            from_, to = move
            f.write(f"{from_[0],from_[1]};{to[0],to[1]};{time:.2f},{tree_size}")

    def get_board(self) -> Board:
        return self.game_repr.get_board()

    def moving_player(self) -> int:
        return self.game_repr.moving_player().value

    def round_number(self) -> int:
        return self.game_playing.round


