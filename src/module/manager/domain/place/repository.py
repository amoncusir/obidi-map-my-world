from abc import abstractmethod

from src.module.common.domain.errors import DomainError
from src.module.manager.domain.place import Place
from src.module.manager.domain.place.place import PlaceID


class InvalidUpdateOperation(DomainError):
    pass


class PlaceRepository:

    @abstractmethod
    async def create_place(self, place: Place) -> PlaceID: ...

    @abstractmethod
    async def save_last_review(self, place: Place): ...

    @abstractmethod
    async def find_place_by_id(self, place_id: PlaceID) -> Place: ...
