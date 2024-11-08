from dataclasses import dataclass

from src.module.common.application.event.domain_bus import DomainEventBus
from src.module.common.application.event.integration import IntegrationEventSubscriber
from src.module.manager import CreatedPlaceApplicationEvent, ReviewAddedApplicationEvent
from src.module.recommendation.domain.recommendation.projections import (
    PlaceViewProjection,
)
from src.module.recommendation.domain.recommendation.recommendation import (
    Recommendation,
)
from src.module.recommendation.domain.recommendation.repository import (
    RecommendationRepository,
)


@dataclass
class CreatedPlaceIntegrationEventSubscriber(IntegrationEventSubscriber[CreatedPlaceApplicationEvent]):
    """
    Subscription to CreatedPlaceApplicationEvent.
    Create a new recommendation
    """

    domain_event_bus: DomainEventBus
    recommendation_repository: RecommendationRepository

    async def handle_event(self, event: CreatedPlaceApplicationEvent):
        # FIXME: Move that logic to a command!

        place_view = PlaceViewProjection.from_entity(event.place_projection)
        recommendation = Recommendation.create(place=place_view)

        await self.recommendation_repository.create_recommendation(recommendation)
        await self.domain_event_bus.async_process_aggregate(recommendation)

    @classmethod
    def name(cls) -> str:
        return "place.created.to.recommendation"

    @classmethod
    def routing_key(cls) -> str:
        return "place.created"


@dataclass
class ReviewAddedIntegrationEventSubscriber(IntegrationEventSubscriber[ReviewAddedApplicationEvent]):
    """
    Subscription to ReviewAddedApplicationEvent.
    Pass through the recommendation layer to decide if it changes
    """

    domain_event_bus: DomainEventBus
    recommendation_repository: RecommendationRepository

    async def handle_event(self, event: ReviewAddedApplicationEvent):
        # FIXME: Move that logic to a command!

        recommendation = await self.recommendation_repository.find_recommendation_by_place_id(event.place_projection.id)

        recommendation.update_place(PlaceViewProjection.from_entity(event.place_projection))

        await self.recommendation_repository.update_place_view(recommendation)
        await self.domain_event_bus.async_process_aggregate(recommendation)

    @classmethod
    def name(cls) -> str:
        return "place.updated.review_added.to.recommendation"

    @classmethod
    def routing_key(cls) -> str:
        return "place.updated.review_added"
