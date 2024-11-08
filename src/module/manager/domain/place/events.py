from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.module.common.domain.events import DomainEvent

if TYPE_CHECKING:
    from src.module.manager.domain.place import Place
    from src.module.manager.domain.place.place import Review


@dataclass(frozen=True, kw_only=True)
class CreatedPlaceDomainEvent(DomainEvent):
    place: "Place"


@dataclass(frozen=True, kw_only=True)
class UpdatedPlaceDomainEvent(DomainEvent):
    place: "Place"


@dataclass(frozen=True, kw_only=True)
class ReviewAddedDomainEvent(UpdatedPlaceDomainEvent):
    added_review: "Review"
