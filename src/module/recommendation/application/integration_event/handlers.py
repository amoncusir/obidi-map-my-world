from src.module.common.application.event.integration import IntegrationEventSubscriber
from src.module.manager.application.integration_event.events import (
    CreatedPlaceApplicationEvent,
    ReviewAddedApplicationEvent,
)


class CreatedPlaceIntegrationEventSubscriber(IntegrationEventSubscriber[CreatedPlaceApplicationEvent]):
    """
    Subscription to CreatedPlaceApplicationEvent.
    Create a new recommendation
    """

    async def handle_event(self, event: CreatedPlaceApplicationEvent): ...

    @classmethod
    def name(cls) -> str:
        return "place.created.to.recommendation"

    @classmethod
    def routing_key(cls) -> str:
        return "place.created"


class ReviewAddedIntegrationEventSubscriber(IntegrationEventSubscriber[ReviewAddedApplicationEvent]):
    """
    Subscription to ReviewAddedApplicationEvent.
    Pass through the recommendation layer to decide if it changes
    """

    async def handle_event(self, event: ReviewAddedApplicationEvent): ...

    @classmethod
    def name(cls) -> str:
        return "place.updated.review_added.to.recommendation"

    @classmethod
    def routing_key(cls) -> str:
        return "place.updated.review_added"
