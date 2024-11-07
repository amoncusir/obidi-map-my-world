from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.api import build_fastapi
from src.app.worker import build_celery
from src.config.celery import CelerySettings
from src.config.mongodb import MongoDBSettings
from src.module.common.infrastructure import mongodb
from src.module.container import ModuleContainer


class CeleryContainer(DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Factory(
        CelerySettings,
        broker_url=config.broker_url,
    )

    celery = providers.Singleton(build_celery, settings=settings)


class MongoContainer(DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(MongoDBSettings, url=config.url.required(), database=config.database)

    client = providers.Factory(mongodb.build_client, settings=settings)

    database = providers.Factory(mongodb.get_database, client=client, settings=settings)


class MainContainer(DeclarativeContainer):
    config = providers.Configuration()

    celery = providers.Container(CeleryContainer, config=config.celery)

    mongodb = providers.Container(
        MongoContainer,
        config=config.mongodb,
    )

    api = providers.Singleton(
        build_fastapi,
        title=config.name,
        debug=config.debug.as_(bool),
    )

    module_container = providers.Container(
        ModuleContainer,
        config=config.module,
        database=mongodb.database,
    )
