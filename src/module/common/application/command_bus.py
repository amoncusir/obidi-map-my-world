from abc import abstractmethod

from src.module.common.domain.command import Command, CommandResult
from src.module.common.domain.errors import DomainError


class CommandBusNoHandlerFoundError(DomainError):
    pass


class CommandBus:

    @abstractmethod
    async def exec(self, command: Command) -> CommandResult: ...
