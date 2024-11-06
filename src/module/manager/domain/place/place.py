import uuid
from typing import List, Optional

from pydantic import Field
from typing_extensions import Self, TypeVar

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.projections import EntityProjection
from src.module.common.domain.values import GenericUUID, Location
from src.module.manager.domain.category import Category
from src.module.manager.domain.category.category import CategoryID

ReviewID = TypeVar("ReviewID", bound=uuid.UUID)


class Review(DomainEntity[ReviewID]):
    id: ReviewID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    rate: int = Field(ge=0, le=5)


PlaceID = TypeVar("PlaceID", bound=str)


class CategoryProjection(EntityProjection[CategoryID]):
    name: str

    @classmethod
    def from_entity(cls, entity: Category[CategoryID]) -> Self:
        return CategoryProjection(id=entity.id, created_at=entity.updated_at, name=entity.name)


class Place(AggregateRoot[PlaceID]):
    id: Optional[PlaceID] = Field(default=None, kw_only=True)
    name: str
    location: Location
    category: CategoryProjection
    reviews: List[Review] = Field(default_factory=list)

    @property
    def last_review(self) -> Optional[Review]:
        return self.reviews[-1]

    def add_review(self, review: Review):
        self.reviews.append(review)
        self._update()

    def get_reviews(self) -> List[Review]:
        return self.reviews.copy()
