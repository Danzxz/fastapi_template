from typing import Any, Optional

from common.errors import BaseBusinessError
from fastapi import HTTPException


class HTTPCustomError(HTTPException):
    __slots__ = (
        "status_code",
        "detail",
        "headers",
        "_business_error",
    )

    def __init__(
        self,
        status_code: int,
        business_error: BaseBusinessError,
        detail: Optional[Any] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
        self._business_error = business_error

    @property
    def business_error(self) -> BaseBusinessError:
        return self._business_error
