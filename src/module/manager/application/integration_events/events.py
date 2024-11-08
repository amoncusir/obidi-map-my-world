from src.module.common.application.event.integration import IntegrationEvent
from src.module.manager.domain.place.projections import (
    PlaceProjection,
    ReviewProjection,
)


class CreatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: PlaceProjection

    @classmethod
    def name(cls) -> str:
        return "place.created"


class UpdatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: PlaceProjection

    @classmethod
    def name(cls) -> str:
        return "place.updated"


class ReviewAddedApplicationEvent(UpdatedPlaceApplicationEvent):
    added_review: ReviewProjection

    @classmethod
    def name(cls) -> str:
        return "place.updated.review_added"
