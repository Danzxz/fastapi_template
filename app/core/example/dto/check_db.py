
from common.dto import BaseQuery, BaseResult


class CheckDbQuery(BaseQuery):
    pass


class CheckDbQueryResult(BaseResult):
    status: bool = False
