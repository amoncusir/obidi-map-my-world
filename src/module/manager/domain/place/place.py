import uuid
from typing import List, Optional

from pydantic import Field
from typing_extensions import TypeVar

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.values import GenericUUID, Location
from src.module.manager.domain.category import Category

ReviewID = TypeVar("ReviewID", bound=uuid.UUID)


class Review(DomainEntity[ReviewID]):
    id: ReviewID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    rate: int


PlaceID = TypeVar("PlaceID", bound=str)


class Place(AggregateRoot[PlaceID]):
    id: Optional[PlaceID] = Field(default=None, kw_only=True)
    name: str
    location: Location
    category: Category
    reviews: List[Review] = Field(default_factory=list)

    @property
    def last_review(self) -> Optional[Review]:
        return self.reviews[-1]

    def add_review(self, review: Review):
        self.reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self.reviews.copy()
