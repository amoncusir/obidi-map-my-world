from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class ManagerContainer(DeclarativeContainer):
    config = providers.Configuration()
