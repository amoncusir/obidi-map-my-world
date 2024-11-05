import uuid
from typing import Self

from pydantic import BaseModel, ConfigDict, Field


class GenericUUID(uuid.UUID):
    @classmethod
    def next_id(cls) -> Self:
        return cls(int=uuid.uuid4().int)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, validation_info):
        if isinstance(value, str):
            return cls(value)
        if not isinstance(value, uuid.UUID):
            raise ValueError("Invalid UUID")
        return cls(value.hex)


class Location(BaseModel):
    model_config = ConfigDict(frozen=True)

    latitude: float = Field(alias="lat", allow_inf_nan=False, ge=-90.0, le=90.0)
    longitude: float = Field(alias="lon", allow_inf_nan=False, ge=-180.0, le=180.0)
