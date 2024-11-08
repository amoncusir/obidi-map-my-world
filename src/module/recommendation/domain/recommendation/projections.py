from dataclasses import dataclass
from typing import Self

from src.module.common.domain.projections import EntityProjection
from src.module.common.domain.values import Location
from src.module.manager import PlaceProjection


@dataclass(frozen=True, kw_only=True)
class PlaceViewProjection(EntityProjection[str]):
    id: str
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
