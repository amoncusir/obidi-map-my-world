"""
!! IMPORTANT !!

DO NOT import this module!
"""

from src.app.logger import configure_logger

configure_logger()


from src.app.api import build_fastapi  # nopep8

api = build_fastapi()
