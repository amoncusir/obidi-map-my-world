from src.module.common.domain.events import DomainEvent
from src.module.manager.domain.place.projections import (
    NewPlaceProjection,
    NewReviewedPlaceProjection,
)


class CreatedPlaceDomainEvent(DomainEvent):
    new_place: NewPlaceProjection


class UpdatedPlaceDomainEvent(DomainEvent):
    pass


class ReviewAddedDomainEvent(UpdatedPlaceDomainEvent):
    new_review_place: NewReviewedPlaceProjection
