from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from module.container import ModuleContainer


class MainContainer(DeclarativeContainer):
    config = providers.Configuration(strict=True)

    module_container = providers.Container(
        ModuleContainer,
        config=config.module,
    )
