from core.example.use_case.check_db import CheckDbUseCase
from dependency_injector import containers, providers
from infrastructure.ioc.commands_container import CommandsContainer
from infrastructure.ioc.gateways import Gateways
from infrastructure.ioc.queries_container import QueriesContainer


class UseCasesContainer(containers.DeclarativeContainer):
    gateways: Gateways = providers.DependenciesContainer()
    queries: QueriesContainer = providers.DependenciesContainer()
    commands: CommandsContainer = providers.DependenciesContainer()

    check_db = providers.Factory(CheckDbUseCase, handler=queries.check_db_query_handler)
