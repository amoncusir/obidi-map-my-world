import logging
import os
import sys
from logging import DEBUG, Formatter, Handler, getLogger
from typing import Final

LOG_LEVEL: Final[int] = os.environ.get("LOG_LEVEL", logging.DEBUG)


def build_formatter() -> Formatter:
    formatter = Formatter("%(levelname)s:\t%(name)s --- %(message)s")
    return formatter


def build_handler() -> Handler:

    handler = logging.StreamHandler(sys.stdout)
    formatter = build_formatter()
    handler.setFormatter(formatter)

    return handler


def configure_logger():
    handler = build_handler()

    project_logger = getLogger("src")
    project_logger.setLevel(DEBUG)
    project_logger.addHandler(handler)
    project_logger.propagate = False
