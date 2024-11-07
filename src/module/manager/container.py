from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from pymongo.asynchronous.database import AsyncDatabase

from src.module.common.application.event.domain_bus import DomainEventBus
from src.module.common.application.event.integration_bus import IntegrationEventsBus
from src.module.manager.application.command import CreatePlaceCommandHandler
from src.module.manager.application.command.add_review_on_place import (
    AddReviewOnPlaceCommandHandler,
)
from src.module.manager.application.command.create_category import (
    CreateCategoryCommandHandler,
)
from src.module.manager.application.domain_event.create_place import (
    PublishEventWhenCreatedPlaceDomainSubscriber,
)
from src.module.manager.application.domain_event.review_added import (
    PublishEventWhenReviewAddedDomainSubscriber,
)
from src.module.manager.domain.category import CategoryRepository
from src.module.manager.domain.place import PlaceRepository
from src.module.manager.infrastructure.mongodb.category_repository import (
    MongoCategoryRepository,
)
from src.module.manager.infrastructure.mongodb.place_repository import (
    MongoPlaceRepository,
)
from src.module.providers import CommandHandlerProvider, DomainEventSubscriberProvider


class Repository(DeclarativeContainer):
    database = providers.Dependency(AsyncDatabase)

    mongo_place_repository = providers.Singleton(
        MongoPlaceRepository,
        database=database,
    )

    mongo_category_repository = providers.Singleton(
        MongoCategoryRepository,
        database=database,
    )

    place_repository = providers.Dependency(instance_of=PlaceRepository, default=mongo_place_repository)
    category_repository = providers.Dependency(instance_of=CategoryRepository, default=mongo_category_repository)


class DomainEventSubscriber(DeclarativeContainer):
    integration_event_bus = providers.Dependency(IntegrationEventsBus)

    publish_event_created_place = DomainEventSubscriberProvider(
        PublishEventWhenCreatedPlaceDomainSubscriber, integration_event_bus=integration_event_bus
    )

    publish_event_review_added = DomainEventSubscriberProvider(
        PublishEventWhenReviewAddedDomainSubscriber, integration_event_bus=integration_event_bus
    )


class Command(DeclarativeContainer):
    repository = providers.DependenciesContainer()
    domain_event_bus = providers.Dependency(DomainEventBus)

    create_category = CommandHandlerProvider(
        CreateCategoryCommandHandler, category_repository=repository.category_repository
    )

    create_place = CommandHandlerProvider(
        CreatePlaceCommandHandler,
        category_repository=repository.category_repository,
        place_repository=repository.place_repository,
        domain_event_bus=domain_event_bus,
    )

    add_review_on_place = CommandHandlerProvider(
        AddReviewOnPlaceCommandHandler, place_repository=repository.place_repository, domain_event_bus=domain_event_bus
    )


class ManagerContainer(DeclarativeContainer):
    config = providers.Configuration()
    database = providers.Dependency(AsyncDatabase)
    domain_event_bus = providers.Dependency(DomainEventBus)
    integration_event_bus = providers.Dependency(IntegrationEventsBus)

    repository = providers.Container(
        Repository,
        database=database,
    )

    domain_event_subscriber = providers.Container(
        DomainEventSubscriber,
        integration_event_bus=integration_event_bus,
    )

    command = providers.Container(
        Command,
        repository=repository,
        domain_event_bus=domain_event_bus,
    )
