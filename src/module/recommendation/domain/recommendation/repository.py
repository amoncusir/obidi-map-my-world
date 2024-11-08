from abc import abstractmethod

from src.module.recommendation.domain.recommendation.recommendation import (
    Recommendation,
)


class RecommendationRepository:

    @abstractmethod
    async def create_recommendation(self, recommendation: Recommendation): ...

    @abstractmethod
    async def update_score(self, recommendation: Recommendation): ...

    @abstractmethod
    async def update_place_view(self, recommendation: Recommendation): ...

    @abstractmethod
    async def find_recommendation_by_place_id(self, recommendation_id: str) -> Recommendation: ...
