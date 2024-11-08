from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Dict, Final, Self

from dacite import Config, from_dict

from src.module.common.domain.values import Location


def now() -> datetime:
    return datetime.now(tz=UTC)


@dataclass(frozen=True)
class DictSerializable:

    @classmethod
    def from_dict(cls, entity: Any) -> Self:
        return from_dict(
            cls, entity, config=Config(type_hooks={datetime: datetime.fromisoformat, Location: Location.model_validate})
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
