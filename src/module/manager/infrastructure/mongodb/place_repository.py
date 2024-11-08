from datetime import datetime
from logging import getLogger
from typing import List

from bson.objectid import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from src.module.common.domain.values import GenericUUID, Location
from src.module.common.infrastructure.mongodb import GeoJson
from src.module.common.infrastructure.mongodb.document import (
    Document,
    PrincipalDocument,
)
from src.module.manager.domain.category.projections import CategoryProjection
from src.module.manager.domain.place import Place, PlaceRepository
from src.module.manager.domain.place.place import PlaceID, Review
from src.module.manager.domain.place.repository import InvalidUpdateOperation

logger = getLogger(__name__)


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


class ReviewDTO(Document):
    id: str
    created_at: datetime
    updated_at: datetime
    rate: int

    @staticmethod
    def from_domain(review: Review) -> "ReviewDTO":
        return ReviewDTO(
            id=str(review.id),
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


class CategoryProjectionDTO(Document):
    id: str
    projected_at: datetime
    name: str

    @classmethod
    def from_domain(cls, domain: CategoryProjection) -> "CategoryProjectionDTO":
        return CategoryProjectionDTO(
            id=domain.id,
            projected_at=domain.projected_at,
            name=domain.name,
        )

    def to_domain(self) -> CategoryProjection:
        return CategoryProjection(id=self.id, projected_at=self.projected_at, name=self.name)


class PlaceDTO(PrincipalDocument[Place]):
    created_at: datetime
    updated_at: datetime
    name: str
    location: GeoPoint
    category: CategoryProjectionDTO
    reviews: List[ReviewDTO]

    @classmethod
    def get_id(cls, domain: Place) -> ObjectId:
        return ObjectId(domain.id) if domain.id is not None else None

    @classmethod
    def from_domain(cls, domain: Place) -> "PlaceDTO":
        oid = cls.get_id(domain)

        return PlaceDTO(
            _id=oid,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            name=domain.name,
            location=GeoPoint.from_location(domain.location),
            category=CategoryProjectionDTO.from_domain(domain.category),
            reviews=[ReviewDTO.from_domain(r) for r in domain.reviews],
        )

    def to_domain(self) -> Place:
        reviews = []
        if self.reviews is not None:
            reviews = [r.to_domain() for r in self.reviews]

        return Place(
            id=str(self.id),
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
        return str(result.inserted_id)

    async def save_last_review(self, place: Place):
        oid = PlaceDTO.get_id(place)

        if oid is None:
            raise InvalidUpdateOperation(
                "The current place do not have an ID. To update a place must be persisted " "before"
            )

        review = place.last_review
        last_update = place.updated_at
        dto = ReviewDTO.from_domain(review)
        doc = dto.to_document()

        await self.mongo_collection.update_one(
            filter={"_id": oid},
            update={
                "$set": {"updated_at": last_update},
                "$push": {"reviews": doc},
            },
        )

    async def find_place_by_id(self, place_id: PlaceID) -> Place:
        doc = await self.mongo_collection.find_one({"_id": ObjectId(place_id)})

        logger.debug("Find place by id[%s]: %s", place_id, doc)

        dto = PlaceDTO.from_document(doc)
        return dto.to_domain()
