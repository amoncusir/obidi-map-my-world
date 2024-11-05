from src.module.common.domain.place import Place


class PlaceRepository:

    def create_place(self, place: Place): ...

    def save_last_review(self, place: Place): ...
