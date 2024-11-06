from fastapi import APIRouter, Response, status
from pydantic import BaseModel, ConfigDict, Field

from src.app import application
from src.module.common.domain.values import Location
from src.module.manager.application.command import CreatePlace, CreatePlaceResult
from src.module.manager.application.command.add_review_on_place import AddReviewOnPlace

router = APIRouter(prefix="/places", tags=["place"])


class CreatePlaceRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    latitude: float = Field(alias="lat", allow_inf_nan=False, ge=-90.0, le=90.0)
    longitude: float = Field(alias="lon", allow_inf_nan=False, ge=-180.0, le=180.0)
    category_id: str = Field(description="Category ID")
    name: str = Field()


class CreatePlaceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str = Field(description="Place ID")


@router.post("")
async def create_place(place: CreatePlaceRequest) -> CreatePlaceResponse:
    app = application()
    bus = app.command_bus

    command = CreatePlace(
        place_name=place.name,
        category_id=place.category_id,
        location=Location(
            lat=place.latitude,
            lon=place.longitude,
        ),
    )

    result: CreatePlaceResult = await bus.exec(command)

    return CreatePlaceResponse(id=result.place_id)


class CreateReview(BaseModel):
    model_config = ConfigDict(frozen=True)
    rate: int = Field(description="Rate of review")


@router.post("/{place_id}/review")
async def review_place(place_id: str, review: CreateReview):
    app = application()
    bus = app.command_bus

    command = AddReviewOnPlace(
        place_id=place_id,
        rate=review.rate,
    )

    await bus.exec(command)

    return Response(status_code=status.HTTP_201_CREATED)
