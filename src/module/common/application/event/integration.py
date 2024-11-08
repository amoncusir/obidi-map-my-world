from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Type, TypeVar
from uuid import UUID

from src.module.common.application.event.base import BaseEventSubscriber
from src.module.common.domain.values import GenericUUID
from src.module.common.utils import DictSerializable

EventID = TypeVar("EventID", bound=UUID)


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent(DictSerializable):

    id: EventID = field(default_factory=GenericUUID.next_id)
    event_created_at: datetime = field(default_factory=datetime.now)

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...


class IntegrationEventSubscriber[Event: IntegrationEvent](BaseEventSubscriber[Event]):

    async def __call__(self, dict_event: Event):
        print(dict_event)
        event = self.event_type().from_dict(dict_event)
        return await super().__call__(event)

    @abstractmethod
    async def handle_event(self, event: Event): ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> Type[Event]: ...

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    @classmethod
    @abstractmethod
    def routing_key(cls) -> str: ...
