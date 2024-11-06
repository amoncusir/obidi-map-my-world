from dependency_injector import providers


class DomainEventSubscriberProvider(providers.Singleton):
    pass


class CommandHandlerProvider(providers.Singleton):
    pass
