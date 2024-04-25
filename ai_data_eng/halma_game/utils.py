import logging
import sys

from ai_data_eng.halma_game.globals import Board, STATE


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


def concat_board_state(board: Board) -> str:
    return ''.join([str(board[i][j].value) for i in range(16) for j in range(16)])


configure_logging(logging.INFO)
