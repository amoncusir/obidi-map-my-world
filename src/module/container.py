from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.module.common.container import CommonContainer
from src.module.geoquerier.container import GeoQuerierContainer
from src.module.placemanager.container import PlaceManagerContainer
from src.module.recommendation.container import RecommendationContainer


class ModuleContainer(DeclarativeContainer):
    config = providers.Configuration()

    common_container = providers.Container(CommonContainer, config=config.common)

    geo_querier_container = providers.Container(GeoQuerierContainer, config=config.geo_querier)

    place_manager_container = providers.Container(PlaceManagerContainer, config=config.place_manager)

    recommendation_container = providers.Container(RecommendationContainer, config=config.recommendation)