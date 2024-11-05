from typing import Annotated, List, Tuple

from fastapi import APIRouter
from fastapi.params import Query
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from src.module.common.application.http import QueryParams

router = APIRouter(prefix="/places", tags=["place"])


class PlaceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    name: str
    latitude: float
    longitude: float


class FindCriteria(QueryParams):
    rectangle: Tuple[float, float, float, float] = Field(
        description="ABCD Rectangle coordinates to perform a geospatial search. "
        "Index (0, 1) represents the latitude and longitude of the A vertex, and "
        "(2, 3) represents the latitude and longitude of the C vertex.",
    )

    @model_validator(mode="after")
    def validate_rectangle_coordinates(self):
        for lat in (self.rectangle[0], self.rectangle[2]):
            if not -90 <= lat <= 90:
                raise ValidationError("Invalid latitude. Must be between -90 and 90 degrees.")

        for lon in (self.rectangle[1], self.rectangle[3]):
            if not -180 <= lon <= 180:
                raise ValidationError("Invalid longitude. Must be between -180 and 180 degrees.")

        return self


@router.get("/")
async def find_places(query: Annotated[FindCriteria, Query()]) -> List[PlaceResponse]: ...
