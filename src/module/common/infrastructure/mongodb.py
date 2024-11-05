from typing import List

from pydantic import BaseModel


class GeoJson(BaseModel):
    type: str
    coordinates: List[float]
