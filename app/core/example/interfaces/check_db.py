from abc import ABC, abstractmethod

from common.interfaces.query import IQueryHandler
from core.example.dto.check_db import CheckDbQuery, CheckDbQueryResult


class ICheckDbQueryHandler(IQueryHandler, ABC):
    @abstractmethod
    async def ask(self, query: CheckDbQuery = None) -> CheckDbQueryResult:
        raise NotImplementedError


class ICheckDbUseCase(ABC):
    def __init__(self, handler: ICheckDbQueryHandler):
        self.handler = handler

    @abstractmethod
    async def __call__(self) -> CheckDbQueryResult:
        ...
