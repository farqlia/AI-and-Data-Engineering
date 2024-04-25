import copy

import pytest

from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.utils import concat_board_state


@pytest.fixture()
def engine():
    return Engine()

@pytest.fixture()
def game_state(engine):
    return GameState(engine)


def test_game_repr_copy(game_state):
    game_repr_copy = copy.deepcopy(game_state)
    gs1 = concat_board_state(game_state.get_board())
    print(gs1)
    game_state.move((4, 1), (4, 2))
    gs2 = concat_board_state(game_state.get_board())
    print(gs2)
    assert gs1 != gs2
    print(hash(gs1))
    print(hash(gs2))
    assert game_state.get_board() != game_repr_copy.get_board()


def test_backtrack(game_state):
    gs1 = concat_board_state(game_state.get_board())
    print(gs1)
    game_state.move((4, 1), (4, 2))
    gs2 = concat_board_state(game_state.get_board())
    print(gs2)
    assert gs1 != gs2
    game_state.backtrack()
    gs3 = concat_board_state(game_state.get_board())
    assert gs3 == gs1