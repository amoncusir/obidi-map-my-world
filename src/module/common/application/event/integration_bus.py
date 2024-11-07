import asyncio
from abc import abstractmethod
from dataclasses import dataclass

from src.module.common.application.event.integration import IntegrationEvent


@dataclass(frozen=True)
class IntegrationEventTask:
    id: str


class IntegrationEventsBus:

    @abstractmethod
    async def async_publish(self, event: IntegrationEvent) -> IntegrationEventTask: ...

    def publish(self, event: IntegrationEvent):
        loop = asyncio.get_event_loop()
        loop.create_task(self.async_publish(event))
