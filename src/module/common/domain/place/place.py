import uuid
from typing import List, Optional

from pydantic import Field
from typing_extensions import TypeVar

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.category import Category
from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.values import GenericUUID, Location

ReviewID = TypeVar("ReviewID", bound=uuid.UUID)


class Review(DomainEntity[ReviewID]):
    id: ReviewID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    rate: int


PlaceID = TypeVar("PlaceID", bound=uuid.UUID)


class Place(AggregateRoot[PlaceID]):
    id: PlaceID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    name: str
    location: Location
    category: Category
    _reviews: List[Review] = Field(default_factory=list)

    @property
    def last_review(self) -> Optional[Review]:
        return self._reviews[-1]

    def add_review(self, review: Review):
        self._reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self._reviews.copy()
