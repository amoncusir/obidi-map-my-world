from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from faststream.rabbit import RabbitBroker, RabbitExchange
from pymongo.asynchronous.database import AsyncDatabase

from src.app.utils import list_providers
from src.module.common.infrastructure.faststream.integration_events_bus import (
    FastStreamIntegrationEventsBus,
)
from src.module.common.infrastructure.inmemory.command_bus import InMemoryCommandBus
from src.module.geoquerier.container import GeoQuerierContainer
from src.module.manager.container import ManagerContainer
from src.module.providers import CommandHandlerProvider
from src.module.recommendation.container import RecommendationContainer


class ModuleContainer(DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Dependency(AsyncDatabase)
    rabbit_broker = providers.Dependency(RabbitBroker)
    rabbit_exchange = providers.Dependency(RabbitExchange)

    __self__ = providers.Self()

    command_bus = providers.Singleton(
        InMemoryCommandBus, handlers=providers.Factory(list_providers, __self__, CommandHandlerProvider)
    )

    integration_event_bus = providers.Singleton(
        FastStreamIntegrationEventsBus, broker=rabbit_broker, exchange=rabbit_exchange
    )

    manager_container = providers.Container(
        ManagerContainer,
        config=config.manager,
        database=database,
        integration_event_bus=integration_event_bus,
    )

    recommendation_container = providers.Container(RecommendationContainer, config=config.recommendation)

    geo_querier_container = providers.Container(GeoQuerierContainer, config=config.geo_querier)
