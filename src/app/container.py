from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from faststream.rabbit import RabbitRouter

from src.app.api import build_fastapi
from src.app.fast_stream import build_app, build_broker, build_exchange, build_router
from src.app.utils import list_providers
from src.app.worker import build_celery
from src.config.celery import CelerySettings
from src.config.fast_stream import FastStreamSettings
from src.config.mongodb import MongoDBSettings
from src.module.common.infrastructure import mongodb
from src.module.container import ModuleContainer
from src.module.providers import IntegrationEventSubscriberProvider


class CeleryContainer(DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Factory(
        CelerySettings,
        broker_url=config.broker_url,
    )

    celery = providers.Singleton(build_celery, settings=settings)


class FastStream(DeclarativeContainer):
    config = providers.Configuration()
    router = providers.Dependency(RabbitRouter)

    settings = providers.Factory(
        FastStreamSettings,
        url=config.url,
        app_id=config.app_id,
        exchange_name=config.exchange_name,
    )

    broker = providers.Singleton(
        build_broker,
        settings=settings,
        router=router,
    )

    app = providers.Singleton(
        build_app,
        broker=broker,
    )

    exchange = providers.Singleton(
        build_exchange,
        settings=settings,
    )


class MongoContainer(DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Factory(MongoDBSettings, url=config.url.required(), database=config.database)
    client = providers.Factory(mongodb.build_client, settings=settings)
    database = providers.Factory(mongodb.get_database, client=client, settings=settings)


class MainContainer(DeclarativeContainer):
    config = providers.Configuration()

    __self__ = providers.Self()

    faststream_router = providers.Singleton(
        build_router, subscribers=providers.Factory(list_providers, __self__, IntegrationEventSubscriberProvider)
    )

    celery = providers.Container(CeleryContainer, config=config.celery)
    faststream = providers.Container(FastStream, config=config.faststream, router=faststream_router)
    mongodb = providers.Container(MongoContainer, config=config.mongodb)

    api = providers.Singleton(
        build_fastapi,
        title=config.name,
        debug=config.debug.as_(bool),
    )

    module_container = providers.Container(
        ModuleContainer,
        config=config.module,
        database=mongodb.database,
        celery=celery.celery,
        rabbit_broker=faststream.broker,
        rabbit_exchange=faststream.exchange,
    )
