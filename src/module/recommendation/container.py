from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class RecommendationContainer(DeclarativeContainer):
    config = providers.Configuration()
