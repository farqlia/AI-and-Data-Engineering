from ai_data_eng.halma_game.globals import STATE, PLAYER, Board


class Engine:

    def __init__(self):
        self._board: Board = [[STATE.EMPTY] * 16 for _ in range(16)]
        # starting player
        self.moving_player = PLAYER.BLACK
        self.move = 0
        self._set_up()

    def _set_up(self):

        # Ustawiamy obóz Czarnego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                self._board[i][j] = STATE.BLACK

        # Ustawiamy obóz Białego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                self._board[15 - i][15 - j] = STATE.WHITE

    def _pos_on_board(self, y, x):
        """! Sprawdza, czy pole jest na planszy.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return Czy pole jest na planszy.
        """
        if (y < 0 or x < 0):
            return False
        if (y > 15 or x > 15):
            return False
        return True

    def _pos_permitted(self, y, x, forbidden):
        """! Sprawdza, czy pole jest na liście pól zakazanych.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param forbidden Lista pól zakazanych.

        @return Czy pole jest na liście pól zakazanych.
        """

        if ((y, x) in forbidden):
            return False
        return True

    def _validate_pos(self, y, x, forbidden):
        """! Sprawdza, czy wolno się ruszyć na dane pole.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param visited Lista pól zakazanych.

        @return Czy wolno się ruszyć na dane pole.
        """
        if self._pos_on_board(y, x) and self._pos_permitted(y, x, forbidden):  # noqa: E129
            return True
        return False

    def moves(self, y, x):
        return self._moves(y, x)

    def _moves(self, y, x, visited=[]):
        """! Funkcja pomocnicza metody moves.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param visited Odwiedzone pola.

        @return Pola na które można się ruszyć.
        TODO: IMPLEMENT THIS WITH USE OF QUEUE (BFS)
        """
        delta_y = [-1, 0, 1, 1, 1, 0, -1, -1]
        delta_x = [1, 1, 1, 0, -1, -1, -1, 0]  # noqa: E201

        possible = []

        for dy, dx in zip(delta_y, delta_x):
            if (self._validate_pos(y + dy, x + dx, visited) and
                self._board[y + dy][x + dx] == STATE.EMPTY):  # noqa E129

                if len(visited) == 0:
                    possible.append((y + dy, x + dx))

            elif (self._validate_pos(y + 2 * dy, x + 2 * dx, visited) and
                  self._board[y + 2 * dy][x + 2 * dx] == STATE.EMPTY):

                possible.append((y + 2 * dy, x + 2 * dx))

                # Unikamy kopiowania tablicy.
                # Dodajemy tylko do niej obecną
                # pozycję, a następnie ją usuwamy.
                visited.append((y, x))
                possible += self._moves(y + 2 * dy, x + 2 * dx, visited)
                visited.pop()

        return possible

    def get_board(self):
        """! Returns gameboard.

        @return Plansza.
        """

        return self._board

    def set_field(self, y, x, value):
        """! Ustawia pole w danym stanie.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param value Stan pola.
        """

        if (not self._pos_on_board(y, x)):
            raise ValueError('No such a field.')

        if (value not in STATE):
            raise ValueError('Not a valid value for field.')

        self._board[y][x] = value

    def read_field(self, y, x):
        """! Zwraca stan danego pola.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return Stan pola.
        """

        if (not self._pos_on_board(y, x)):
            raise ValueError('No such a field.')

        value = self._board[y][x]

        if (value not in STATE):
            raise ValueError('Corrupted data.')

        return value

