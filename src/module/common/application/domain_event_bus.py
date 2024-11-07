import asyncio
from abc import abstractmethod
from asyncio import TaskGroup
from typing import List

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.events import DomainEvent


class DomainEventBus:

    @abstractmethod
    async def async_trigger(self, event: DomainEvent): ...

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

    async def async_trigger_aggregate(self, aggregate: AggregateRoot):
        await self.async_trigger_list(aggregate.pop_events())

    def trigger_aggregate(self, aggregate: AggregateRoot):
        self.trigger_list(aggregate.pop_events())
