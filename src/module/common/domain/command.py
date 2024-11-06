from abc import abstractmethod
from datetime import datetime
from logging import Logger, getLogger
from typing import Type, TypeVar

from pydantic import BaseModel, ConfigDict


class Command(BaseModel):
    model_config = ConfigDict(frozen=True)

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name()})"


CommandType = TypeVar("CommandType", bound=Command)


class CommandHandler[CommandType]:

    log: Logger = getLogger()

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

    @classmethod
    @abstractmethod
    def command_type(cls) -> Type[CommandType]: ...
