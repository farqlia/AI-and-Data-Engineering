from ai_data_eng.halma_game.game import GamePlaying
from ai_data_eng.halma_game.globals import Board, PLAYER
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player


class GameUiAdapter:

    '''
    Adapter between game and game ui
    '''
    def __init__(self, game_repr: GameRepresentation,
                 player1: Player, player2: Player,
                 history_depth: int = 1):
        self.game_repr = game_repr
        self.player1 = player1
        self.player2 = player2
        # keeps track of n previous moves
        self.history = []

    def setup(self):
        self.game_playing = GamePlaying(self.game_repr, self.player1, self.player2)

    def next(self):

        move = self.game_playing.next()
        return move

    def get_previous_state(self, n: int):
        return self.history[-n] if len(self.history) >= n else None

    def get_board(self) -> Board:
        return self.game_repr.get_board()

    def moving_player(self) -> int:
        return 1 if self.game_repr.moving_player() == PLAYER.BLACK else 2

    def round_number(self) -> int:
        return self.game_repr.round_number()


