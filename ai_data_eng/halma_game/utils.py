import logging
import sys
from pathlib import Path
from typing import Set

import pandas as pd

from ai_data_eng.halma_game.globals import Board, STATE, CAMP, Field
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.game_representation import GameRepresentation
from ai_data_eng.halma_game.logic.gamestate import GameState


def configure_logging(minimal_level=logging.DEBUG):
    logging_format = '%(levelname)s: %(asctime)s - %(message)s'
    formatter = logging.Formatter(logging_format)
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    console_handler.addFilter(filter_maker(logging.WARNING))
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(minimal_level)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)


def filter_maker(level):

    def filter_log(record):
        return record.levelno <= level

    return filter_log


def cell_value(cell):
    return cell.value if isinstance(cell, STATE) else cell

def print_board(board):
    print("   ", " ".join([f"{n:02}" for n in range(16)]))
    print("----------------------------------------------------")
    for i in range(16):
        print(f"{i:02}", "|", "  ".join([str(cell_value(board[i][j])) for j in range(16)]), "|", f"{i:02}")
    print("----------------------------------------------------")
    print("   ", " ".join([f"{n:02}" for n in range(16)]))


def get_camp_boundaries(camp: CAMP) -> Set[Field]:
    return {(15, 11), (14, 11), (13, 12), (12, 13), (11, 14), (11, 15)} if camp == CAMP.WHITE else \
        {(4, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 4)}


def hash_board(board: Board) -> int:
    board_string = concat_board_state(board)
    assert len(board_string) == 256
    return hash(board_string)


def split(field):
    pos = field.split(',')
    return int(pos[0]), int(pos[1])


def concat_board_state(board: Board) -> str:
    return ''.join([str(board[i][j].value) for i in range(16) for j in range(16)])


def read_game_state_from_file(dir_path: Path, steps: int) -> GameRepresentation:
    player_black = pd.read_csv(dir_path / 'PLAYER.BLACK', header=None, sep=';')
    player_white = pd.read_csv(dir_path / 'PLAYER.WHITE', header=None, sep=';')
    engine = Engine()
    game_repr = GameState(engine)
    for i in range(steps):
        game_repr.move(split(player_black.iloc[i, 0]),
                       split(player_black.iloc[i, 1]))
        game_repr.move(split(player_white.iloc[i, 0]),
                       split(player_white.iloc[i, 1]))

    return game_repr


configure_logging(logging.INFO)
