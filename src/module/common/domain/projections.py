from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from src.module.common.utils import DictSerializable


@dataclass(frozen=True, kw_only=True)
class EntityProjection[ID](DictSerializable):
    id: ID
    projected_at: datetime
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
