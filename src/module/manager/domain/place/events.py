from src.module.common.domain.events import DomainEvent
from src.module.manager.domain.place.projections import (
    PlaceProjection,
    ReviewProjection,
)


class CreatedPlaceDomainEvent(DomainEvent):
    new_place: PlaceProjection


class UpdatedPlaceDomainEvent(DomainEvent):
    place_projection: PlaceProjection


class ReviewAddedDomainEvent(UpdatedPlaceDomainEvent):
    added_review: ReviewProjection
