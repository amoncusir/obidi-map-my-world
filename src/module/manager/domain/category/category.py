from typing import Optional, TypeVar

from pydantic import Field

from src.module.common.domain.entities import DomainEntity

CategoryID = TypeVar("CategoryID", bound=str)


class Category(DomainEntity):
    id: Optional[CategoryID] = Field(kw_only=True)
    name: str
