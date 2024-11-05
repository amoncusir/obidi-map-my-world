from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class GeoQuerierContainer(DeclarativeContainer):
    config = providers.Configuration()
