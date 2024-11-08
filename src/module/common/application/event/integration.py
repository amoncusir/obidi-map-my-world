from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Type, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.application.event.base import BaseEventSubscriber
from src.module.common.domain.values import GenericUUID

EventID = TypeVar("EventID", bound=UUID)


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent:

    id: EventID = field(default_factory=GenericUUID.next_id)
    event_created_at: datetime = field(default_factory=datetime.now)

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...


class IntegrationEventSubscriber[Event: IntegrationEvent](BaseEventSubscriber[Event]):
    @abstractmethod
    async def handle_event(self, event: Event): ...

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    @classmethod
    @abstractmethod
    def routing_key(cls) -> str: ...
