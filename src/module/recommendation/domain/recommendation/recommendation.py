from typing import List, Optional, TypeVar

from pydantic import Field, ValidationError

from src.module.common.domain.aggregates import AggregateRoot
from src.module.recommendation.domain.evaluator import ScoreEvaluator, StateEvaluator
from src.module.recommendation.domain.recommendation.events import (
    CreatedRecommendationDomainEvent,
    UpdatedRecommendationPlaceViewDomainEvent,
    UpdatedRecommendationScoreDomainEvent,
    UpdatedRecommendationStateDomainEvent,
)
from src.module.recommendation.domain.recommendation.projections import (
    PlaceViewProjection,
)
from src.module.recommendation.domain.recommendation.rules import (
    TotalWeightScoreMustBeGraterThanZero,
    UpdatedPlaceMustBeNewer,
    UpdatedPlaceMustBeSameID,
)
from src.module.recommendation.domain.values import Score

RecommendationID = TypeVar("RecommendationID", bound=str)


class Recommendation(AggregateRoot[RecommendationID]):
    id: Optional[RecommendationID] = Field(..., kw_only=True)
    place: PlaceViewProjection = Field(None, kw_only=True)
    score: Score = Field(None, ge=0, le=1)
    state: bool = Field(False, kw_only=True)

    @property
    def is_enabled(self) -> bool:
        return self.state

    @classmethod
    def create(cls, *, place: PlaceViewProjection):
        aggregate = Recommendation(
            id=None,
        )

        aggregate._add_event(
            CreatedRecommendationDomainEvent(
                recommendation=aggregate.duplicate(),
            )
        )

        aggregate.update_place(place)

        return aggregate

    def update_place(self, place: PlaceViewProjection):
        if place is None:
            raise ValidationError("place cannot be None")

        current_place = self.place

        UpdatedPlaceMustBeSameID.spark(
            current_place=current_place,
            new_place=place,
        )

        UpdatedPlaceMustBeNewer.spark(
            current_place=current_place,
            new_place=place,
        )

        self.place = place
        self._update()

        self._add_event(
            UpdatedRecommendationPlaceViewDomainEvent(
                recommendation=self.duplicate(),
                old_place=current_place if current_place is not None else None,
                new_place=self.place,
            )
        )

    def calculate_score(self, evaluators: List[ScoreEvaluator]):
        if self.place is None:
            raise ValidationError("place cannot be None")

        if len(evaluators) == 0:
            return

        current_score = self.score
        rates = [e.evaluate(self.place) for e in evaluators]

        weighted_sum = sum(score * weight for score, weight in rates)
        total_weight = sum(weight for _, weight in rates)

        TotalWeightScoreMustBeGraterThanZero.spark(total_weight=total_weight)

        final_score = weighted_sum / total_weight

        self.score = Score(final_score)
        self._update()

        self._add_event(
            UpdatedRecommendationScoreDomainEvent(
                recommendation=self.duplicate(), old_score=current_score, new_score=self.score
            )
        )

    def update_state(self, evaluators: List[StateEvaluator]):
        if self.place is None:
            raise ValidationError("place cannot be None")

        if len(evaluators) == 0:
            return

        current_state = self.state

        evaluations = {e.evaluate(self.place) for e in evaluators}

        self.state = False in evaluations
        self._update()

        self._add_event(
            UpdatedRecommendationStateDomainEvent(
                recommendation=self.duplicate(), old_status=current_state, new_status=self.state
            )
        )
