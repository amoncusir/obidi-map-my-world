from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Annotated, Final, Tuple

from typing_extensions import Doc

from src.module.recommendation.domain.recommendation.projections import (
    PlaceViewProjection,
)
from src.module.recommendation.domain.values import Score


class StateEvaluator:

    @abstractmethod
    def evaluate(self, place: PlaceViewProjection) -> bool: ...


class DisableIfPlaceIsUpdatedInLast30Days(StateEvaluator):

    def evaluate(self, place: PlaceViewProjection) -> bool:
        thirty_days_ago = datetime.now() - timedelta(days=30)

        return place.projected_at >= thirty_days_ago


class ScoreEvaluator:

    @abstractmethod
    def evaluate(self, place: PlaceViewProjection) -> Tuple[
        Annotated[float, Doc("Weight value. Defines the relevance for the score")],
        Annotated[Score, Doc("Score punctuation")],
    ]: ...


class ReviewCountScoreEvaluator(ScoreEvaluator):

    punctuation_value: Final[float] = 0.0000000000000004
    weight: Final[float] = 0.8

    def evaluate(self, place: PlaceViewProjection) -> Tuple[
        Annotated[float, Doc("Weight value. Defines the relevance for the score")],
        Annotated[Score, Doc("Score punctuation")],
    ]:
        punctuation = place.total_reviews * self.punctuation_value
        return (
            self.weight,
            Score(punctuation),
        )


class OlderScoreEvaluator(ScoreEvaluator):
    """
    Another evaluator example. Isn't added to the current scoring flow, because the business rules only prioritize the
    non reviewed places.
    """

    punctuation_value: Final[float] = 0.0000000000000002
    weight: Final[float] = 0.4

    def evaluate(self, place: PlaceViewProjection) -> Tuple[
        Annotated[float, Doc("Weight value. Defines the relevance for the score")],
        Annotated[Score, Doc("Score punctuation")],
    ]:
        now = datetime.now()
        difference_from_now = now - place.projected_at
        punctuation = difference_from_now.timestamp() * self.punctuation_value

        return (
            self.weight,
            Score(punctuation),
        )
