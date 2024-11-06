from dataclasses import dataclass
from typing import Type

from src.module.common.domain.command import Command, CommandHandler, CommandResult
from src.module.common.domain.errors import DomainError
from src.module.common.domain.values import Location
from src.module.manager.domain.category import CategoryRepository
from src.module.manager.domain.category.category import CategoryID
from src.module.manager.domain.place import Place, PlaceRepository
from src.module.manager.domain.place.place import PlaceID


class CreatePlaceInvalidCategoryIdError(DomainError):
    pass


class CreatePlace(Command):
    category_id: CategoryID
    place_name: str
    location: Location

    @classmethod
    def name(cls) -> str:
        return "manager_create_place"


class CreatePlaceResult(CommandResult):
    place_id: PlaceID


@dataclass
class CreatePlaceCommandHandler(CommandHandler[CreatePlace, CreatePlaceResult]):

    place_repository: PlaceRepository
    category_repository: CategoryRepository

    @classmethod
    def command_type(cls) -> Type[CreatePlace]:
        return CreatePlace

    async def process_command(self, command: CreatePlace) -> CreatePlaceResult:
        category = await self.category_repository.find_category_by_id(command.category_id)

        if category is None:
            raise CreatePlaceInvalidCategoryIdError("Invalid category_id")

        place = Place(category=category, name=command.place_name, location=command.location)

        place_id = await self.place_repository.create_place(place)

        return CreatePlaceResult(place_id=place_id)
