from dependency_injector import containers, providers
from infrastructure.config import config
from infrastructure.ioc.commands_container import CommandsContainer
from infrastructure.ioc.gateways import Gateways
from infrastructure.ioc.kafka_container import KafkaContainer
from infrastructure.ioc.queries_container import QueriesContainer
from infrastructure.ioc.use_cases_container import UseCasesContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[config])
    wiring_config = containers.WiringConfiguration(
        packages=[
            "common",
            "web",
            "infrastructure.commands",
            "infrastructure.http",
            "infrastructure.kafka",
            "infrastructure.queries",
        ],
        modules=["web.api.v1.example.router"],
    )

    gateways = providers.Container(Gateways, config=config)

    kafka = providers.Container(KafkaContainer, config=config)

    queries = providers.Container(QueriesContainer, gateways=gateways)
    commands = providers.Container(CommandsContainer, gateways=gateways)

    use_cases = providers.Container(UseCasesContainer, gateways=gateways, queries=queries, commands=commands)
