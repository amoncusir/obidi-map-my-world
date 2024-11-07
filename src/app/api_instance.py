"""
!! IMPORTANT !!

DO NOT import this module!
"""

from src.app.logger import configure_logger

configure_logger()


from src.app import application  # nopep8

api = application().api
