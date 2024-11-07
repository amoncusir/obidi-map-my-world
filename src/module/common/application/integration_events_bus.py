from abc import abstractmethod
from dataclasses import dataclass

from src.module.common.application.integration_events import IntegrationEvent


@dataclass(frozen=True)
class IntegrationEventTask:
    id: str


class IntegrationEventsBus:

    @abstractmethod
    async def async_trigger(self, event: IntegrationEvent) -> IntegrationEventTask: ...
