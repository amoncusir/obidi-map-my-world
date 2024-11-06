from datetime import UTC, datetime

from pydantic import BaseModel, Field

from src.module.common.domain.types import DateTime


def now() -> datetime:
    return datetime.now(tz=UTC)


class DomainEntity[ID](BaseModel):
    id: ID = Field(..., kw_only=True)
    created_at: DateTime = Field(default_factory=now, kw_only=True)
    updated_at: DateTime = Field(default_factory=now, kw_only=True)

    def _update(self):
        self.updated_at = now()

    def __eq__(self, other):
        if not isinstance(other, DomainEntity):
            raise NotImplemented()
        return self.id == other.id
