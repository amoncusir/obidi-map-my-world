from typing import TYPE_CHECKING, Self

from src.module.common.domain.projections import EntityProjection

if TYPE_CHECKING:
    from src.module.common.domain.values import Location
    from src.module.manager import CategoryProjection
    from src.module.manager.domain.place import Place
    from src.module.manager.domain.place.place import Review


class ReviewProjection(EntityProjection[str]):
    id: str
    rate: int

    @classmethod
    def from_entity(cls, entity: "Review") -> Self:
        return ReviewProjection(id=str(entity.id), projected_at=entity.updated_at, rate=entity.rate)


class PlaceProjection(EntityProjection[str]):
    id: str
    name: str
    location: Location
    category: CategoryProjection
    reviews: list[ReviewProjection]

    @classmethod
    def from_entity(cls, entity: "Place") -> Self:
        return PlaceProjection(
            id=str(entity.id),
            projected_at=entity.updated_at,
            name=entity.name,
            location=entity.location,
            category=entity.category,
            reviews=[ReviewProjection.from_entity(r) for r in entity.reviews],
        )