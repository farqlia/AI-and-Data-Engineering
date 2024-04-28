from ai_data_eng.halma_game.globals import Move, Board
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.search_tree.search_algorithm import SearchAlgorithm
from ai_data_eng.halma_game.utils import hash_board


# This class prevents the players from moving between the same states, inspired by TabuSearch
class MetaSearch(SearchAlgorithm):

    def __init__(self, search_depth: int, alg_init, queue_size=20):
        super().__init__(search_depth=search_depth)
        self.alg: SearchAlgorithm = alg_init(search_depth=search_depth)
        self.queue = []
        self.queue_size = queue_size
        self.name = f"m-{self.alg.name}"

    def _search(self, game_repr: GameRepresentation, player) -> Move:
        move = self.alg.search(game_repr, player)
        self.tree_size = self.alg.get_searched_tree_size()
        return move

    # This is mainly used to update the queue as the opponent makes a move
    def update_by_move(self, game_repr: GameRepresentation):
        self.update_queue(game_repr.get_board())

    def update_queue(self, board: Board):
        board_hash = hash_board(board)
        self.queue.append(board_hash)
        self.alg.forbidden_nodes.add(board_hash)
        if len(self.queue) > self.queue_size:
            # logging.info(f"Remove {self.queue[0]} from queue")
            self.alg.forbidden_nodes.remove(self.queue.pop(0))
        # logging.info(f"Queue state = {self.queue}")
        # logging.info(f"Forbidden nodes = {self.alg.forbidden_nodes}")
