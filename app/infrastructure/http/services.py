from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Any, Optional

from common.dto.errors import BusinessErrorDTO
from common.errors import BaseInternalBusinessError, ValidationBusinessError
from common.interfaces.service import ClientResponse, IHTTPService
from dependency_injector.wiring import Provide, inject
from httpx import Response
from httpx_backoff.clients.on_predicate import PredicateClient
from opentelemetry import trace
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from pydantic import ValidationError

tracer = trace.get_tracer(__name__)


class BasehttpService(IHTTPService, ABC):
    DEFAULT_DETAIL = "Failed to validate a foreign service error response"

    @inject
    def __init__(self, retry_client: PredicateClient = Provide["gateways.retry_client"]):
        self._retry_client = retry_client
        HTTPXClientInstrumentor().instrument_client(client=self._retry_client.client)

    async def _parse_error(self, error: dict, status: str) -> BaseInternalBusinessError:
        """
        Парсин ошибку
        :param error: dict: Исходная ошибка сервиса
        :param status: str: Http статус ответа сервиса
        :raises ValidationBusinessError: Не удалось распарсить структуру ошибки, возвращаем ошибку с исходной ошибкой
        и детальной ошибкой парсинга
        :return: BaseInternalBusinessError: Ошибка сервиса завернутая в исключение python
        """
        with tracer.start_as_current_span("_parse_error"):
            try:
                return BaseInternalBusinessError(**BusinessErrorDTO.parse_obj(error).dict())
            except ValidationError as e:
                raise ValidationBusinessError(
                    status=status, detail=self.DEFAULT_DETAIL, data={"rawResponse": error, "reason": e.errors()}
                )

    async def _process_error(self, response: Response) -> BaseInternalBusinessError:
        """
        Обработка ошибок сервиса

        :param response: ClientResponse: сырой aiohttp ответ сервиса
        :raises ValidationBusinessError: Поднимается в случае, если ответ сервиса не удалось разобрать и обработать.
        :return BaseInternalBusinessError: Обработанная и разобранная ошибка сервиса
        """
        with tracer.start_as_current_span("_process_error"):
            try:
                return await self._parse_error(response.json(), str(response.status_code))
            except JSONDecodeError as e:
                raise ValidationBusinessError(
                    status=str(response.status_code),
                    detail=self.DEFAULT_DETAIL,
                    data={"rawResponse": response.text, "reason": response.text},
                ) from e

    @abstractmethod
    async def _process_response(self, response: Response) -> ClientResponse:
        """
        Обработка ответа сервиса
        :param response: ClientResponse: сыройй aiohttp ответ сервиса
        :return: Response: отформатированный в ответ сервиса.
        """
        ...

    async def request(
        self,
        *,
        method: str,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Response:
        """
        Кастомный запрос к ресурсу

        :param method: Метод вызова
        :param url: URL
        :param json: json request body
        :param headers: Headers
        :param data: multipart data
        :param params: Query параметры
        :param kwargs: другие параметры, которые соответствуют интерфейсу клиента AsyncClient из httpx
        :return:
        """
        with tracer.start_as_current_span("custom_request"):
            request_headers = {**self.http_headers}
            if headers:
                request_headers.update(headers)
            response = await self._retry_client.request(url, method=method, headers=request_headers, **kwargs)
            if self._retry_client.predicate(response):
                raise await self._process_error(response)
            return await self._process_response(response)


class SimpleJsonHTTPService(BasehttpService):
    async def _process_response(self, response: Response) -> ClientResponse:
        with tracer.start_as_current_span("_process_response"):
            return response.json()
