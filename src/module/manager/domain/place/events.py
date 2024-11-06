from src.module.common.domain.events import DomainEvent
from src.module.manager.domain.place.projections import (
    NewPlaceProjection,
    NewReviewedPlaceProjection,
)


class ReviewAddedDomainEvent(DomainEvent):
    projection: NewReviewedPlaceProjection


class CreatedPlaceDomainEvent(DomainEvent):
    projection: NewPlaceProjection
