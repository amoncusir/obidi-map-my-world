from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from pymongo.collection import Collection
from pymongo.database import Database

from src.module.common.domain.values import GenericUUID, Location
from src.module.common.infrastructure.mongodb import GeoJson
from src.module.manager.domain.place import Place, PlaceRepository
from src.module.manager.domain.place.place import Review
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


class PlaceDTO(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    name: str
    location: GeoPoint
    category: CategoryDTO
    reviews: List[ReviewDTO]

    @staticmethod
    def from_domain(place: Place) -> "PlaceDTO":
        oid = ObjectId(place.id) if place.id is not None else None

        return PlaceDTO(
            _id=oid,
            created_at=place.created_at,
            updated_at=place.updated_at,
            name=place.name,
            location=GeoPoint.from_location(place.location),
            category=CategoryDTO.from_domain(place.category),
            reviews=[ReviewDTO.from_domain(r) for r in place.reviews],
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

    mongo_collection: Collection

    def __init__(self, database: Database): ...

    def create_place(self, place: Place):
        dto = PlaceDTO.from_domain(place)
        self.mongo_collection.insert_one(dto.model_dump())

    def save_last_review(self, place: Place):
        dto = PlaceDTO.from_domain(place)
