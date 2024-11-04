from typing import List, Optional

from pydantic import Field

from src.module.common.domain.entities import Category, DomainEntity, Review
from src.module.common.domain.values import Location


class AggregateRoot(DomainEntity):
    pass


class Place(AggregateRoot):
    name: str
    location: Location
    category: Category
    reviews: List[Review] = Field(default_factory=list)

    @property
    def last_review(self) -> Optional[Review]:
        return self.reviews[-1]

    def add_review(self, review: Review):
        self.reviews.append(review)
