from dataclasses import dataclass
from typing import Type

from src.module.common.application.event.integration_bus import IntegrationEventsBus
from src.module.common.domain.events import DomainEventSubscriber
from src.module.manager.application.integration_event.events import (
    ReviewAddedApplicationEvent,
)
from src.module.manager.domain.place.events import ReviewAddedDomainEvent
from src.module.manager.domain.place.projections import (
    PlaceProjection,
    ReviewProjection,
)


@dataclass
class PublishEventWhenReviewAddedDomainSubscriber(DomainEventSubscriber[ReviewAddedDomainEvent]):
    integration_event_bus: IntegrationEventsBus

    @classmethod
    def event_type(cls) -> Type[ReviewAddedDomainEvent]:
        return ReviewAddedDomainEvent

    async def handle_event(self, event: ReviewAddedDomainEvent):
        integration_event = ReviewAddedApplicationEvent(
            place_projection=PlaceProjection.from_entity(event.place),
            added_review=ReviewProjection.from_entity(event.added_review),
        )

        await self.integration_event_bus.async_publish(integration_event)
