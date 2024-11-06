from dataclasses import dataclass
from typing import Type

from src.module.common.domain.command import Command, CommandHandler, CommandResponse
from src.module.manager.domain.category import Category, CategoryRepository
from src.module.manager.domain.category.category import CategoryID


class CreateCategory(Command):
    category_name: str

    @classmethod
    def name(cls) -> str:
        return "manager_create_category"


class CreateCategoryResponse(CommandResponse):
    category_id: CategoryID


@dataclass
class CreateCategoryCommandHandler(CommandHandler[CreateCategory, CreateCategoryResponse]):

    category_repository: CategoryRepository

    @classmethod
    def command_type(cls) -> Type[CreateCategory]:
        return CreateCategory

    async def process_command(self, command: CreateCategory) -> CreateCategoryResponse:

        category = Category(name=command.category_name)
        category_id = await self.category_repository.create_category(category)

        return CreateCategoryResponse(category_id=category_id)
