from src.module.manager.application.integration_events.events import (
    ReviewAddedApplicationEvent,
)


def manager_place_review_added_handler(event: ReviewAddedApplicationEvent): ...
