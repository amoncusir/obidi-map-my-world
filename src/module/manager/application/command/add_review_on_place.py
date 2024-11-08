from dataclasses import dataclass
from typing import Type

from src.module.common.application.event.domain_bus import DomainEventBus
from src.module.common.domain.command import Command, CommandHandler, CommandResult
from src.module.common.domain.errors import DomainError
from src.module.manager.domain.place import PlaceRepository
from src.module.manager.domain.place.place import PlaceID, Review


class AddReviewOnPlaceNotFoundError(DomainError):
    pass


@dataclass(frozen=True, kw_only=True)
class AddReviewOnPlace(Command):
    place_id: PlaceID
    rate: int

    @classmethod
    def name(cls) -> str:
        return "manager_add_review_on_place"


class AddReviewOnPlaceResult(CommandResult):
    pass


@dataclass
class AddReviewOnPlaceCommandHandler(CommandHandler[AddReviewOnPlace, AddReviewOnPlaceResult]):
    place_repository: PlaceRepository
    domain_event_bus: DomainEventBus

    @classmethod
    def command_type(cls) -> Type[AddReviewOnPlace]:
        return AddReviewOnPlace

    async def handle_command(self, command: AddReviewOnPlace) -> AddReviewOnPlaceResult:
        place = await self.place_repository.find_place_by_id(command.place_id)

        if not place:
            raise AddReviewOnPlaceNotFoundError(f"Invalid place_id: {command.place_id}")

        review = Review(rate=command.rate)
        place.add_review(review)

        await self.place_repository.save_last_review(place)

        await self.domain_event_bus.async_process_aggregate(place)

        return AddReviewOnPlaceResult()
