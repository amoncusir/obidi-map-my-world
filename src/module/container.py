from itertools import chain
from typing import Any, List

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from pymongo.asynchronous.database import AsyncDatabase

from src.module.common.application.command_bus import CommandBus
from src.module.common.application.domain_event_bus import DomainEventBus
from src.module.geoquerier.container import GeoQuerierContainer
from src.module.manager.container import ManagerContainer
from src.module.providers import CommandHandlerProvider, DomainEventSubscriberProvider
from src.module.recommendation.container import RecommendationContainer


def list_providers(container: DeclarativeContainer, provider_type: Any):
    return [p() for p in container.traverse(types=[provider_type])]


class ModuleContainer(DeclarativeContainer):
    config = providers.Configuration()
    database = providers.Dependency(AsyncDatabase)
    __self__ = providers.Self()

    domain_event_bus = providers.Singleton(
        DomainEventBus, subscribers=providers.Singleton(list_providers, __self__, DomainEventSubscriberProvider)
    )

    command_bus = providers.Singleton(
        CommandBus, handlers=providers.Singleton(list_providers, __self__, CommandHandlerProvider)
    )

    manager_container = providers.Container(
        ManagerContainer,
        config=config.manager,
        database=database,
        domain_event_bus=domain_event_bus,
    )

    geo_querier_container = providers.Container(GeoQuerierContainer, config=config.geo_querier)
    recommendation_container = providers.Container(RecommendationContainer, config=config.recommendation)
