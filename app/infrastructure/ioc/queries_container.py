from dependency_injector import containers, providers
from infrastructure.db.queries.example import CheckDbQueryHandler
from infrastructure.ioc.gateways import Gateways


class QueriesContainer(containers.DeclarativeContainer):
    gateways: Gateways = providers.DependenciesContainer()

    check_db_query_handler = providers.Factory(CheckDbQueryHandler, session=gateways.db_session)
