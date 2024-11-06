from typing import Optional

from pydantic import BaseModel, ConfigDict


class MongoDBSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: str = ...
    database: Optional[str] = ...
