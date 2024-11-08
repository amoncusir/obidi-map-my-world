from datetime import datetime
from typing import TYPE_CHECKING, Self

from src.module.common.domain.projections import EntityProjection
from src.module.common.domain.values import Location
from src.module.manager.domain.category.projections import CategoryProjection

if TYPE_CHECKING:
    from src.module.manager.domain.place.place import Place, Review


class ReviewProjection(EntityProjection[str]):
    id: str
    rate: int

    @classmethod
    def from_entity(cls, entity: "Review") -> Self:
        return ReviewProjection(id=str(entity.id), created_at=entity.updated_at, rate=entity.rate)


class PlaceProjection(EntityProjection[str]):
    id: str
    created_at: datetime
    name: str
    location: Location
    category: CategoryProjection
    reviews: list[ReviewProjection]

    @classmethod
    def from_entity(cls, entity: "Place") -> Self:
        return PlaceProjection(
            id=str(entity.id),
            created_at=entity.updated_at,
            name=entity.name,
            location=entity.location,
            category=entity.category,
            reviews=[ReviewProjection.from_entity(r) for r in entity.reviews],
        )
