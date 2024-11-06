from logging import getLogger
from typing import Type

from src.module.common.domain.events import DomainEvent, DomainEventSubscriber

logger = getLogger(__name__)


class LoggerDomainEventSubscriber(DomainEventSubscriber[DomainEvent]):

    @classmethod
    def event_type(cls) -> Type[DomainEvent]:
        return DomainEvent

    async def handle_event(self, event: DomainEvent):
        logger.debug(f"New event triggered: {event.__class__.__qualname__}")
