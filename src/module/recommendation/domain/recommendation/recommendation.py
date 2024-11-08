from typing import Optional, TypeVar

from pydantic import Field

from src.module.common.domain.aggregates import AggregateRoot

RecommendationID = TypeVar("RecommendationID", bound=str)


class Recommendation(AggregateRoot[RecommendationID]):
    id: Optional[RecommendationID] = Field(..., kw_only=True)
    name: str = Field(..., kw_only=True)
    score: float = Field(..., ge=0, le=1)

    @classmethod
    def create(cls, *, name: str):
        aggregate = cls(id=None, name=name)
        return aggregate
