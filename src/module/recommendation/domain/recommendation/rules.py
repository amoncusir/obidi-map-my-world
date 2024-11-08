from dataclasses import dataclass

from src.module.common.domain.rules import Rule, RuleError
from src.module.recommendation.domain.recommendation.recommendation import PlaceView


class DifferentIDPlaceWhenUpdateRuleError(RuleError):
    pass


@dataclass(frozen=True)
class UpdatedPlaceMustBeSameID(Rule):
    current_place: PlaceView
    new_place: PlaceView

    def __call__(self):
        if self.current_place is not None and self.current_place.id != self.new_place.id:
            raise DifferentIDPlaceWhenUpdateRuleError(
                f"current_id: {self.current_place.id} new_id: {self.new_place.id}"
            )


class OlderPlaceWhenUpdateRuleError(RuleError):
    pass


@dataclass(frozen=True)
class UpdatedPlaceMustBeNewer(Rule):
    current_place: PlaceView
    new_place: PlaceView

    def __call__(self):
        if self.current_place is not None and self.current_place.last_update > self.new_place.last_update:
            raise OlderPlaceWhenUpdateRuleError(
                f"Place({self.current_place.id}); current_update: {self.new_place.last_update}, new_update: {self.current_place.last_update}"
            )


class InvalidWeightTotalScoreRuleError(RuleError):
    pass


@dataclass(frozen=True)
class TotalWeightScoreMustBeGraterThanZero(Rule):
    total_weight: float

    def __call__(self):
        if self.total_weight <= 0:
            raise InvalidWeightTotalScoreRuleError(f"Invalid weight: {self.total_weight}")
