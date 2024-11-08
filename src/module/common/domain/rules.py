from abc import abstractmethod
from dataclasses import dataclass

from src.module.common.domain.errors import DomainError


class RuleError(DomainError):
    pass


@dataclass(frozen=True, kw_only=True)
class Rule:

    def __post_init__(self):
        self()

    @abstractmethod
    def __call__(self): ...
