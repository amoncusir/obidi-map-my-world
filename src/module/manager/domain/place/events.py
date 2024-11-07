from src.module.common.domain.events import DomainEvent
from src.module.manager.domain.place.projections import (
    NewReviewedPlaceProjection,
    PlaceProjection,
)


class CreatedPlaceDomainEvent(DomainEvent):
    new_place: PlaceProjection


class UpdatedPlaceDomainEvent(DomainEvent):
    pass


class ReviewAddedDomainEvent(UpdatedPlaceDomainEvent):
    new_review_place: NewReviewedPlaceProjection
