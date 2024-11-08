from abc import abstractmethod
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.types import DateTime


class EntityProjection[ID](BaseModel):
    model_config = ConfigDict(frozen=True)

    id: ID = Field(..., kw_only=True)
    projected_at: DateTime = Field(..., kw_only=True)

    def __eq__(self, other):
        if not isinstance(other, EntityProjection):
            raise NotImplemented()
        return self.id == other.id

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: DomainEntity[ID]) -> Self: ...
