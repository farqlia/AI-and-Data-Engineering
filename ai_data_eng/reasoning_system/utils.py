import logging
import sys


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

    logger = logging.getLogger(__name__)
    logger.setLevel(minimal_level)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    return logger


def filter_maker(level):
    def filter_log(record):
        return record.levelno <= level

    return filter_log
