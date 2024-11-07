"""
!! IMPORTANT !!

DO NOT import this module!
"""

from src.app.logger import configure_logger

configure_logger()


from src.app.application import Application  # nopep8

celery = Application().celery
