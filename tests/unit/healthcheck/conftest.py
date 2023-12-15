import random
from typing import Type

import pytest

from app.infrastructure.config import HealthCheckConfig
from app.web.healthcheck.commands import BaseCommand, CommandResult
from app.web.healthcheck.handler import CommandHandler
from app.web.healthcheck.status import Status


class SuccessfulMockCommand(BaseCommand):
    async def execute(self) -> CommandResult:
        return CommandResult(
            status=Status.HEALTHY,
            duration=float(random.randrange(1, 5)),
        )


class FailedMockCommand(BaseCommand):
    async def execute(self) -> CommandResult:
        return CommandResult(
            status=Status.UNHEALTHY,
            duration=float(random.randrange(1, 5)),
            exception="SomethingError",
            description="Something went wrong",
        )


@pytest.fixture()
def successful_mock_command() -> SuccessfulMockCommand:
    return SuccessfulMockCommand()


@pytest.fixture()
def failed_mock_command() -> FailedMockCommand:
    return FailedMockCommand()


@pytest.fixture()
def command_handler() -> CommandHandler:
    return CommandHandler()


@pytest.fixture()
def healthcheck_config() -> Type[HealthCheckConfig]:
    return HealthCheckConfig
