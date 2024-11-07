from abc import abstractmethod

from src.module.common.application.integration_events import IntegrationEvent


class IntegrationEventsBus:

    @abstractmethod
    async def async_trigger(self, event: IntegrationEvent): ...
