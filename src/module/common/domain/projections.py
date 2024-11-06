from pydantic import BaseModel, ConfigDict, Field

from src.module.common.domain.types import DateTime


class EntityProjection[ID](BaseModel):
    model_config = ConfigDict(frozen=True)

    id: ID = Field(..., kw_only=True)
    created_at: DateTime = Field(..., kw_only=True)

    def __eq__(self, other):
        if not isinstance(other, EntityProjection):
            raise NotImplemented()
        return self.id == other.id
