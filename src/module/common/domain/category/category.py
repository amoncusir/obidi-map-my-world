import uuid
from typing import TypeVar

from pydantic import Field

from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.values import GenericUUID

CategoryID = TypeVar("CategoryID", bound=uuid.UUID)


class Category(DomainEntity):
    id: CategoryID = Field(default_factory=GenericUUID.next_id, kw_only=True)
    name: str
