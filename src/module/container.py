from itertools import chain
from typing import Any, List

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.module.common.container import CommonContainer
from src.module.geoquerier.container import GeoQuerierContainer
from src.module.manager.container import ManagerContainer
from src.module.recommendation.container import RecommendationContainer


def plain_list(*lists: List[Any]) -> List[Any]:
    return list(chain.from_iterable(lists))


class ModuleContainer(DeclarativeContainer):
    config = providers.Configuration()

    common_container = providers.Container(CommonContainer, config=config.common)

    geo_querier_container = providers.Container(GeoQuerierContainer, config=config.geo_querier)

    manager_container = providers.Container(ManagerContainer, config=config.manager)

    recommendation_container = providers.Container(RecommendationContainer, config=config.recommendation)

    commands = providers.Factory(plain_list, manager_container.list_commands)
