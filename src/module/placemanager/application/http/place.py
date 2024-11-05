from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/places", tags=["place"])


class CreatePlace(BaseModel):
    model_config = ConfigDict(frozen=True)
    latitude: float = Field(alias="lat", allow_inf_nan=False, ge=-90.0, le=90.0)
    longitude: float = Field(alias="lon", allow_inf_nan=False, ge=-180.0, le=180.0)
    category: str = Field(description="Category ID")


class CreatePlaceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str = Field(description="Generated ID")


@router.post("/")
async def create_place(place: CreatePlace) -> CreatePlaceResponse: ...


class CreateReview(BaseModel):
    model_config = ConfigDict(frozen=True)
    rate: int = Field(description="Rate of review", ge=0, le=5)


@router.post("/{place_id}/review", status_code=201)
async def review_place(place_id: str, review: CreateReview): ...
