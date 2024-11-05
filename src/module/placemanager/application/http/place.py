from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/places", tags=["place"])


class CreatePlace(BaseModel):
    model_config = ConfigDict(frozen=True)
    latitude: float = Field(alias="lat", description="Latitude", allow_inf_nan=False, ge=-90.0, le=90.0)
    longitude: float = Field(alias="lon", description="Longitude", allow_inf_nan=False, ge=-180.0, le=180.0)
    category: str = Field(description="Category")


class CreatePlaceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str = Field(description="Generated ID")


@router.post("/")
async def create_place(place: CreatePlace) -> CreatePlaceResponse: ...
