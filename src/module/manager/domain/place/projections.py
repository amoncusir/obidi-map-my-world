from datetime import datetime
from typing import Self

from src.module.common.domain.projections import EntityProjection
from src.module.manager.domain.category.projections import CategoryProjection
from src.module.manager.domain.place.place import Place, PlaceID, Review


class ReviewProjection(EntityProjection[str]):
    id: str
    rate: int

    @classmethod
    def from_entity(cls, entity: Review) -> Self:
        return ReviewProjection(id=str(entity.id), created_at=entity.updated_at, rate=entity.rate)


class NewReviewedPlaceProjection(EntityProjection[PlaceID]):
    id: PlaceID
    added_review: ReviewProjection

    @classmethod
    def from_entity(cls, entity: Place) -> Self:
        return NewReviewedPlaceProjection(
            id=str(entity.id),
            created_at=entity.updated_at,
            added_review=ReviewProjection.from_entity(entity.last_review),
        )


class NewPlaceProjection(EntityProjection[PlaceID]):
    id: PlaceID
    created_at: datetime
    name: str
    category: CategoryProjection

    @classmethod
    def from_entity(cls, entity: Place) -> Self:
        return NewPlaceProjection(
            id=str(entity.id), created_at=entity.created_at, name=entity.name, category=entity.category
        )
