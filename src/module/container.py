from itertools import chain
from typing import Any, List

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from pymongo.asynchronous.database import AsyncDatabase

from src.module.common.application.command_bus import CommandBus
from src.module.geoquerier.container import GeoQuerierContainer
from src.module.manager.container import ManagerContainer
from src.module.recommendation.container import RecommendationContainer


def plain_list(*lists: List[Any]) -> List[Any]:
    return list(chain.from_iterable(lists))


class ModuleContainer(DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Dependency(AsyncDatabase)

    manager_container = providers.Container(
        ManagerContainer,
        config=config.manager,
        database=database,
    )

    geo_querier_container = providers.Container(GeoQuerierContainer, config=config.geo_querier)
    recommendation_container = providers.Container(RecommendationContainer, config=config.recommendation)

    command_bus = providers.Singleton(
        CommandBus, handlers=providers.Factory(plain_list, manager_container.list_commands)
    )
