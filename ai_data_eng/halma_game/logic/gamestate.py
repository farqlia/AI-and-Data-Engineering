import logging
from typing import Union, List

from ai_data_eng.halma_game.globals import PLAYER, STATE, CAMP, Field, Board
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation


class GameState(GameRepresentation):

    def __init__(self, engine: Engine):
        """! Konstruktor klasy GameInterface.

        @param engine Obiekt klasy Engine.
        """
        self._engine = engine
        self.prev_move_stack = []

    def setup(self):
        pass

    def get_board(self) -> Board:
        """! Zwraca planszę do gry.

        @return Plansza do gry.
        """
        return self._engine.get_board()

    def move_number(self) -> int:
        """! Zwraca numer obecnego ruchu.

        @return Numer ruchu.
        """
        return self._engine.move

    def moving_player(self):
        """! Gracz którego jest ruch w typie wyliczeniowym PLAYER.

        @return Gracz, którego jest ruch.
        """
        return self._engine.moving_player

    # TODO: consider if the move should really be validated here
    def _validate_move(self, field1, field2):
        """! Sprawdza, czy obecnie ruszający się gracz może wykonać taki ruch.

        @param field1 Pole z którego chcemy się ruszyć.
        @param field2 Pole na które chcemy się ruszyć.

        @return Czy można wykonać ruch.
        """

        # Najpierw należy sprawdzić, czy na polu
        # z którego chcemy się ruszyć stoi kamień
        # gracza, który ma teraz swój ruch.
        if self._engine.moving_player == PLAYER.WHITE:
            field_state = STATE.WHITE
        else:
            field_state = STATE.BLACK

        board = self._engine.get_board()
        if board[field1[0]][field1[1]] != field_state:
            return False

        # Teraz należy sprawdzić, czy z danego pola
        # da się wykonać ruch tam gdzie chcemy.
        possible_moves = self._engine.moves(*field1)
        if field2 not in possible_moves:
            return False

        return True

    def _apply_move(self, field1, field2):
        """! Wykonuje ruch.

        @param field1 Pole z którego chcemy się ruszyć.
        @param field2 Pole na które chcemy się ruszyć.
        """

        on_field1 = self._engine.read_field(*field1)
        self._engine.set_field(*field1, STATE.EMPTY)
        self._engine.set_field(*field2, on_field1)

        if self._engine.moving_player == PLAYER.WHITE:
            # Jeżeli teraz ruszał się biały, to
            # teraz jest kolej na czarnego.
            self._engine.moving_player = PLAYER.BLACK
        else:
            # Jeżeli w danym ruchu ruszył się czarny,
            # przechodzimy do następnego ruchu.
            self._engine.moving_player = PLAYER.WHITE


    def possible_moves(self, field_from: Field) -> List[Field]:
        return self._engine.moves(*field_from)

    def move(self, field_from: Field, field_to: Field) -> bool:
        """! Funkcja wykonująca ruch.

        @param move_str Zapis ruchu.

        @return Wykonany ruch (lub None jeśli się nie udało).
        """

        if not self._validate_move(field_from, field_to):
            logging.warning(f"{self.moving_player()} is illegal: {field_from} -> {field_to}")
            return False

        self._apply_move(field_from, field_to)
        self.prev_move_stack.append((field_from, field_to))
        self._engine.move += 1
        return True

    def backtrack(self):
        field_to, field_from = self.prev_move_stack.pop()
        on_field1 = self._engine.read_field(*field_from)
        self._engine.set_field(*field_from, STATE.EMPTY)
        self._engine.set_field(*field_to, on_field1)
        self._engine.moving_player = PLAYER.WHITE if on_field1 == STATE.WHITE else PLAYER.BLACK
        self._engine.move -= 1

    def in_camp(self, y, x):
        """! Sprawdza w jakim obozie znajduje się pole.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return W jakim obozie znajduje się pole.
        """

        # Sprawdzamy, czy jest w obozie Czarnego.
        if (x in range(0, 5) and
                y in range(0, [5, 5, 4, 3, 2][x])):
            return CAMP.BLACK

        # Sprawdzamy, czy jest w obozie Białego.
        if (x in range(11, 16) and
                15 - y in range(0, [5, 5, 4, 3, 2][15 - x])):
            return CAMP.WHITE

        return None

    def check_white_player(self):
        board = self._engine.get_board()
        all_full = True

        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                if board[i][j] != STATE.WHITE:
                    all_full = False
                    break

        if all_full:
            return PLAYER.WHITE

    def check_black_player(self):
        board = self._engine.get_board()
        all_full = True

        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                if board[15 - i][15 - j] != STATE.BLACK:
                    all_full = False
                    break

        if all_full:
            return PLAYER.BLACK

    def get_winner(self) -> Union[PLAYER, None]:
        """! Sprawdza, czy jest koniec gry.

        Zwraca zwycięzcę w typie wyliczeniowym
        PLAYER.

        @return Zwycięzca.
        """

        white_player = self.check_white_player()
        black_player = self.check_black_player()

        if white_player:
            return white_player
        elif black_player:
            return black_player

        return None
