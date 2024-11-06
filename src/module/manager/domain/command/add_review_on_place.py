from dataclasses import dataclass
from typing import Type

from src.module.common.domain.command import Command, CommandHandler, CommandResult
from src.module.common.domain.errors import DomainError
from src.module.manager.domain.place import PlaceRepository
from src.module.manager.domain.place.place import PlaceID, Review


class AddReviewOnPlaceNotFoundError(DomainError):
    pass


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

    @classmethod
    def command_type(cls) -> Type[AddReviewOnPlace]:
        return AddReviewOnPlace

    async def process_command(self, command: AddReviewOnPlace) -> AddReviewOnPlaceResult:
        place = await self.place_repository.find_place_by_id(command.place_id)

        if not place:
            raise AddReviewOnPlaceNotFoundError(f"Invalid place_id: {command.place_id}")

        review = Review(rate=command.rate)
        place.add_review(review)

        await self.place_repository.save_last_review(place)

        return AddReviewOnPlaceResult()
