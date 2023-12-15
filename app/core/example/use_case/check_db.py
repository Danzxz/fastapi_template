from core.example.dto.check_db import CheckDbQueryResult
from core.example.interfaces.check_db import ICheckDbUseCase


class CheckDbUseCase(ICheckDbUseCase):
    async def __call__(self) -> CheckDbQueryResult:
        return await self.handler.ask()
