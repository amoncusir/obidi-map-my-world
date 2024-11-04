from datetime import UTC, datetime

from pydantic import BaseModel, Field

from src.module.common.domain.types import ID, DateTime
from src.module.common.domain.values import GenericUUID


def now() -> datetime:
    return datetime.now(tz=UTC)


class DomainEntity(BaseModel):
    id: ID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    created_at: DateTime = Field(default_factory=now, kw_only=True)
    updated_at: DateTime = Field(default_factory=now, kw_only=True)

    def __eq__(self, other):
        if not isinstance(other, DomainEntity):
            raise NotImplemented()
        return self.id == other.id


class Category(DomainEntity):
    name: str


class Review(DomainEntity):
    rate: int
