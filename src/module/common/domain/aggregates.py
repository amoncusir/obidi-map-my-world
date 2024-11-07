from typing import List

from pydantic import PrivateAttr

from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.events import DomainEvent


class AggregateRoot[ID](DomainEntity[ID]):

    __events_queue: List[DomainEvent] = PrivateAttr(default_factory=list)

    def _add_event(self, event: DomainEvent):
        self.__events_queue.append(event)

    def pop_events(self) -> List[DomainEvent]:
        flushed_events = self.__events_queue.copy()
        self.__events_queue = []
        return flushed_events

    def list_events_repr(self) -> List[str]:
        return [repr(e) for e in self.__events_queue]
