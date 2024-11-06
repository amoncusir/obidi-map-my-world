from datetime import datetime

from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from src.module.common.infrastructure.mongodb.document import InternalDocument
from src.module.manager.domain.category import Category, CategoryRepository


class CategoryDTO(InternalDocument[Category]):
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
        return Category(id=self.id, created_at=self.created_at, updated_at=self.updated_at, name=self.name)


class MongoCategoryRepository(CategoryRepository):

    mongo_collection: Collection

    def __init__(self, database: Database):
        self.mongo_collection = database["categories"]

    def create_category(self, category: Category):
        dto = CategoryDTO.from_domain(category)
        document = dto.to_document()
        print(document)
        self.mongo_collection.insert_one(document)

    def find_category_by_id(self, category_id) -> Category:
        doc = self.mongo_collection.find_one({"_id": ObjectId(category_id)})
        print(doc)
        dto = CategoryDTO.model_validate(doc)
        return dto.to_domain()
