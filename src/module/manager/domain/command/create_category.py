from dataclasses import dataclass
from typing import Type

from src.module.common.domain.command import Command, CommandHandler, CommandResult
from src.module.manager.domain.category import Category, CategoryRepository
from src.module.manager.domain.category.category import CategoryID


class CreateCategory(Command):
    category_name: str

    @classmethod
    def name(cls) -> str:
        return "manager_create_category"


class CreateCategoryResult(CommandResult):
    category_id: CategoryID


@dataclass
class CreateCategoryCommandHandler(CommandHandler[CreateCategory, CreateCategoryResult]):

    category_repository: CategoryRepository

    @classmethod
    def command_type(cls) -> Type[CreateCategory]:
        return CreateCategory

    async def process_command(self, command: CreateCategory) -> CreateCategoryResult:

        category = Category(name=command.category_name)
        category_id = await self.category_repository.create_category(category)

        return CreateCategoryResult(category_id=category_id)
