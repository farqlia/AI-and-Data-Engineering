import logging

from ai_data_eng.halma_game.globals import Move, Board
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm
from ai_data_eng.halma_game.utils import concat_board_state, hash_board


class MetaSearch(SearchAlgorithm):

    def __init__(self, search_depth: int, alg_init, queue_size=30):
        super().__init__(search_depth=search_depth)
        self.alg : SearchAlgorithm = alg_init(search_depth=search_depth)
        self.queue = []
        self.queue_size = queue_size

    def _search(self, game_repr: GameRepresentation, player) -> Move:
        self.update_queue(game_repr.get_board())
        move = self.alg.search(game_repr, player)
        self.tree_size = self.alg.get_searched_tree_size()
        return move

    def update_queue(self, board: Board):
        board_hash = hash_board(board)
        self.queue.append(board_hash)
        self.alg.forbidden_nodes.add(board_hash)
        if len(self.queue) > self.queue_size:
            logging.info(f"Update queue")
            self.alg.forbidden_nodes.remove(self.queue.pop(0))