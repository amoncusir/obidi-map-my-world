import asyncio
from asyncio import TaskGroup
from functools import singledispatchmethod
from logging import getLogger
from typing import List, Type

from src.module.common.domain.events import DomainEvent, DomainEventSubscriber

logger = getLogger(__name__)


class DomainEventBus:

    subscribers: List[DomainEventSubscriber]

    def __init__(self, subscribers: List[DomainEventSubscriber]):
        self.subscribers = subscribers

    @singledispatchmethod
    def find_subscribers(self, event_type: Type[DomainEvent]) -> List[DomainEventSubscriber]:
        subscribers = []

        for subscriber in self.subscribers:
            if issubclass(event_type, subscriber.event_type()):
                subscribers.append(subscriber)

        logger.debug("Founded %d subscribers for event %s", len(subscribers), event_type)

        return subscribers

    @find_subscribers.register
    def _(self, event: DomainEvent) -> List[DomainEventSubscriber]:
        return self.find_subscribers(type(event))

    async def async_trigger(self, event: DomainEvent):
        logger.debug("Event triggered: %s", event)

        subscribers: List[DomainEventSubscriber] = self.find_subscribers(event)

        async with TaskGroup() as task_group:
            for subscriber in subscribers:
                task_group.create_task(subscriber(event))

    def trigger(self, event: DomainEvent):
        loop = asyncio.get_event_loop()
        loop.create_task(self.async_trigger(event))

    async def async_trigger_list(self, events: List[DomainEvent]):
        async with TaskGroup() as task_group:
            for event in events:
                task_group.create_task(self.async_trigger(event))

    def trigger_list(self, events: List[DomainEvent]):
        loop = asyncio.get_event_loop()
        loop.create_task(self.async_trigger_list(events))
