"""
!! IMPORTANT !!

DO NOT import this module!
"""

from contextlib import asynccontextmanager

from src.app.logger import configure_logger

configure_logger()


from src.app.application import Application  # nopep8

application = Application()


@asynccontextmanager
async def start(_):
    application.start()
    await application.broker.start()

    yield


api = application.api(lifespan=start)
