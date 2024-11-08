from src.module.common.domain.events import DomainEvent
from src.module.recommendation.domain.recommendation.recommendation import (
    PlaceView,
    Recommendation,
)


class CreatedRecommendationDomainEvent(DomainEvent):
    recommendation: Recommendation


class UpdatedRecommendationDomainEvent(DomainEvent):
    recommendation: Recommendation


class UpdatedRecommendationPlaceViewDomainEvent(UpdatedRecommendationDomainEvent):
    old_place: PlaceView
    new_place: PlaceView


class UpdatedRecommendationScoreDomainEvent(UpdatedRecommendationDomainEvent):
    old_score: float
    new_score: float
