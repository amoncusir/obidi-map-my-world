from abc import abstractmethod
from datetime import datetime
from logging import Logger, getLogger
from typing import Any, Type


class BaseEventSubscriber[Event: Any]:
    log: Logger = getLogger(__name__)

    async def __call__(self, event: Event):
        start = datetime.now()
        result = await self.handle_event(event)

        self.log.debug("Handled Event on time (%s): %s", datetime.now() - start, repr(event))

        return result

    @abstractmethod
    async def handle_event(self, event: Event): ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> Type[Event]: ...
