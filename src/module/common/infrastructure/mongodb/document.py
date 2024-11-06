from abc import abstractmethod
from typing import Any

from pydantic import BaseModel, Field
from typing_extensions import Dict, Optional, Self

from src.module.common.infrastructure.mongodb import ValidatedObjectId


class InternalDocument[Domain](BaseModel):
    id: Optional[ValidatedObjectId] = Field(alias="_id")

    @classmethod
    @abstractmethod
    def from_domain(cls, domain: Domain) -> Self: ...

    @abstractmethod
    def to_domain(self) -> Domain: ...

    def to_document(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)
