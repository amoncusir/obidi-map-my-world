from datetime import datetime
from logging import getLogger

from bson.objectid import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from src.module.common.infrastructure.mongodb.document import PrincipalDocument
from src.module.manager.domain.category import Category, CategoryRepository
from src.module.manager.domain.category.category import CategoryID

logger = getLogger(__name__)


class CategoryDTO(PrincipalDocument[Category]):
    created_at: datetime
    updated_at: datetime
    name: str

    @classmethod
    def from_domain(cls, domain: Category) -> "CategoryDTO":
        oid = ObjectId(domain.id) if domain.id is not None else None
        return CategoryDTO(
            _id=oid,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            name=domain.name,
        )

    def to_domain(self) -> Category:
        return Category(id=str(self.id), created_at=self.created_at, updated_at=self.updated_at, name=self.name)


class MongoCategoryRepository(CategoryRepository):

    mongo_collection: AsyncCollection

    def __init__(self, database: AsyncDatabase):
        self.mongo_collection = database["categories"]

    async def create_category(self, category: Category) -> CategoryID:
        dto = CategoryDTO.from_domain(category)
        document = dto.to_document()

        logger.debug("New Category: %s", document)

        result = await self.mongo_collection.insert_one(document)
        return str(result.inserted_id)

    async def find_category_by_id(self, category_id: CategoryID) -> Category:
        doc = await self.mongo_collection.find_one({"_id": ObjectId(category_id)})

        logger.debug("Find Category by id[%s]: %s", category_id, doc)

        dto = CategoryDTO.model_validate(doc)
        return dto.to_domain()
