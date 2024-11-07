from dataclasses import dataclass
from typing import Type

from src.module.common.application.event.integration_bus import IntegrationEventsBus
from src.module.common.domain.events import DomainEventSubscriber
from src.module.manager.application.integration_events.events import (
    CreatedPlaceApplicationEvent,
)
from src.module.manager.domain.place.events import CreatedPlaceDomainEvent


@dataclass
class PublishEventWhenCreatedPlaceDomainSubscriber(DomainEventSubscriber[CreatedPlaceDomainEvent]):

    integration_event_bus: IntegrationEventsBus

    @classmethod
    def event_type(cls) -> Type[CreatedPlaceDomainEvent]:
        return CreatedPlaceDomainEvent

    async def handle_event(self, event: CreatedPlaceDomainEvent):
        projection = event.new_place
        integration_event = CreatedPlaceApplicationEvent(
            place_projection=projection,
        )

        await self.integration_event_bus.async_publish(integration_event)
