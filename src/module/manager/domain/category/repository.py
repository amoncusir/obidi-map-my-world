from abc import abstractmethod

from src.module.manager.domain.category.category import Category


class CategoryRepository:

    @abstractmethod
    def create_category(self, category: Category): ...

    @abstractmethod
    def find_category_by_id(self, category_id) -> Category: ...
