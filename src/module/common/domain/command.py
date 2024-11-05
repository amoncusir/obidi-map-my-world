from abc import abstractmethod
from datetime import datetime
from logging import Logger, getLogger
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict


class Command(BaseModel):
    model_config = ConfigDict(frozen=True)

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...


CommandType = TypeVar("CommandType", bound=Command)


class CommandHandler(Generic[CommandType]):

    log: Logger

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        instance.log = getLogger(cls.__qualname__)

        return instance

    def __call__(self, command: CommandType):
        start = datetime.now()
        self.log.debug("Handled Command: %s", command)

        self.process_command(command)

        self.log.debug("Finished Command on time (%s): %s", datetime.now() - start, command)

    @abstractmethod
    def process_command(self, command: CommandType): ...
