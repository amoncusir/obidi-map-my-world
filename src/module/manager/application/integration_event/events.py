from dataclasses import dataclass
from typing import Any, Dict, Self

from src.module.common.application.event.integration import IntegrationEvent
from src.module.manager.application.projections.place import (
    PlaceProjection,
    ReviewProjection,
)


@dataclass(frozen=True, kw_only=True)
class CreatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: PlaceProjection

    @classmethod
    def name(cls) -> str:
        return "place.created"


@dataclass(frozen=True, kw_only=True)
class UpdatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: PlaceProjection

    @classmethod
    def name(cls) -> str:
        return "place.updated"


@dataclass(frozen=True, kw_only=True)
class ReviewAddedApplicationEvent(UpdatedPlaceApplicationEvent):
    added_review: ReviewProjection

    @classmethod
    def name(cls) -> str:
        return "place.updated.review_added"
