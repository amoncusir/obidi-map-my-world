from typing import TYPE_CHECKING

from typing_extensions import Self

from src.module.common.domain.projections import EntityProjection
from src.module.manager.domain.category.category import CategoryID

if TYPE_CHECKING:
    from src.module.manager.domain.category import Category


class CategoryProjection(EntityProjection[CategoryID]):
    name: str

    @classmethod
    def from_entity(cls, entity: "Category") -> Self:
        return CategoryProjection(id=entity.id, projected_at=entity.updated_at, name=entity.name)