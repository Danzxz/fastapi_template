import asyncio
import datetime
import logging
from typing import Any, Callable, Optional

from httpx import AsyncClient, ConnectTimeout, Response
from httpx_backoff._common import _next_wait
from httpx_backoff._typing import _BackoffGenerator, _Jitterer
from httpx_backoff.backoff_options.jitter import use_full_jitter
from httpx_backoff.clients.base import CustomClient

logger = logging.getLogger(__name__)


class PredicateClient(CustomClient):
    """
    Client bases on a retry way on predicate
    """

    __slots__ = (
        "_predicate",
        "_client",
        "_backoff_option",
        "_timeout",
        "_jitter",
    )

    def __init__(
        self,
        predicate: Callable[[Response], bool],
        *,
        client: AsyncClient,
        backoff_option: _BackoffGenerator,
        attempts: int = 5,
        timeout: Optional[float] = None,
        jitter: Optional[_Jitterer] = use_full_jitter,
    ):
        """
        Constructor
        :param client: AsyncClient from httpx
        :param predicate: A function which when called on the return func of
            the target function will trigger backoff when considered
            truthfully. If not specified, the default behavior is to
            backoff on falsely return values.
        :param backoff_option: Your backoff option which influences to retrying behaviour
        :param attempts: The maximum number of attempts to make before giving
            up. In the case of failure, the result of the last attempt
            will be returned. The default func of None means there
            is no limit to the number of tries. If a callable is passed,
            it will be evaluated at runtime and its return func used.
        :param timeout: The maximum total amount of time to try for before
            giving up. If this time expires, the result of the last
            attempt will be returned. If a callable is passed, it will
            be evaluated at runtime and its return func used.
        :param jitter: A function of the func yielded by backoff_option returning
            the actual time to wait. This distributes wait times
            stochastically in order to avoid timing collisions across
            concurrent clients. Wait times are jittered by default
            using the full_jitter function. Jittering may be disabled
            altogether by passing jitter=None.
        """
        self._predicate = predicate
        self._client = client
        self._backoff_option = backoff_option
        self._timeout = timeout
        self._attempts = attempts
        self._jitter = jitter

    @property
    def client(self):
        return self._client

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
    ) -> Response:
        attempts = 0
        start = datetime.datetime.now()

        logger.info(f"Starting request on {start.isoformat()}")

        while True:
            attempts += 1
            logger.debug(f"Attempts: {attempts}")

            elapsed_time = datetime.timedelta.total_seconds(datetime.datetime.now() - start)
            logger.debug(f"Elapsed time: {elapsed_time}")

            try:
                response = await self._client.request(
                    url=url,
                    method=method,
                    json=json,
                    headers=headers,
                    data=data,
                    params=params,
                    timeout=5,
                    **kwargs,
                )
            except ConnectTimeout as e:
                response = Response(status_code=408)

            if self._predicate(response):
                max_attempts_exceeded = attempts == self._attempts
                max_time_exceeded = self._timeout is not None and elapsed_time >= self._timeout

                if max_attempts_exceeded or max_time_exceeded:
                    logger.debug(f"Max attempts: {self._attempts}\nMax time: {self._timeout}")
                    break

                try:
                    seconds = _next_wait(
                        self._backoff_option,
                        response,
                        elapsed_time,
                        self._jitter,
                        self._timeout,
                    )
                    logger.debug(f"Seconds for retry: {seconds}")
                except StopIteration:
                    break

                await asyncio.sleep(seconds)
                continue
            else:
                break

        return response

    def is_closed(self) -> bool:
        return self._client.is_closed

    async def __aexit__(self, *_: Any) -> None:
        await self._client.aclose()

    @property
    def predicate(self):
        return self._predicate
