from abc import abstractmethod
from typing import Annotated, Tuple

from typing_extensions import Doc

from src.module.recommendation.domain.recommendation.recommendation import PlaceView
from src.module.recommendation.domain.recommendation.values import Score


class ScoreEvaluator:

    @abstractmethod
    def evaluate(self, place: PlaceView) -> Tuple[
        Annotated[float, Doc("Weight value. Defines the relevance for the score")],
        Annotated[Score, Doc("Score punctuation")],
    ]: ...
