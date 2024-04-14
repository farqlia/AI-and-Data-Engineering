from enum import Enum


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