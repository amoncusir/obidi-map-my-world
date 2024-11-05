from types import NoneType

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from pymongo.database import Database

from src.module.manager.domain.category import CategoryRepository
from src.module.manager.domain.command.create_category import (
    CreateCategoryCommandHandler,
)
from src.module.manager.domain.command.create_place import CreatePlaceCommandHandler
from src.module.manager.domain.place import PlaceRepository
from src.module.manager.infrastructure.mongodb.category_repository import (
    MongoCategoryRepository,
)
from src.module.manager.infrastructure.mongodb.place_repository import (
    MongoPlaceRepository,
)


class Repository(DeclarativeContainer):
    database = providers.Dependency(Database)

    mongo_place_repository = providers.Singleton(MongoPlaceRepository, database=database)

    place_repository = providers.Dependency(instance_of=PlaceRepository, default=mongo_place_repository)

    mongo_category_repository = providers.Singleton(MongoCategoryRepository, database=database)

    category_repository = providers.Dependency(instance_of=CategoryRepository, default=mongo_category_repository)


class Command(DeclarativeContainer):
    repository = providers.DependenciesContainer()

    create_category = providers.Singleton(
        CreateCategoryCommandHandler, category_repository=repository.category_repository
    )

    create_place = providers.Singleton(
        CreatePlaceCommandHandler,
        category_repository=repository.category_repository,
        place_repository=repository.place_repository,
    )


class ManagerContainer(DeclarativeContainer):
    config = providers.Configuration()
    database = providers.Dependency(Database)

    repository = providers.Container(
        Repository,
        database=database,
    )

    command = providers.Container(
        Command,
        repository=repository,
    )

    list_commands = providers.List(
        command.create_category,
        command.create_place,
    )
