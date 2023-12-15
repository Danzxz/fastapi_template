from abc import ABCMeta, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Any, Optional

from httpx import Response


class CustomClient(AbstractAsyncContextManager, metaclass=ABCMeta):
    """
    Abstract class for backoff clients
    """

    @abstractmethod
    async def _request(
        self,
        url: str,
        *,
        method: str = "GET",
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        It's a custom protected request which encapsulates request with backoff behavior.

        **Parameters**: See `httpx.request`.
        """
        ...

    async def request(
        self,
        url: str,
        *,
        method: str = "GET",
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        It's a custom public request which encapsulates request with backoff behavior.

        **Parameters**: See `httpx.request`.
        """
        return await self._request(
            url=url,
            method=method,
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    async def get(
        self,
        url: str,
        *,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        Send a custom `GET` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            url=url,
            method="GET",
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    async def post(
        self,
        url: str,
        *,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        Send a custom `POST` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            url=url,
            method="POST",
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    async def patch(
        self,
        url: str,
        *,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        Send a custom `PATCH` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            url=url,
            method="PATCH",
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    async def put(
        self,
        url: str,
        *,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        Send a custom `PUT` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            url=url,
            method="PUT",
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    async def delete(
        self,
        url: str,
        *,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        Send a custom `DELETE` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            url=url,
            method="DELETE",
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    async def options(
        self,
        url: str,
        *,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        Send a custom `OPTIONS` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            url=url,
            method="OPTIONS",
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    async def head(
        self,
        url: str,
        *,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """
        Send a custom `HEAD` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            url=url,
            method="HEAD",
            json=json,
            headers=headers,
            data=data,
            params=params,
            **kwargs,
        )

    @abstractmethod
    def is_closed(self) -> bool:
        ...

    async def __aenter__(self) -> "CustomClient":
        return self
