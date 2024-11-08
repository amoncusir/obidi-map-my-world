from abc import abstractmethod
from datetime import datetime
from logging import Logger, getLogger
from typing import Any


class BaseEventSubscriber[Event: Any]:
    log: Logger = getLogger(__name__)

    async def __call__(self, event: Event):
        start = datetime.now()
        result = await self.handle_event(event)

        self.log.debug("Handled Event %s, time (%s)", event.__class__.__name__, datetime.now() - start)

        return result

    @abstractmethod
    async def handle_event(self, event: Event): ...
