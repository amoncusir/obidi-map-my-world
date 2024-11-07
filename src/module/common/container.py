from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.module.common.application.domain_event_bus import DomainEventBus
from src.module.common.application.subscriber.domain_event import (
    LoggerDomainEventSubscriber,
)
from src.module.providers import DomainEventSubscriberProvider


class DomainEventSubscriber(DeclarativeContainer):

    logger_events = DomainEventSubscriberProvider(LoggerDomainEventSubscriber)


class CommonContainer(DeclarativeContainer):
    config = providers.Configuration()
    domain_event_bus = providers.Dependency(DomainEventBus)

    domain_event_subscriber = providers.Container(
        DomainEventSubscriber,
    )
