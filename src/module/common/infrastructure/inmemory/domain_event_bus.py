import logging
from asyncio import TaskGroup
from functools import singledispatchmethod
from logging import getLogger
from typing import List, Type

from src.module.common.application.event.domain_bus import DomainEventBus
from src.module.common.domain.events import DomainEvent, DomainEventSubscriber

logger = getLogger(__name__)


class InMemoryDomainEventBus(DomainEventBus):

    subscribers: List[DomainEventSubscriber]

    def __init__(self, subscribers: List[DomainEventSubscriber]):
        self.subscribers = subscribers

    @singledispatchmethod
    def find_subscribers(self, event_type: Type[DomainEvent]) -> List[DomainEventSubscriber]:
        subscribers = []

        for subscriber in self.subscribers:
            if issubclass(event_type, subscriber.event_type()):
                subscribers.append(subscriber)

        if logger.isEnabledFor(logging.WARNING):
            subscribers_len = len(subscribers)

            if subscribers_len == 0:
                logger.warning("No subscribers found for event %s", event_type)
            else:
                logger.debug("Founded %d subscribers for event %s", subscribers_len, event_type)

        return subscribers

    @find_subscribers.register
    def _(self, event: DomainEvent) -> List[DomainEventSubscriber]:
        return self.find_subscribers(type(event))

    async def async_trigger(self, event: DomainEvent):
        logger.debug("Event triggered: %s", repr(event))

        subscribers: List[DomainEventSubscriber] = self.find_subscribers(event)

        async with TaskGroup() as task_group:
            for subscriber in subscribers:
                task_group.create_task(subscriber(event))