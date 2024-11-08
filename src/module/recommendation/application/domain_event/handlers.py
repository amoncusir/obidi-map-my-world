from dataclasses import dataclass
from typing import Type

from src.module.common.domain.events import DomainEventSubscriber
from src.module.recommendation.domain.recommendation.events import (
    UpdatedRecommendationPlaceViewDomainEvent,
    UpdatedRecommendationScoreDomainEvent,
)
from src.module.recommendation.domain.recommendation.repository import (
    RecommendationRepository,
)


@dataclass
class UpdateScoreWhenPlaceIsUpdatedDomainSubscriber(DomainEventSubscriber[UpdatedRecommendationPlaceViewDomainEvent]):

    @classmethod
    def event_type(cls) -> Type[UpdatedRecommendationPlaceViewDomainEvent]:
        return UpdatedRecommendationPlaceViewDomainEvent

    async def subscription_event(self, event: UpdatedRecommendationPlaceViewDomainEvent):
        recommendation = event.recommendation

        recommendation.calculate_score([])

        self._aggregate_events(recommendation)


@dataclass
class UpdateIfIsRecommendableWhenPlaceIsUpdatedDomainSubscriber(
    DomainEventSubscriber[UpdatedRecommendationPlaceViewDomainEvent]
):

    @classmethod
    def event_type(cls) -> Type[UpdatedRecommendationPlaceViewDomainEvent]:
        return UpdatedRecommendationPlaceViewDomainEvent

    async def subscription_event(self, event: UpdatedRecommendationPlaceViewDomainEvent):
        recommendation = event.recommendation

        # recommendation.calculate_score([])

        self._aggregate_events(recommendation)


class SaveUpdatedScoreRecommendationIfIsDifferentDomainSubscriber(
    DomainEventSubscriber[UpdatedRecommendationScoreDomainEvent]
):

    recommendation_repository: RecommendationRepository

    @classmethod
    def event_type(cls) -> Type[UpdatedRecommendationScoreDomainEvent]:
        return UpdatedRecommendationScoreDomainEvent

    async def subscription_event(self, event: UpdatedRecommendationScoreDomainEvent):

        if event.old_score != event.new_score:
            await self.recommendation_repository.update_score(event.recommendation)
