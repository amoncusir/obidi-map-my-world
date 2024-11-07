from src.module.common.application.event.integration import IntegrationEvent
from src.module.manager.domain.place.projections import (
    NewReviewedPlaceProjection,
    PlaceProjection,
)


class CreatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: PlaceProjection

    @classmethod
    def name(cls) -> str:
        return "manager.place.created"


class UpdatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: PlaceProjection

    @classmethod
    def name(cls) -> str:
        return "manager.place.updated"


class ReviewAddedApplicationEvent(UpdatedPlaceApplicationEvent):
    new_review_place: NewReviewedPlaceProjection

    @classmethod
    def name(cls) -> str:
        return "manager.place.updated.review_added"
