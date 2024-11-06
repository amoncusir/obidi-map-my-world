from abc import abstractmethod

from src.module.manager.domain.category.category import Category, CategoryID


class CategoryRepository:

    @abstractmethod
    async def create_category(self, category: Category) -> CategoryID: ...

    @abstractmethod
    async def find_category_by_id(self, category_id: CategoryID) -> Category: ...
