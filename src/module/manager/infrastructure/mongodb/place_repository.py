from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from src.module.common.domain.values import GenericUUID, Location
from src.module.common.infrastructure.mongodb import GeoJson, ValidatedObjectId
from src.module.common.infrastructure.mongodb.document import InternalDocument
from src.module.manager.domain.place import Place, PlaceRepository
from src.module.manager.domain.place.place import PlaceID, Review
from src.module.manager.infrastructure.mongodb.category_repository import CategoryDTO


class GeoPoint(GeoJson):

    @staticmethod
    def from_location(loc: Location) -> "GeoPoint":
        return GeoPoint(
            type="Point",
            coordinates=[loc.longitude, loc.latitude],
        )

    def to_location(self) -> Location:
        return Location(
            lat=self.coordinates[1],
            lon=self.coordinates[0],
        )


class ReviewDTO(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    rate: int

    @staticmethod
    def from_domain(review: Review) -> "ReviewDTO":
        return ReviewDTO(
            id=review.id,
            created_at=review.created_at,
            updated_at=review.updated_at,
            rate=review.rate,
        )

    def to_domain(self) -> Review:
        return Review(
            id=GenericUUID(self.id),
            created_at=self.created_at,
            updated_at=self.updated_at,
            rate=self.rate,
        )


class PlaceDTO(InternalDocument[Place]):
    created_at: datetime
    updated_at: datetime
    name: str
    location: GeoPoint
    category: CategoryDTO
    reviews: List[ReviewDTO]

    @classmethod
    def from_domain(cls, domain: Place) -> "PlaceDTO":
        oid = ObjectId(domain.id) if domain.id is not None else None

        return PlaceDTO(
            _id=oid,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            name=domain.name,
            location=GeoPoint.from_location(domain.location),
            category=CategoryDTO.from_domain(domain.category),
            reviews=[ReviewDTO.from_domain(r) for r in domain.reviews],
        )

    def to_domain(self) -> Place:
        reviews = []
        if self.reviews is not None:
            reviews = [r.to_domain() for r in self.reviews]

        return Place(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            category=self.category.to_domain(),
            location=self.location.to_location(),
            reviews=reviews,
        )


class MongoPlaceRepository(PlaceRepository):

    mongo_collection: AsyncCollection

    def __init__(self, database: AsyncDatabase):
        self.mongo_collection = database["places"]

    async def create_place(self, place: Place) -> PlaceID:
        dto = PlaceDTO.from_domain(place)
        result = await self.mongo_collection.insert_one(dto.to_document())
        return result.inserted_id

    async def save_last_review(self, place: Place):
        dto = PlaceDTO.from_domain(place)
