from src.module.common.domain.events import DomainEvent
from src.module.manager.domain.place import Place
from src.module.manager.domain.place.place import Review


class CreatedPlaceDomainEvent(DomainEvent):
    place: Place


class UpdatedPlaceDomainEvent(DomainEvent):
    place: Place


class ReviewAddedDomainEvent(UpdatedPlaceDomainEvent):
    added_review: Review
