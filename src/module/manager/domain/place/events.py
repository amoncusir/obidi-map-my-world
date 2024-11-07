from src.module.common.domain.events import DomainEvent
from src.module.manager.domain.place.projections import (
    NewPlaceProjection,
    NewReviewedPlaceProjection,
)


class CreatedPlaceDomainEvent(DomainEvent):
    projection: NewPlaceProjection


class UpdatedPlaceDomainEvent(DomainEvent):
    pass


class ReviewAddedDomainEvent(UpdatedPlaceDomainEvent):
    projection: NewReviewedPlaceProjection
