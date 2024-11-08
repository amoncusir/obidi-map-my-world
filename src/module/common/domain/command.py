from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from logging import Logger, getLogger
from typing import Type, TypeVar

from pydantic import BaseModel, ConfigDict


@dataclass(frozen=True, kw_only=True)
class Command:
    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name()})"


class CommandResult(BaseModel):
    model_config = ConfigDict(frozen=True)


CommandType = TypeVar("CommandType", bound=Command)
ReturnType = TypeVar("ReturnType", bound=CommandResult)


class CommandHandler[CommandType, ReturnType]:

    log: Logger = getLogger(__name__)

    async def __call__(self, command: CommandType) -> ReturnType:
        start = datetime.now()
        self.log.debug("Handled Command: %s", command)

        result = await self.handle_command(command)

        self.log.debug("Finished Command on time (%s): %s", datetime.now() - start, command)

        return result

    @abstractmethod
    async def handle_command(self, command: CommandType) -> ReturnType: ...

    @classmethod
    @abstractmethod
    def command_type(cls) -> Type[CommandType]: ...
