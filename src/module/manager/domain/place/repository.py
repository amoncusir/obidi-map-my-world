from abc import abstractmethod

from src.module.manager.domain.place import Place


class PlaceRepository:

    @abstractmethod
    def create_place(self, place: Place): ...

    @abstractmethod
    def save_last_review(self, place: Place): ...
