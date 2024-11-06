from abc import abstractmethod
from typing import Any

from pydantic import BaseModel, Field
from typing_extensions import Dict, Optional, Self

from src.module.common.infrastructure.mongodb import ValidatedObjectId


class Document(BaseModel):
    def to_document(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_defaults=True)

    @classmethod
    def from_document(cls, document: Dict[str, Any]) -> "Document":
        return cls.model_load(document)


class PrincipalDocument[Domain](Document):
    id: Optional[ValidatedObjectId] = Field(default=None, alias="_id")

    @classmethod
    @abstractmethod
    def from_domain(cls, domain: Domain) -> Self: ...

    @abstractmethod
    def to_domain(self) -> Domain: ...
