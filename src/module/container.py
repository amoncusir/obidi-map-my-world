from celery import Celery
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
    RabbitRoute,
    RabbitRouter,
)
from pymongo.asynchronous.database import AsyncDatabase

from src.app.utils import list_providers
from src.module.common.container import CommonContainer
from src.module.common.infrastructure.faststream.integration_events_bus import (
    FastStreamIntegrationEventsBus,
)
from src.module.common.infrastructure.inmemory.command_bus import InMemoryCommandBus
from src.module.common.infrastructure.inmemory.domain_event_bus import (
    InMemoryDomainEventBus,
)
from src.module.geoquerier.container import GeoQuerierContainer
from src.module.manager.container import ManagerContainer
from src.module.providers import CommandHandlerProvider, DomainEventSubscriberProvider
from src.module.recommendation.container import RecommendationContainer


class ModuleContainer(DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Dependency(AsyncDatabase)
    celery = providers.Dependency(Celery)
    rabbit_broker = providers.Dependency(RabbitBroker)
    rabbit_exchange = providers.Dependency(RabbitExchange)

    __self__ = providers.Self()

    domain_event_bus = providers.Singleton(
        InMemoryDomainEventBus, subscribers=providers.Factory(list_providers, __self__, DomainEventSubscriberProvider)
    )

    command_bus = providers.Singleton(
        InMemoryCommandBus, handlers=providers.Factory(list_providers, __self__, CommandHandlerProvider)
    )

    integration_event_bus = providers.Singleton(
        FastStreamIntegrationEventsBus, broker=rabbit_broker, exchange=rabbit_exchange
    )

    common_container = providers.Container(
        CommonContainer,
        domain_event_bus=domain_event_bus,
    )

    manager_container = providers.Container(
        ManagerContainer,
        config=config.manager,
        database=database,
        domain_event_bus=domain_event_bus,
        integration_event_bus=integration_event_bus,
    )

    recommendation_container = providers.Container(RecommendationContainer, config=config.recommendation)

    geo_querier_container = providers.Container(GeoQuerierContainer, config=config.geo_querier)
