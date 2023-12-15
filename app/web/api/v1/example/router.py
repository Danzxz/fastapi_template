from core.example.dto.check_db import CheckDbQueryResult

# from common.cache import api_cache
from core.example.interfaces.check_db import ICheckDbUseCase
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

example_router = APIRouter()

# example_router.include_router(
#     BuildingAdminRouter(), tags=["admin_building"], prefix="/building"
# )

# @api_cache(expire=300)
@example_router.get("/check_db", summary="Check session to db", responses={200: {"model": CheckDbQueryResult}})
@inject
async def check_db(use_case: ICheckDbUseCase = Depends(Provide["use_cases.check_db"])) -> CheckDbQueryResult:
    return await use_case()
