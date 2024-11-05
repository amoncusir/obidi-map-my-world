from typing import Type

from src.module.common.domain.command import Command, CommandHandler
from src.module.common.domain.values import Location
from src.module.manager.domain.category import CategoryRepository
from src.module.manager.domain.category.category import CategoryID
from src.module.manager.domain.place import Place, PlaceRepository


class CreatePlace(Command):
    category_id: CategoryID
    name: str
    location: Location

    @classmethod
    def name(cls) -> str:
        return "manager_create_place"


class CreatePlaceCommandHandler(CommandHandler[CreatePlace]):

    place_repository: PlaceRepository
    category_repository: CategoryRepository

    @classmethod
    def command_type(cls) -> Type[CreatePlace]:
        return CreatePlace

    def process_command(self, command: CreatePlace):
        category = self.category_repository.find_category_by_id(command.category_id)

        if category is None:
            ...

        place = Place(category=category, name=command.name, location=command.location)

        self.place_repository.create_place(place)
