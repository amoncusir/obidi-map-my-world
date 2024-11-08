import uuid
from typing import List, Optional, Self

from pydantic import Field
from typing_extensions import TypeVar

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.values import GenericUUID, Location
from src.module.manager.domain.category import Category
from src.module.manager.domain.place.events import (
    CreatedPlaceDomainEvent,
    ReviewAddedDomainEvent,
)

ReviewID = TypeVar("ReviewID", bound=uuid.UUID)
PlaceID = TypeVar("PlaceID", bound=str)


class Review(DomainEntity[ReviewID]):
    id: ReviewID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    rate: int = Field(ge=0, le=5)


class Place(AggregateRoot[PlaceID]):
    id: Optional[PlaceID] = Field(kw_only=True)
    name: str
    location: Location
    category: Category
    reviews: List[Review] = Field(default_factory=list)

    @classmethod
    def create_place(cls, *, name: str, location: Location, category: Category) -> Self:
        """
        To avoid the creation of Factories, I decide to use a class member functions to handle the logic of the
        factory creation process, but in more complex domains, they will be a must.
        """

        place = Place(id=None, name=name, location=location, category=category)

        place._add_event(CreatedPlaceDomainEvent(place=place.duplicate()))

        return place

    @property
    def last_review(self) -> Optional[Review]:
        return self.reviews[-1]

    def add_review(self, review: Review):
        self.reviews.append(review)
        self._update()

        self._add_event(
            ReviewAddedDomainEvent(
                place=self.duplicate(),
                added_review=review.duplicate(),
            )
        )

    def get_reviews(self) -> List[Review]:
        return [r.model_copy(deep=True) for r in self.reviews]
