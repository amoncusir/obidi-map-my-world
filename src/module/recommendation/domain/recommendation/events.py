from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.module.common.domain.events import DomainEvent
from src.module.recommendation.domain.recommendation.projections import (
    PlaceViewProjection,
)

if TYPE_CHECKING:
    from src.module.recommendation.domain.recommendation.recommendation import (
        Recommendation,
    )


@dataclass(frozen=True, kw_only=True)
class CreatedRecommendationDomainEvent(DomainEvent):
    recommendation: "Recommendation"


@dataclass(frozen=True, kw_only=True)
class UpdatedRecommendationDomainEvent(DomainEvent):
    recommendation: "Recommendation"


@dataclass(frozen=True, kw_only=True)
class UpdatedRecommendationPlaceViewDomainEvent(UpdatedRecommendationDomainEvent):
    old_place: PlaceViewProjection
    new_place: PlaceViewProjection


@dataclass(frozen=True, kw_only=True)
class UpdatedRecommendationScoreDomainEvent(UpdatedRecommendationDomainEvent):
    old_score: float
    new_score: float


@dataclass(frozen=True, kw_only=True)
class UpdatedRecommendationStateDomainEvent(UpdatedRecommendationDomainEvent):
    old_status: bool
    new_status: bool
