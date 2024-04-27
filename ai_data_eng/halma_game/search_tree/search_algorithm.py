from abc import ABC, abstractmethod
from typing import Union, Tuple, Set

from ai_data_eng.halma_game.globals import Move, Board, PLAYER
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.utils import concat_board_state, hash_board


# Candidate moves can be also generated differently
def generate_candidate_moves(game_repr: GameRepresentation, plr_flag: PLAYER):
    for field_from in game_repr.get_occupied_fields(plr_flag):
        for field_to in game_repr.possible_moves(field_from):
            yield field_from, field_to


def to_be_visited(board: Board, already_visited: Set[int]):
    pos_hash = hash_board(board)
    if pos_hash in already_visited:
        # logging.debug(f"{pos_hash} already visited")
        return False
    already_visited.add(pos_hash)
    # logging.debug(f"Already visited set: " + str(already_visited))
    return True


class SearchAlgorithm(ABC):

    def __init__(self, search_depth):
        self.search_depth = search_depth
        self.tree_size = 0
        self.forbidden_nodes = set()
        self.name = ""

    @abstractmethod
    def _search(self, game_repr: GameRepresentation, player) -> Move:
        pass

    def get_searched_tree_size(self):
        return self.tree_size

    def update_by_move(self, game_repr: GameRepresentation):
        pass

    def search(self, game_repr: GameRepresentation, player) -> Move:
        self.tree_size = 0
        return self._search(game_repr, player)

