from typing import TYPE_CHECKING

from src.module.common.domain.events import DomainEvent
from src.module.recommendation.domain.recommendation.projections import (
    PlaceViewProjection,
)

if TYPE_CHECKING:
    from src.module.recommendation.domain.recommendation.recommendation import (
        Recommendation,
    )


class CreatedRecommendationDomainEvent(DomainEvent):
    recommendation: "Recommendation"


class UpdatedRecommendationDomainEvent(DomainEvent):
    recommendation: "Recommendation"


class UpdatedRecommendationPlaceViewDomainEvent(UpdatedRecommendationDomainEvent):
    old_place: PlaceViewProjection
    new_place: PlaceViewProjection


class UpdatedRecommendationScoreDomainEvent(UpdatedRecommendationDomainEvent):
    old_score: float
    new_score: float


class UpdatedRecommendationStateDomainEvent(UpdatedRecommendationDomainEvent):
    old_status: bool
    new_status: bool
