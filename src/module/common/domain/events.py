from abc import abstractmethod
from datetime import datetime
from logging import Logger, getLogger
from typing import Type

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.utils import now


class DomainEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    created_at: datetime = Field(default_factory=now)


class DomainEventSubscriber[Event: DomainEvent]:
    log: Logger = getLogger(__name__)

    async def __call__(self, event: Event):
        start = datetime.now()
        result = await self.handle_event(event)

        self.log.debug("Handled Event on time (%s): %s", datetime.now() - start, repr(event))

        return result

    @abstractmethod
    async def handle_event(self, event: Event): ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> Type[Event]: ...