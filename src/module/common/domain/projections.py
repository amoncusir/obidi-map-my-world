from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self

from src.module.common.domain.types import DateTime


@dataclass(frozen=True, kw_only=True)
class EntityProjection[ID]:
    id: ID
    projected_at: DateTime
    """
    Projection time. Must be the datetime of the last modification for the object wants to project
    """

    def __eq__(self, other):
        if not isinstance(other, EntityProjection):
            raise NotImplemented()
        return self.id == other.id

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: Any) -> Self: ...
