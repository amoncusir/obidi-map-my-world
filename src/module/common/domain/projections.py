from abc import abstractmethod
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.domain.types import DateTime


class EntityProjection[ID](BaseModel):
    model_config = ConfigDict(frozen=True)

    id: ID = Field(..., kw_only=True)
    projected_at: DateTime = Field(
        ...,
        kw_only=True,
        description="Projection time. Must be the datetime of the last modification for " "the object wants to project",
    )

    def __eq__(self, other):
        if not isinstance(other, EntityProjection):
            raise NotImplemented()
        return self.id == other.id

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: Any) -> Self: ...
