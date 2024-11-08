from functools import singledispatchmethod
from typing import Dict, List, Type

from src.module.common.application.command_bus import (
    CommandBus,
    CommandBusNoHandlerFoundError,
)
from src.module.common.domain.command import Command, CommandHandler, CommandResult


class InMemoryCommandBus(CommandBus):

    handlers: Dict[Type[Command], CommandHandler]

    def __init__(self, handlers: List[CommandHandler]):
        self.handlers = {h.command_type(): h for h in handlers}

    @singledispatchmethod
    def find_handler(self, command: Type[Command]) -> CommandHandler:
        handler = self.handlers.get(command, None)

        if handler is None:
            raise CommandBusNoHandlerFoundError(f"Not found any handler for command {repr(command)}")

        return handler

    @find_handler.register
    def _(self, command: Command):
        return self.find_handler(type(command))

    async def exec(self, command: Command) -> CommandResult:
        if not isinstance(command, Command):
            raise ValueError("Invalid command type. Must be a Command base instance")

        handler = self.find_handler(command)
        return await handler(command)
