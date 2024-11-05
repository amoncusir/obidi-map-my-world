from src.module.manager.domain.category.category import Category


class CategoryRepository:

    def create_category(self, category: Category): ...

    def find_category_by_id(self, category_id) -> Category: ...
