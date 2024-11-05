from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")
K = TypeVar("K")


class QueryParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class PaginatedResponse(BaseModel, Generic[T, K]):
    model_config = ConfigDict(frozen=True)

    items: List[T] = Field(description="List of items")
    next_token: Optional[K] = Field(default=None, description="Next token")

    def has_next(self) -> bool:
        return self.next_token is not None
