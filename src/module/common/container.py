from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.module.common.application.event.domain_bus import DomainEventBus


class DomainEventSubscriber(DeclarativeContainer):
    pass


class CommonContainer(DeclarativeContainer):
    config = providers.Configuration()
    domain_event_bus = providers.Dependency(DomainEventBus)

    domain_event_subscriber = providers.Container(
        DomainEventSubscriber,
    )
