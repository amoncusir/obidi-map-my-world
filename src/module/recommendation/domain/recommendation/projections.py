from typing import Self, TypeVar

from pydantic import Field

from src.module.common.domain.projections import EntityProjection
from src.module.common.domain.values import Location
from src.module.manager import PlaceProjection

PlaceID = TypeVar("PlaceID", bound=str)


class PlaceViewProjection(EntityProjection[PlaceID]):
    id: PlaceID = Field(..., kw_only=True)
    name: str = Field(..., kw_only=True)
    location: Location = Field(..., kw_only=True)
    total_reviews: int = Field(..., kw_only=True)

    @classmethod
    def from_entity(cls, entity: PlaceProjection) -> Self:
        return PlaceViewProjection(
            id=entity.id,
            projected_at=entity.projected_at,
            name=entity.name,
            location=entity.location,
            total_reviews=len(entity.reviews),
        )
