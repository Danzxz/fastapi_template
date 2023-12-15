import datetime
import uuid

import pytest
from httpx import AsyncClient
from jose import jwt

from app.infrastructure.config import Config
from app.infrastructure.ioc.container import Container
from app.web.main import create_app


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ]
)
def anyio_backend(request):
    return request.param


@pytest.fixture(scope="session")
def container():
    container = Container()
    container.init_resources()
    yield container
    container.shutdown_resources()


@pytest.fixture(scope="session")
def fastapi_app(container):
    return create_app(container)


@pytest.fixture()
async def async_test_client(fastapi_app):
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def app_config(fastapi_app, secret_key):
    Config.KEYCLOAK_CONFIG.PUBLIC_KEY = secret_key
    Config.KEYCLOAK_CONFIG.ALGORITHMS = None
    yield Config


@pytest.fixture(scope="session")
def secret_key():
    return "PUBLIC_KEY"


@pytest.fixture()
def jwt_payload(app_config):
    return {
        "exp": round((datetime.datetime.utcnow() + datetime.timedelta(hours=24)).timestamp()),
        "iat": round(datetime.datetime.utcnow().timestamp()),
        "jti": str(uuid.uuid4()),
        "iss": f"https://auth.keycloak.ru/realms/{app_config.KEYCLOAK_CONFIG.REALM_NAME}",
        "sub": str(uuid.uuid4()),
        "typ": "Bearer",
        "azp": f"{app_config.KEYCLOAK_CONFIG.CLIENT_ID}",
        "session_state": str(uuid.uuid4()),
        "allowed-origins": ["*"],
        "resource_access": {f"{app_config.KEYCLOAK_CONFIG.CLIENT_ID}": {"roles": ["get-my-agency-profile"]}},
        "scope": "openid profile email",
        "sid": str(uuid.uuid4()),
        "email_verified": True,
        "name": "Full Name",
        "preferred_username": "username",
        "given_name": "Full",
        "family_name": "Name",
        "email": "email@gmail.com",
    }


@pytest.fixture()
def jwt_token(secret_key, jwt_payload):
    return jwt.encode(jwt_payload, secret_key)
