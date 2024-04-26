import os
from enum import Enum

from typing import Tuple, List
from pathlib import Path

HALMA_DIR = Path('../../data/halma')
os.makedirs(HALMA_DIR, exist_ok=True)


class STRATEGY(Enum):
    STATIC_WEIGHTED = 'static weighted'
    DISTANCE = 'distance'
    NONE = 'none'


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