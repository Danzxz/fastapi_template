from core.example.dto.check_db import CheckDbQuery, CheckDbQueryResult
from core.example.interfaces.check_db import ICheckDbQueryHandler
from infrastructure.db.base import BaseRepository
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


class CheckDbQueryHandler(BaseRepository, ICheckDbQueryHandler):
    async def ask(self, query: CheckDbQuery = None) -> CheckDbQueryResult:
        try:
            await self.session.execute(text("SELECT 1"))
            status = True
        except SQLAlchemyError as e:
            status = False
        return CheckDbQueryResult(status=status)
