from abc import abstractmethod
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.domain.types import ID
from src.module.common.domain.values import GenericUUID


class ApplicationEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: ID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    created_at: datetime = Field(default_factory=datetime.now, kw_only=True)

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...
