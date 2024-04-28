import logging
import logging
import sys
from typing import Set, Tuple

from ai_data_eng.halma_game.globals import Move
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm, to_be_visited, generate_candidate_moves


class MinMax(SearchAlgorithm):

    def __init__(self, search_depth):
        super().__init__(search_depth)
        self.best_move = None
        self.name = "minmax"

    def _search(self, game_repr: GameRepresentation, player: Player)-> Tuple[Move, float]:
        best_val = self.minmax_search(game_repr, player, 0, set(self.forbidden_nodes))
        logging.info(f"Best value: {best_val:.2f}")
        best_move = self.best_move
        self.best_move = None
        return best_move, best_val

    def search_min(self, game_repr: GameRepresentation, player: Player, depth: int,
                   already_visited: Set[int]):
        logging.debug(f"[{depth}/{self.tree_size}] MIN {game_repr.moving_player()}")
        min_value = sys.maxsize
        for (field_from, field_to) in generate_candidate_moves(game_repr, game_repr.moving_player()):
            game_repr.move(field_from, field_to)
            # logging.debug(f"Try move {field_from} -> {field_to}")
            if to_be_visited(game_repr.get_board(), already_visited):
                value = self.minmax_search(game_repr, player, depth + 1, already_visited)
                min_value = min(min_value, value)
                self.tree_size += 1
            else:
                min_value = min(min_value, player.evaluate(game_repr))
            game_repr.backtrack()
        logging.debug(f"[{depth}/{self.tree_size}] Min value = {min_value} {len(already_visited)}")
        return min_value

    def search_max(self, game_repr: GameRepresentation, player: Player, depth: int,
                   already_visited: Set[int]):
        # take max over children
        logging.debug(f"[{depth}/{self.tree_size}] MAX {game_repr.moving_player()}")
        max_value = -sys.maxsize + 1
        for (field_from, field_to) in generate_candidate_moves(game_repr, game_repr.moving_player()):
            game_repr.move(field_from, field_to)
            if to_be_visited(game_repr.get_board(), already_visited):
                # logging.debug(f"Try move  {field_from} -> {field_to}")
                value = self.minmax_search(game_repr, player, depth + 1, already_visited)
                self.tree_size += 1
            else:
                value = player.evaluate(game_repr)
            if value >= max_value:
                max_value = value
                if depth == 0:
                    self.best_move = (field_from, field_to)
                    logging.debug(f"Best move: {self.best_move}")
            game_repr.backtrack()
        logging.debug(f"[{depth}/{self.tree_size}] Max value = {max_value} {len(already_visited)}")
        return max_value

    # utilize backtracking to not copy the whole board
    def minmax_search(self, game_repr: GameRepresentation, player: Player, depth: int,
                      already_visited: Set[int]) -> float:

        winner = game_repr.get_winner()
        if winner:
            logging.info(f"[{depth}/{self.tree_size}] Winner {winner}")
            return sys.maxsize if winner == player.repr() else -sys.maxsize + 1

        elif depth >= self.search_depth:
            # cut searching at max depth
            return player.evaluate(game_repr)

        # take max over children
        if game_repr.moving_player() == player.repr():
            return self.search_max(game_repr, player, depth, already_visited)
        else:
            return self.search_min(game_repr, player, depth, already_visited)
