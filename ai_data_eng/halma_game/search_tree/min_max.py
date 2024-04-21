import copy
import logging
import sys
from typing import Set

import numpy as np

from ai_data_eng.halma_game.globals import Board, PLAYER, Move, Field
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm
from ai_data_eng.halma_game.utils import concat_board_state


# Candidate moves can be also generated differently
def generate_candidate_moves(game_repr: GameRepresentation, player: Player):
    for field_from in player.get_occupied_fields(game_repr):
        for field_to in game_repr.possible_moves(field_from):
            yield field_from, field_to


def to_be_visited(board: Board, already_visited: Set[int]):
    board_string = concat_board_state(board)
    assert len(board_string) == 256
    pos_hash = hash(board_string)
    if pos_hash in already_visited:
        return False
    already_visited.add(pos_hash)
    return True


class MinMax(SearchAlgorithm):

    def __init__(self, search_depth):
        super().__init__(search_depth)
        self.best_move = None

    def _search(self, game_repr: GameRepresentation, player: Player) -> Move:
        self.minmax_search(game_repr, player, 0, set())
        best_move = self.best_move
        self.best_move = None
        return best_move

    def minmax_search(self, game_repr: GameRepresentation, player: Player, depth: int,
                      already_visited: Set[int]) -> float:
        logging.debug(f"[MinMax] at depth {depth}, already searched {self.search_depth}")
        game_repr = copy.deepcopy(game_repr)
        winner = game_repr.get_winner()
        if winner:
            logging.debug(f"[MinMax] at depth {depth} with winner {winner}")
            return sys.maxsize if winner == player.repr() else -sys.maxsize + 1

        elif depth == self.search_depth:
            # cut searching at max depth
            return player.evaluate(game_repr)

        # take max over children
        if game_repr.moving_player() == player.repr():
            max_value = -sys.maxsize + 1
            for (field_from, field_to) in generate_candidate_moves(game_repr, player):
                game_repr.move(field_from, field_to)
                logging.debug(f"Move {field_from} -> {field_to}")
                if to_be_visited(game_repr.get_board(), already_visited):
                    value = self.minmax_search(game_repr, player, depth + 1, already_visited)
                    logging.debug(f"Value at {field_from} -> {field_to} is {value}")
                    if value > max_value:
                        max_value = value
                        self.best_move = field_from, field_to
                    self.tree_size += 1
            return max_value
        else:
            min_value = sys.maxsize
            for (field_from, field_to) in generate_candidate_moves(game_repr, player):
                game_repr.move(field_from, field_to)
                if to_be_visited(game_repr.get_board(), already_visited):
                    min_value = min(min_value, self.minmax_search(game_repr, player, depth + 1, already_visited))
                    self.tree_size += 1
            return min_value

