from logging import getLogger

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from src.module.recommendation.domain.recommendation.recommendation import (
    Recommendation,
)
from src.module.recommendation.domain.recommendation.repository import (
    RecommendationRepository,
)

logger = getLogger(__name__)


class MongoDBRecommendationRepository(RecommendationRepository):
    mongo_collection: AsyncCollection

    def __init__(self, database: AsyncDatabase):
        self.mongo_collection = database["recommendations"]

    async def create_recommendation(self, recommendation: Recommendation):
        pass

    async def update_score(self, recommendation: Recommendation):
        pass

    async def update_place_view(self, recommendation: Recommendation):
        pass

    async def find_recommendation_by_place_id(self, recommendation_id: str) -> Recommendation:
        pass
