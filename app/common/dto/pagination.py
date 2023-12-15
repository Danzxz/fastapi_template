from typing import Generic, TypeVar

from common.dto import BaseResult, CustomModel
from pydantic.generics import GenericModel

ResultType = TypeVar("ResultType", bound=BaseResult)


class PaginationQuery(CustomModel):
    offset: int
    limit: int


class PageInfo(CustomModel):
    page_number: int
    page_size: int


class PaginationResult(GenericModel, CustomModel, Generic[ResultType]):
    items: list[ResultType]
    total_count: int
    page: PageInfo
