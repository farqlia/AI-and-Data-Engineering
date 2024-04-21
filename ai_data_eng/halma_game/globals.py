from enum import Enum

from typing import Tuple, List


class STATE(Enum):
    """! Stan pola planszy. """
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class PLAYER(Enum):
    BLACK = 1
    WHITE = 2


class CAMP(Enum):
    """! Obóz. """
    BLACK = 1
    WHITE = 2


Field = Tuple[(int, int)]
Board = List[List[STATE]]
Move = Tuple[Field, Field]