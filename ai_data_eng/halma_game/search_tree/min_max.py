import copy
import logging
import sys
from typing import Set, Union, Tuple

import numpy as np

from ai_data_eng.halma_game.globals import Board, PLAYER, Move, Field
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm, to_be_visited, generate_candidate_moves
from ai_data_eng.halma_game.utils import concat_board_state


class MinMax(SearchAlgorithm):

    def __init__(self, search_depth):
        super().__init__(search_depth)
        self.best_move = None

    def _search(self, game_repr: GameRepresentation, player: Player) -> Move:
        best_val = self.minmax_search(game_repr, player, 0, set(self.forbidden_nodes))
        logging.info(f"Best value: {best_val}")
        best_move = self.best_move
        self.best_move = None
        return best_move

    # utilize backtracking to not copy the whole board
    def minmax_search(self, game_repr: GameRepresentation, player: Player, depth: int,
                      already_visited: Set[int]) -> float:

        winner = game_repr.get_winner()
        if winner:
            logging.debug(f"[{depth}/{self.tree_size}] Winner {winner}")
            return sys.maxsize if winner == player.repr() else -sys.maxsize + 1

        elif depth >= self.search_depth:
            # cut searching at max depth
            return player.evaluate(game_repr)

        tree_size_before = self.tree_size
        # take max over children
        if game_repr.moving_player() == player.repr():
            logging.debug(f"[{depth}/{self.tree_size}] MAX {game_repr.moving_player()}")
            max_value = -sys.maxsize + 1
            for (field_from, field_to) in generate_candidate_moves(game_repr, game_repr.moving_player()):
                is_moved = game_repr.move(field_from, field_to)
                if is_moved and to_be_visited(game_repr.get_board(), already_visited):
                    # logging.debug(f"Move {field_from} -> {field_to}")
                    value = self.minmax_search(game_repr, player, depth + 1, already_visited)
                    # None is if the node is invalid
                    if value is not None:
                        self.tree_size += 1
                        if value > max_value:
                            max_value = value
                            if depth == 0:
                                self.best_move = (field_from, field_to)
                if is_moved:
                    game_repr.backtrack()
            # if the tree hasn't been searched at all
            if self.tree_size == tree_size_before:
                max_value = None
                self.best_move = None
            logging.debug(f"[{depth}/{self.tree_size}] Max value = {max_value} {len(already_visited)}")
            return max_value
        else:
            logging.debug(f"[{depth}/{self.tree_size}] MIN {game_repr.moving_player()}")
            min_value = sys.maxsize
            for (field_from, field_to) in generate_candidate_moves(game_repr, game_repr.moving_player()):
                is_moved = game_repr.move(field_from, field_to)
                # logging.debug(f"Try move {field_from} -> {field_to}")
                if is_moved and to_be_visited(game_repr.get_board(), already_visited):
                    value = self.minmax_search(game_repr, player, depth + 1, already_visited)
                    if value is not None:
                        min_value = min(min_value, value)
                        self.tree_size += 1
                if is_moved:
                    game_repr.backtrack()
            if self.tree_size == tree_size_before:
                min_value = None
            logging.debug(f"[{depth}/{self.tree_size}] Min value = {min_value} {len(already_visited)}")
            return min_value

