from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from pymongo.collection import Collection
from pymongo.database import Database

from src.module.manager.domain.category import Category, CategoryRepository


class CategoryDTO(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    name: str

    @staticmethod
    def from_domain(category: Category) -> "CategoryDTO":
        oid = ObjectId(category.id) if category.id is not None else None
        return CategoryDTO(
            _id=oid,
            created_at=category.created_at,
            updated_at=category.updated_at,
            name=category.name,
        )

    def to_domain(self) -> Category:
        return Category(id=self.id, created_at=self.created_at, updated_at=self.updated_at, name=self.name)


class MongoCategoryRepository(CategoryRepository):

    mongo_collection: Collection

    def __init__(self, database: Database): ...

    def create_category(self, category: Category):
        dto = CategoryDTO.from_domain(category)
        print(dto.model_dump())
        self.mongo_collection.insert_one(dto.model_dump())

    def find_category_by_id(self, category_id) -> Category:
        doc = self.mongo_collection.find_one({"_id": ObjectId(category_id)})
        print(doc)
        dto = CategoryDTO.model_validate(doc)
        return dto.to_domain()
