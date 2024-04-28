import logging
import logging
import sys
from typing import Set

from ai_data_eng.halma_game.globals import Move
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm, to_be_visited, generate_candidate_moves


class AlphaBeta(SearchAlgorithm):

    def __init__(self, search_depth):
        super().__init__(search_depth)
        self.best_move = None
        self.name = "alphabeta"

    def _search(self, game_repr: GameRepresentation, player: Player) -> Move:
        best_val = self.alphabeta_search(game_repr, player, 0, set(self.forbidden_nodes),
                                         -sys.maxsize + 1, sys.maxsize)
        logging.info(f"Best value: {best_val:.2f}")
        best_move = self.best_move
        self.best_move = None
        return best_move

    def search_min(self, game_repr: GameRepresentation, player: Player, depth: int,
                   already_visited: Set[int], alpha: float, beta: float):
        tree_size_before = self.tree_size
        logging.debug(f"[{depth}/{self.tree_size}] MIN {game_repr.moving_player()}")
        for (field_from, field_to) in generate_candidate_moves(game_repr, game_repr.moving_player()):
            is_moved = game_repr.move(field_from, field_to)
            logging.debug(f"Try move {field_from} -> {field_to}")
            if is_moved and to_be_visited(game_repr.get_board(), already_visited):
                value = self.alphabeta_search(game_repr, player, depth + 1, already_visited, alpha, beta)
                if value is not None:
                    beta = min(beta, value)
                    self.tree_size += 1
            if is_moved:
                game_repr.backtrack()
            if alpha >= beta:
                return beta  # cut off
        if self.tree_size == tree_size_before:
            beta = None
        logging.debug(f"[{depth}/{self.tree_size}] Min value = {beta} {len(already_visited)}")
        return beta

    def search_max(self, game_repr: GameRepresentation, player: Player, depth: int,
                   already_visited: Set[int], alpha: float, beta: float):
        tree_size_before = self.tree_size
        # take max over children
        logging.debug(f"[{depth}/{self.tree_size}] MAX {game_repr.moving_player()}")
        for (field_from, field_to) in generate_candidate_moves(game_repr, game_repr.moving_player()):
            is_moved = game_repr.move(field_from, field_to)
            if is_moved and to_be_visited(game_repr.get_board(), already_visited):
                logging.debug(f"Try move  {field_from} -> {field_to}")
                value = self.alphabeta_search(game_repr, player, depth + 1, already_visited, alpha, beta)
                # None is if the node is invalid
                if value is not None:
                    self.tree_size += 1
                    if value >= alpha:
                        alpha = value
                        if depth == 0:
                            self.best_move = (field_from, field_to)
                            logging.debug(f"Best move: {self.best_move}")
            if is_moved:
                game_repr.backtrack()
            if alpha >= beta:
                return alpha  # cut off
            # if the tree hasn't been searched at all
        if self.tree_size == tree_size_before:
            alpha = None
        logging.debug(f"[{depth}/{self.tree_size}] Max value = {alpha} {len(already_visited)}")
        return alpha

    # utilize backtracking to not copy the whole board
    def alphabeta_search(self, game_repr: GameRepresentation, player: Player, depth: int,
                         already_visited: Set[int], alpha: float, beta: float) -> float:

        winner = game_repr.get_winner()
        if winner:
            logging.info(f"[{depth}/{self.tree_size}] Winner {winner}")
            return sys.maxsize if winner == player.repr() else -sys.maxsize + 1

        elif depth >= self.search_depth:
            # cut searching at max depth
            return player.evaluate(game_repr)

        # take max over children
        if game_repr.moving_player() == player.repr():
            return self.search_max(game_repr, player, depth, already_visited, alpha, beta)
        else:
            return self.search_min(game_repr, player, depth, already_visited, alpha, beta)
