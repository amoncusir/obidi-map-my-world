from dataclasses import dataclass
from typing import Self, TypeVar

from src.module.common.domain.projections import EntityProjection
from src.module.common.domain.values import Location
from src.module.manager import PlaceProjection

PlaceID = TypeVar("PlaceID", bound=str)


@dataclass(frozen=True, kw_only=True)
class PlaceViewProjection(EntityProjection[PlaceID]):
    id: PlaceID
    name: str
    location: Location
    total_reviews: int

    @classmethod
    def from_entity(cls, entity: PlaceProjection) -> Self:
        return PlaceViewProjection(
            id=entity.id,
            projected_at=entity.projected_at,
            name=entity.name,
            location=entity.location,
            total_reviews=len(entity.reviews),
        )
