from pydantic import BaseModel, Field

from src.module.common.domain.types import DateTime
from src.module.common.utils import now


class DomainEntity[ID](BaseModel):
    id: ID = Field(..., kw_only=True)
    created_at: DateTime = Field(default_factory=now, kw_only=True)
    updated_at: DateTime = Field(default_factory=now, kw_only=True)

    def _update(self):
        self.updated_at = now()

    def duplicate(self):
        return self.model_copy(deep=True)

    def __eq__(self, other):
        if not isinstance(other, DomainEntity):
            raise NotImplemented()
        return self.id == other.id
