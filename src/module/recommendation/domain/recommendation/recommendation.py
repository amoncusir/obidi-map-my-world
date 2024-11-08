from datetime import datetime
from typing import List, Optional, TypeVar

from pydantic import Field, ValidationError

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.values import Location
from src.module.recommendation.domain.evaluator import ScoreEvaluator
from src.module.recommendation.domain.recommendation.events import (
    CreatedRecommendationDomainEvent,
    UpdatedRecommendationPlaceViewDomainEvent,
    UpdatedRecommendationScoreDomainEvent,
)
from src.module.recommendation.domain.recommendation.rules import (
    TotalWeightScoreMustBeGraterThanZero,
    UpdatedPlaceMustBeNewer,
    UpdatedPlaceMustBeSameID,
)
from src.module.recommendation.domain.recommendation.values import Score

RecommendationID = TypeVar("RecommendationID", bound=str)
PlaceID = TypeVar("PlaceID", bound=str)


class PlaceView(DomainEntity[PlaceID]):
    id: PlaceID = Field(..., kw_only=True)
    name: str = Field(..., kw_only=True)
    last_update: datetime = Field(..., kw_only=True)
    location: Location
    total_reviews: int


class Recommendation(AggregateRoot[RecommendationID]):
    id: Optional[RecommendationID] = Field(..., kw_only=True)
    place: PlaceView = Field(..., kw_only=True)
    score: Score = Field(None, ge=0, le=1)

    @classmethod
    def create(cls, *, place: PlaceView):
        aggregate = cls(
            id=None,
            place=None,
        )

        aggregate._add_event(
            CreatedRecommendationDomainEvent(
                recommendation=aggregate.duplicate(),
            )
        )

        aggregate.update_place(place)

        return aggregate

    def update_place(self, place: PlaceView):
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
                old_place=current_place.duplicate(),
                new_place=self.place.duplicate(),
            )
        )

    def calculate_score(self, evaluators: List[ScoreEvaluator]):
        if self.place is None:
            raise ValidationError("place cannot be None")

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
