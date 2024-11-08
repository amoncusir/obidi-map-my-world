from logging import getLogger
from typing import TYPE_CHECKING, List

from pydantic import PrivateAttr

from src.module.common.domain.entities import DomainEntity

if TYPE_CHECKING:
    from src.module.common.domain.events import DomainEvent

logger = getLogger(__name__)


class AggregateRoot[ID](DomainEntity[ID]):

    __events_queue: List["DomainEvent"] = PrivateAttr(default_factory=list)

    def __del__(self):
        if len(self.__events_queue) > 0:
            class_name = self.__class__.__qualname__
            logger.error(f"Remaining events on {class_name} when destructor called! :: %s", self.__events_queue)

    def _add_event(self, event: "DomainEvent"):
        self.__events_queue.append(event)

    def pop_events(self) -> List["DomainEvent"]:
        flushed_events = self.__events_queue.copy()
        self.__events_queue = []
        return flushed_events

    def list_events_repr(self) -> List[str]:
        return [repr(e) for e in self.__events_queue]
