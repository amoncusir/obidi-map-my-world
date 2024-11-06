from functools import singledispatchmethod
from typing import Any, Dict, List, Type

from src.module.common.domain.command import Command, CommandHandler
from src.module.common.domain.errors import DomainError


class CommandBusNoHandlerFoundError(DomainError):
    pass


class CommandBus:

    handlers: Dict[Type[Command], CommandHandler]

    def __init__(self, handlers: List[CommandHandler[Any]]):
        self.handlers = {h.command_type(): h for h in handlers}

    @singledispatchmethod
    def find_handler(self, command: Type[Command]) -> CommandHandler:
        handler = self.handlers.get(command)

        if handler is None:
            raise CommandBusNoHandlerFoundError(f"Not found any handler for command {repr(command)}")

        return handler

    @find_handler.register
    def _(self, command: Command):
        return self.find_handler(type(command))

    def exec(self, command: Command):
        if not isinstance(command, Command):
            raise ValueError("Invalid command type. Must be a Command base instance")

        handler = self.find_handler(command)
        handler(command)
