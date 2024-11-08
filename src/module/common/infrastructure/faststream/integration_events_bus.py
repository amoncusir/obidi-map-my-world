from dataclasses import dataclass
from logging import getLogger

from faststream.rabbit import RabbitBroker, RabbitExchange

from src.module.common.application.event.integration import IntegrationEvent
from src.module.common.application.event.integration_bus import (
    IntegrationEventsBus,
    IntegrationEventTask,
)

logger = getLogger(__name__)


@dataclass
class FastStreamIntegrationEventsBus(IntegrationEventsBus):

    broker: RabbitBroker
    exchange: RabbitExchange

    async def async_publish(self, event: IntegrationEvent) -> IntegrationEventTask:

        await self.broker.publish(event, routing_key=event.name(), message_id=str(event.id), exchange=self.exchange)

        logger.debug("Event Published: %s", repr(event))

        return IntegrationEventTask(event.id)
