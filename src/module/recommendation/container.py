from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.module.providers import IntegrationEventSubscriberProvider
from src.module.recommendation.application.integration_events.handlers import (
    ReviewAddedIntegrationEventSubscriber,
)


class IntegrationEventSubscribers(DeclarativeContainer):
    review_added_integration_subscriber = IntegrationEventSubscriberProvider(ReviewAddedIntegrationEventSubscriber)


class RecommendationContainer(DeclarativeContainer):
    config = providers.Configuration()

    integration_event_subscriber = providers.Container(
        IntegrationEventSubscribers,
    )
