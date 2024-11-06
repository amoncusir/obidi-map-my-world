from dataclasses import dataclass
from typing import Type

from src.module.common.domain.command import Command, CommandHandler
from src.module.common.domain.errors import DomainError
from src.module.common.domain.values import Location
from src.module.manager.domain.category import CategoryRepository
from src.module.manager.domain.category.category import CategoryID
from src.module.manager.domain.place import Place, PlaceRepository


class CreatePlaceInvalidCategoryIdError(DomainError):
    pass


class CreatePlace(Command):
    category_id: CategoryID
    place_name: str
    location: Location

    @classmethod
    def name(cls) -> str:
        return "manager_create_place"


@dataclass
class CreatePlaceCommandHandler(CommandHandler[CreatePlace]):

    place_repository: PlaceRepository
    category_repository: CategoryRepository

    @classmethod
    def command_type(cls) -> Type[CreatePlace]:
        return CreatePlace

    def process_command(self, command: CreatePlace):
        category = self.category_repository.find_category_by_id(command.category_id)

        if category is None:
            raise CreatePlaceInvalidCategoryIdError("Invalid category_id")

        place = Place(category=category, name=command.place_name, location=command.location)

        self.place_repository.create_place(place)
