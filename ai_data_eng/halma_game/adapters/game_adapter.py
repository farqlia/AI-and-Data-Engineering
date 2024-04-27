import abc
import os
from pathlib import Path
from typing import Union

import pandas as pd

from ai_data_eng.halma_game.globals import STRATEGY, PLAYER
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.players.player import Player


class GameAdapter(abc.ABC):

    @abc.abstractmethod
    def next(self):
        pass

    @abc.abstractmethod
    def is_finished(self) -> Union[PLAYER, None]:
        pass

    @abc.abstractmethod
    def to_be_moved(self) -> Player:
        pass

    @abc.abstractmethod
    def round_number(self) -> int:
        pass

    @abc.abstractmethod
    def moving_player(self) -> int:
        pass