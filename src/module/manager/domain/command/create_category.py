from dataclasses import dataclass
from typing import Type

from src.module.common.domain.command import Command, CommandHandler
from src.module.manager.domain.category import Category, CategoryRepository


class CreateCategory(Command):
    category_name: str

    @classmethod
    def name(cls) -> str:
        return "manager_create_category"


@dataclass
class CreateCategoryCommandHandler(CommandHandler[CreateCategory]):

    category_repository: CategoryRepository

    @classmethod
    def command_type(cls) -> Type[CreateCategory]:
        return CreateCategory

    def process_command(self, command: CreateCategory):

        category = Category(name=command.category_name)
        self.category_repository.create_category(category)
