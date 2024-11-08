from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from pymongo.asynchronous.database import AsyncDatabase

from src.app.utils import list_providers
from src.module.common.application.event.domain_bus import DomainEventBus
from src.module.common.application.event.integration_bus import IntegrationEventsBus
from src.module.common.infrastructure.inmemory.domain_event_bus import (
    InMemoryDomainEventBus,
)
from src.module.providers import (
    DomainEventSubscriberProvider,
    IntegrationEventSubscriberProvider,
)
from src.module.recommendation.application.domain_event.handlers import (
    SaveUpdatedScoreRecommendationIfDifferentDomainSubscriber,
    UpdateScoreWhenPlaceIsUpdatedDomainSubscriber,
    UpdateStatusWhenPlaceIsUpdatedDomainSubscriber,
)
from src.module.recommendation.application.integration_event.handlers import (
    CreatedPlaceIntegrationEventSubscriber,
    ReviewAddedIntegrationEventSubscriber,
)
from src.module.recommendation.domain.recommendation.repository import (
    RecommendationRepository,
)
from src.module.recommendation.infrastructure.mongodb.recommendation_repository import (
    MongoDBRecommendationRepository,
)


class Repository(DeclarativeContainer):
    database = providers.Dependency(AsyncDatabase)

    mongo_recommendation_repository = providers.Singleton(
        MongoDBRecommendationRepository,
        database=database,
    )

    recommendation_repository = providers.Dependency(
        instance_of=RecommendationRepository, default=mongo_recommendation_repository
    )


class IntegrationEventSubscribers(DeclarativeContainer):
    domain_event_bus = providers.Dependency(DomainEventBus)
    repository = providers.DependenciesContainer()

    review_added_integration_subscriber = IntegrationEventSubscriberProvider(
        ReviewAddedIntegrationEventSubscriber,
        domain_event_bus=domain_event_bus,
        recommendation_repository=repository.recommendation_repository,
    )

    place_created_integration_subscriber = IntegrationEventSubscriberProvider(
        CreatedPlaceIntegrationEventSubscriber,
        domain_event_bus=domain_event_bus,
        recommendation_repository=repository.recommendation_repository,
    )


class DomainEventSubscribers(DeclarativeContainer):
    repository = providers.DependenciesContainer()

    update_score_when_place_is_updated = DomainEventSubscriberProvider(UpdateScoreWhenPlaceIsUpdatedDomainSubscriber)

    update_status_when_place_is_updated = DomainEventSubscriberProvider(UpdateStatusWhenPlaceIsUpdatedDomainSubscriber)

    save_updated_score_recommendation = DomainEventSubscriberProvider(
        SaveUpdatedScoreRecommendationIfDifferentDomainSubscriber,
        recommendation_repository=repository.recommendation_repository,
    )


class RecommendationContainer(DeclarativeContainer):
    config = providers.Configuration()
    database = providers.Dependency(AsyncDatabase)
    integration_event_bus = providers.Dependency(IntegrationEventsBus)

    __self__ = providers.Self()

    domain_event_bus = providers.Singleton(
        InMemoryDomainEventBus, subscribers=providers.Factory(list_providers, __self__, DomainEventSubscriberProvider)
    )

    repository = providers.Container(
        Repository,
        database=database,
    )

    domain_event_subscriber = providers.Container(
        DomainEventSubscribers,
        repository=repository,
    )

    integration_event_subscriber = providers.Container(IntegrationEventSubscribers, domain_event_bus=domain_event_bus)
