from pydantic import Field

from src.module.common.application.integration_events import IntegrationEvent


class ReviewAddedApplicationEvent(IntegrationEvent):
    place_id: str = Field(...)
    review_id: str = Field(...)
    review_rate: int = Field(...)

    @classmethod
    def name(cls) -> str:
        return "manager_place_review_added"
