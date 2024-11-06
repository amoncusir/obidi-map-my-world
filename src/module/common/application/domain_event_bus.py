import asyncio
from asyncio import TaskGroup
from functools import singledispatchmethod
from typing import Dict, List, Type

from src.module.common.domain.events import DomainEvent, DomainEventSubscriber


class DomainEventBus:

    subscribers: List[DomainEventSubscriber]

    def __init__(self, subscribers: List[DomainEventSubscriber]):
        self.subscribers = subscribers

    @singledispatchmethod
    def find_subscribers(self, event_type: Type[DomainEvent]) -> List[DomainEventSubscriber]:
        subscribers = []

        for subscriber in self.subscribers:
            if isinstance(subscriber.event_type(), event_type):
                subscribers.append(subscriber)

        return subscribers

    @find_subscribers.register
    def _(self, event: DomainEvent) -> List[DomainEventSubscriber]:
        return self.find_subscribers(type(event))

    async def async_trigger(self, event: DomainEvent):
        subscribers: List[DomainEventSubscriber] = self.find_subscribers(event)

        async with TaskGroup() as task_group:
            for subscriber in subscribers:
                task_group.create_task(subscriber(event))

    def trigger(self, event: DomainEvent):
        loop = asyncio.get_event_loop()
        loop.create_task(self.async_trigger(event))
