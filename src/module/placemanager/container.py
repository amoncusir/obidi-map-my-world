from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class PlaceManagerContainer(DeclarativeContainer):
    config = providers.Configuration()
