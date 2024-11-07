from abc import abstractmethod
from datetime import datetime
from typing import Type

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.application.event.base import BaseEventSubscriber
from src.module.common.utils import now


class DomainEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_created_at: datetime = Field(default_factory=now)


class DomainEventSubscriber[Event: DomainEvent](BaseEventSubscriber[Event]):

    @abstractmethod
    async def handle_event(self, event: Event): ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> Type[Event]: ...
