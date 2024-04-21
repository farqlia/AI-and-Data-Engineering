from abc import ABC, abstractmethod
from typing import Union, List

from ai_data_eng.halma_game.globals import PLAYER, Field, Board, Move


class GameRepresentation(ABC):

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def get_board(self) -> Board:
        pass

    @abstractmethod
    def round_number(self) -> int:
        pass

    @abstractmethod
    def moving_player(self) -> PLAYER:
        '''
        Returns player whose move is to be performed
        '''
        pass

    @abstractmethod
    def possible_moves(self, field_from: Field) -> List[Field]:
        pass

    @abstractmethod
    def move(self, field_from: Field, field_to: Field) -> Union[Move, None]:
        '''
        Tries to perform move from field_from to field_to and returns performed move or None if no move is done
        Or maybe do not validate this move?
        '''
        pass

    @abstractmethod
    def get_winner(self) -> Union[PLAYER, None]:
        '''
        Checks if the game is finished and returns the winner; otherwise, returns None
        '''
        pass


