from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter
from fastapi.params import Query
from pydantic import BaseModel, ConfigDict, Field

from module.common.application.http import QueryParams

router = APIRouter(prefix="/recommend", tags=["recommendation"])


class ReviewResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    rate: int = Field(description="Rate number")


class PlaceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    name: str
    latitude: float
    longitude: float
    last_date_review: datetime
    reviews: List[ReviewResponse]


class FindCriteria(QueryParams):
    latitude: float = Field(alias="lat", description="Latitude", allow_inf_nan=False, ge=-90.0, le=90.0)
    longitude: float = Field(alias="lon", description="Longitude", allow_inf_nan=False, ge=-180.0, le=180.0)
    radius: int = Field(default=50, description="Radius to find places in kilometers", gt=0)


@router.get("/places", tags=["place"])
async def recommend_places(query: Annotated[FindCriteria, Query()]) -> List[PlaceResponse]: ...
