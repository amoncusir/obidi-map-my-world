from abc import abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.module.common.domain.aggregates import AggregateRoot
    from src.module.common.domain.events import DomainEvent


class DomainEventBus:

    @abstractmethod
    async def async_process(self, events: List["DomainEvent"]): ...

    async def async_process_aggregate(self, aggregate: "AggregateRoot"):
        await self.async_process(aggregate.pop_events())
