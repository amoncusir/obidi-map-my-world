from pydantic import Field

from src.module.common.application.integration_events import IntegrationEvent
from src.module.manager.domain.place.projections import (
    NewPlaceProjection,
    NewReviewedPlaceProjection,
)


class CreatedPlaceApplicationEvent(IntegrationEvent):
    place_projection: NewPlaceProjection

    @classmethod
    def name(cls) -> str:
        return "manager_place_created"


class ReviewAddedApplicationEvent(IntegrationEvent):
    new_review_place: NewReviewedPlaceProjection

    @classmethod
    def name(cls) -> str:
        return "manager_place_review_added"
