from typing import Type

from src.module.common.domain.events import DomainEventSubscriber
from src.module.manager.domain.place.events import CreatedPlaceDomainEvent


class CreatePlaceDomainEventSubscriber(DomainEventSubscriber[CreatedPlaceDomainEvent]):

    @classmethod
    def event_type(cls) -> Type[CreatedPlaceDomainEvent]:
        return CreatedPlaceDomainEvent

    async def handle_event(self, event: CreatedPlaceDomainEvent):
        pass
