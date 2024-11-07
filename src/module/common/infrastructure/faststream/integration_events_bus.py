from faststream.rabbit import RabbitBroker, RabbitExchange

from src.module.common.application.event.integration import IntegrationEvent
from src.module.common.application.event.integration_bus import (
    IntegrationEventsBus,
    IntegrationEventTask,
)


class FastStreamIntegrationEventsBus(IntegrationEventsBus):

    broker: RabbitBroker
    exchange: RabbitExchange

    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def async_publish(self, event: IntegrationEvent) -> IntegrationEventTask:
        await self.broker.publish(event, routing_key=event.name(), message_id=str(event.id), exchange=self.exchange)
        return IntegrationEventTask(event.id)
