from abc import abstractmethod
from datetime import datetime
from typing import Type, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.application.event.base import BaseEventSubscriber
from src.module.common.domain.values import GenericUUID

EventID = TypeVar("EventID", bound=UUID)


class IntegrationEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: EventID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    event_created_at: datetime = Field(default_factory=datetime.now, kw_only=True)

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...


class IntegrationEventSubscriber[Event: IntegrationEvent](BaseEventSubscriber[Event]):
    @abstractmethod
    async def handle_event(self, event: Event): ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> Type[Event]: ...
