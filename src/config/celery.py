from typing import Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field


class CelerySettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    broker_url: str = ...

    result_backend: Optional[str] = Field(default="file:///var/celery/results")

    accept_content: Tuple[str, ...] = Field(default=("application/json",))
    event_serializer: str = Field(default="json")
    task_serializer: str = Field(default="json")
    result_serializer: str = Field(default="json")
    timezone: str = Field(default="UTC")

    beat_schedule: dict = {}
