from dependency_injector import containers, providers
from httpx import AsyncClient
from httpx_backoff.backoff_options import Expo
from httpx_backoff.clients.on_predicate import PredicateClient
from infrastructure.config import config
from infrastructure.db.session import init_db_session
from infrastructure.http.services import SimpleJsonHTTPService


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_session = providers.Resource(init_db_session)

    expo_option = providers.Singleton(
        Expo,
        factor=config.HTTP_SERVICE_CONFIG.BACKOFF_FACTOR,
    )
    async_client = providers.Factory(AsyncClient)
    retry_client = providers.Factory(
        PredicateClient,
        predicate=lambda x: x.status_code in config.HTTP_SERVICE_CONFIG.STATUSES_FOR_RETRY,
        client=async_client,
        backoff_option=expo_option,
        attempts=config.HTTP_SERVICE_CONFIG.ATTEMPTS,
        timeout=config.HTTP_SERVICE_CONFIG.REQUESTS_TIMEOUT,
    )

    http_service: AsyncClient = providers.Factory(SimpleJsonHTTPService)
