import os

from faststream.rabbit import RabbitBroker

from src.app.container import MainContainer
from src.app.fast_api import build_fastapi
from src.app.fast_stream import build_faststream
from src.app.utils import Singleton
from src.module.common.application.command_bus import CommandBus


class Application(metaclass=Singleton):

    container: MainContainer

    def __init__(self):
        config_path = os.environ.get("APP_CONFIGURATION_FILE", default="./config/development.yaml")

        self.container = MainContainer()
        self.container.config.from_yaml(config_path, required=True)

    async def start(self):
        self.container.init_resources()
        await self.broker.start()

    async def shutdown(self):
        self.container.shutdown_resources()
        await self.broker.close()

    @classmethod
    def remove_instance(cls):
        Singleton.remove_instance(cls)

    @property
    def debug(self) -> bool:
        return self.container.config.debug.as_(bool)

    @property
    def command_bus(self) -> CommandBus:
        return self.container.module_container.command_bus()

    @property
    def broker(self) -> RabbitBroker:
        return self.container.faststream.broker()

    @property
    def celery(self):
        return self.container.celery.celery()

    def api(self, **kwargs):

        return build_fastapi(
            title=self.container.config.name(),
            debug=self.debug,
            **kwargs,
        )

    def faststream(self):
        return build_faststream(broker=self.container.faststream.broker)
