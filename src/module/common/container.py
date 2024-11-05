from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class CommonContainer(DeclarativeContainer):
    config = providers.Configuration()
