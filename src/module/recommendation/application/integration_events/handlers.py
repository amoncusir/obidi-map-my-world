from src.module.common.application.event.integration import IntegrationEventSubscriber
from src.module.manager.application.integration_events.events import (
    ReviewAddedApplicationEvent,
)


class ReviewAddedIntegrationEventSubscriber(IntegrationEventSubscriber[ReviewAddedApplicationEvent]):
    """
    Subscription to ReviewAddedApplicationEvent.
    Pass through the recommendation layer to decide if it changes
    """

    async def handle_event(self, event: ReviewAddedApplicationEvent):
        print(event)
        print("AMZNG!")

    @classmethod
    def name(cls) -> str:
        return "place.updated.review_added.to.recommendation"

    @classmethod
    def routing_key(cls) -> str:
        return "place.updated.review_added"
