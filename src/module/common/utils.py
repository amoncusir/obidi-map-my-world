from abc import abstractmethod
from datetime import UTC, datetime
from typing import Any, Dict, Self


def now() -> datetime:
    return datetime.now(tz=UTC)


class DictSerializable:

    @classmethod
    @abstractmethod
    def from_dict(cls, entity: Any) -> Self: ...

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]: ...
