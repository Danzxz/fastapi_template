from dependency_injector import containers, providers


class CommandsContainer(containers.DeclarativeContainer):
    gateways = providers.DependenciesContainer()
