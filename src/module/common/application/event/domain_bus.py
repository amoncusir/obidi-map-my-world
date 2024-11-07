import asyncio
from abc import abstractmethod
from asyncio import TaskGroup
from typing import List

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.events import DomainEvent


class DomainEventBus:

    @abstractmethod
    async def async_trigger(self, event: DomainEvent): ...

    async def async_trigger_list(self, events: List[DomainEvent]):
        async with TaskGroup() as task_group:
            for event in events:
                task_group.create_task(self.async_trigger(event))

    async def async_trigger_aggregate(self, aggregate: AggregateRoot):
        await self.async_trigger_list(aggregate.pop_events())
