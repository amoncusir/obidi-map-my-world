from dataclasses import dataclass
from typing import Tuple, Type

from src.module.common.domain.events import DomainEventSubscriber
from src.module.recommendation.domain.evaluator import (
    DisableIfPlaceIsUpdatedInLast30Days,
    ReviewCountScoreEvaluator,
    ScoreEvaluator,
    StateEvaluator,
)
from src.module.recommendation.domain.recommendation.events import (
    UpdatedRecommendationPlaceViewDomainEvent,
    UpdatedRecommendationScoreDomainEvent,
)
from src.module.recommendation.domain.recommendation.repository import (
    RecommendationRepository,
)


class UpdateScoreWhenPlaceIsUpdatedDomainSubscriber(DomainEventSubscriber[UpdatedRecommendationPlaceViewDomainEvent]):

    score_evaluators: Tuple[ScoreEvaluator] = (ReviewCountScoreEvaluator(),)

    @classmethod
    def event_type(cls) -> Type[UpdatedRecommendationPlaceViewDomainEvent]:
        return UpdatedRecommendationPlaceViewDomainEvent

    async def subscription_event(self, event: UpdatedRecommendationPlaceViewDomainEvent):
        recommendation = event.recommendation

        recommendation.calculate_score(list(self.score_evaluators))

        self._aggregate_events(recommendation)


class UpdateStatusWhenPlaceIsUpdatedDomainSubscriber(DomainEventSubscriber[UpdatedRecommendationPlaceViewDomainEvent]):

    status_evaluators: Tuple[StateEvaluator] = (DisableIfPlaceIsUpdatedInLast30Days(),)

    @classmethod
    def event_type(cls) -> Type[UpdatedRecommendationPlaceViewDomainEvent]:
        return UpdatedRecommendationPlaceViewDomainEvent

    async def subscription_event(self, event: UpdatedRecommendationPlaceViewDomainEvent):
        recommendation = event.recommendation

        recommendation.update_state(list(self.status_evaluators))

        self._aggregate_events(recommendation)


@dataclass
class SaveUpdatedScoreRecommendationIfDifferentDomainSubscriber(
    DomainEventSubscriber[UpdatedRecommendationScoreDomainEvent]
):
    recommendation_repository: RecommendationRepository

    @classmethod
    def event_type(cls) -> Type[UpdatedRecommendationScoreDomainEvent]:
        return UpdatedRecommendationScoreDomainEvent

    async def subscription_event(self, event: UpdatedRecommendationScoreDomainEvent):

        if event.old_score != event.new_score:
            await self.recommendation_repository.update_score(event.recommendation)
