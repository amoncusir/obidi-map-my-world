from src.module.common.application.event.integration import IntegrationEvent
from src.module.manager.domain.place.projections import (
    NewPlaceProjection,
    NewReviewedPlaceProjection,
)


class CreatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: NewPlaceProjection

    @classmethod
    def name(cls) -> str:
        return "manager.place.created"


class ReviewAddedApplicationEvent(IntegrationEvent):
    new_review_place: NewReviewedPlaceProjection

    @classmethod
    def name(cls) -> str:
        return "manager.place.review_added"
