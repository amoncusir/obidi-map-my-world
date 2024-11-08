from abc import abstractmethod
from datetime import datetime
from typing import List, Type

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.application.event.base import BaseEventSubscriber
from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.utils import now


class DomainEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_created_at: datetime = Field(default_factory=now)


class DomainEventSubscriber[Event: DomainEvent](BaseEventSubscriber[Event]):

    __queued_events: List[DomainEvent] = None

    @abstractmethod
    async def subscription_event(self, event: Event): ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> Type[Event]: ...

    async def handle_event(self, event: Event):
        self.__queued_events = []
        await self.subscription_event(event)
        return self.__pop_events()

    def _aggregate_events(self, aggregate: AggregateRoot):
        self._append_events(aggregate.pop_events())

    def _append_events(self, events: List[DomainEvent]):
        self.__queued_events.extend(events)

    def __pop_events(self) -> List[DomainEvent]:
        flushed_events = self.__queued_events.copy()
        self.__queued_events = []
        return flushed_events
