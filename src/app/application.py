import os

from src.app.container import MainContainer
from src.app.utils import Singleton
from src.module.common.application.command_bus import CommandBus


class Application(metaclass=Singleton):

    container: MainContainer

    def __init__(self):
        config_path = os.environ.get("APP_CONFIGURATION_FILE", default="./config/development.yaml")

        self.container = MainContainer()
        self.container.config.from_yaml(config_path, required=True)

    @classmethod
    def remove_instance(cls):
        Singleton.remove_instance(cls)

    @property
    def debug(self) -> bool:
        return self.container.config.debug.as_(bool)

    @property
    def command_bus(self) -> CommandBus:
        return self.container.module_container.command_bus()
