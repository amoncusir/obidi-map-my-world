import logging
from asyncio import TaskGroup
from collections import deque
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
                logger.debug("Founded %d subscribers for event %s :: %s", subscribers_len, event_type, subscribers)

        return subscribers

    @find_subscribers.register
    def _(self, event: DomainEvent) -> List[DomainEventSubscriber]:
        return self.find_subscribers(type(event))

    async def async_process(self, events: List[DomainEvent]):
        logger.debug("Event triggered: %s", repr(events))
        queue = deque(events)
        processed_events = 0

        while len(queue) > 0:
            event = queue.popleft()
            processed_events += 1

            await self._handler_event(event, queue)

        logger.debug("Processed %d events", processed_events)

    async def _handler_event(self, event: DomainEvent, queue: deque[DomainEvent]):
        subscribers: List[DomainEventSubscriber] = self.find_subscribers(event)

        async with TaskGroup() as task_group:
            for subscriber in subscribers:
                task_group.create_task(_handler_subscriber(event, subscriber, queue))


async def _handler_subscriber(event: DomainEvent, subscriber: DomainEventSubscriber, queue: deque[DomainEvent]):
    new_events = await subscriber(event)
    queue.extend(new_events)
