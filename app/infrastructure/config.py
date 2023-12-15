import os
import uuid
from typing import Any, Dict, Optional

import hvac
from infrastructure.log import LogFormat, LogLevel
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, Extra, Field, validator
from pydantic.env_settings import EnvSettingsSource


class VaultSettingsSource(EnvSettingsSource):
    """
    Super modified SettingsSource for Vault! It can do everything!
    """

    _instance = None
    dotenv_vars: dict = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not VaultSettingsSource._instance:
            VaultSettingsSource._instance = super(VaultSettingsSource, cls).__new__(cls, *args, **kwargs)
        return VaultSettingsSource._instance

    def __call__(self, settings: BaseSettings) -> Dict[str, Any]:  # noqa C901
        super().__init__(
            env_file=settings.__config__.env_file,
            env_file_encoding=settings.__config__.env_file_encoding,
            env_nested_delimiter=settings.__config__.env_nested_delimiter,
            env_prefix_len=len(settings.__config__.env_prefix),
        )
        return super().__call__(settings)

    def flatten_json(self, json_obj):
        items = {}
        for key, value in json_obj.items():
            if isinstance(value, dict):
                items.update(self.flatten_json(value))
            else:
                items[key] = value
        return items

    def _read_env_files(self, case_sensitive: bool) -> Dict[str, Optional[str]]:
        if self.dotenv_vars is not None:
            return self.dotenv_vars

        if (
            "VAULT_HOST" not in os.environ
            or "VAULT_TOKEN" not in os.environ
            or "VAULT_NAMESPACE" not in os.environ
            or "VAULT_NAMESPACE" not in os.environ
        ):
            self.dotenv_vars = {}
            return self.dotenv_vars

        client = hvac.Client(
            url=os.environ.get("VAULT_HOST"),
            token=os.environ.get("VAULT_TOKEN"),
        )
        response = client.secrets.kv.v1.read_secret(
            path=os.environ.get("VAULT_NAMESPACE"), mount_point=os.environ.get("VAULT_PATH")
        )
        self.dotenv_vars = self.flatten_json(response["data"])
        if not case_sensitive:
            self.dotenv_vars = {k.lower(): v for k, v in self.dotenv_vars.items()}

        return self.dotenv_vars


class BaseProjectConfig(BaseSettings):
    class Config:
        case_sensitive = True
        extra = Extra.ignore

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                VaultSettingsSource(),
                env_settings,
                file_secret_settings,
            )


class _AsyncPostgresDsn(AnyUrl):
    allowed_schemes = {"postgres", "postgresql", "postgresql+asyncpg"}
    user_required = True


class PostgresConfig(BaseProjectConfig):
    HOST: str = "localhost"
    PORT: str = "5432"
    USER: str
    PASSWORD: str
    DB: str
    URI: Optional[_AsyncPostgresDsn] = None

    @validator("URI", pre=True, allow_reuse=True)
    def assemble_async_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return _AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("USER"),
            password=values.get("PASSWORD"),
            host=values.get("HOST"),
            port=values.get("PORT"),
            path=f"/{values.get('DB') or ''}",
        )

    class Config(BaseProjectConfig.Config):
        env_prefix = "POSTGRES_"


class CORSConfig(BaseProjectConfig):
    ORIGINS: list[str] = ["*"]
    METHODS: list[str] | str = ["*"]
    HEADERS: list[str] = ["*"]

    class Config(BaseProjectConfig.Config):
        env_prefix = "CORS_"


class TracingConfig(BaseProjectConfig):
    JAEGER_HOST: Optional[str] = None
    JAEGER_PORT: Optional[int] = None
    NAMESPACE: str = "default"
    INSTANCE_ID: str = Field(default=str(uuid.uuid4()))
    VERSION: str = "1.0.0"

    class Config(BaseProjectConfig.Config):
        env_prefix = "TRACING_"


class LogConfig(BaseProjectConfig):
    LEVEL: LogLevel = LogLevel.INFO
    FORMAT: LogFormat = LogFormat.PLAIN

    class Config(BaseProjectConfig.Config):
        env_prefix = "LOG_"


class SentryConfig(BaseProjectConfig):
    DSN: Optional[AnyHttpUrl] = None
    STAGE: str

    class Config(BaseProjectConfig.Config):
        env_prefix = "SENTRY_"


class KafkaConfig(BaseProjectConfig):
    LOCAL: bool = True
    BOOTSTRAP_SERVERS: str
    SASL_MECHANISMS: str = "SCRAM-SHA-512"
    USER: Optional[str] = None
    PASSWORD: Optional[str] = None
    AUTO_OFFSET_RESET: str = "earliest"
    GROUP_ID: str = "1"
    CA_LOCATION: Optional[str] = None
    SCHEMA_REGISTRY_URL: str = "https://test.com"
    SCHEMA_REGISTRY_USER: Optional[str] = None
    SCHEMA_REGISTRY_PASSWORD: Optional[str] = None

    # topics
    TOPIC_TEST: str

    # schemas
    SCHEMA_TEST_SUBJECT: str
    SCHEMA_TEST_ID: int

    class Config(BaseProjectConfig.Config):
        env_prefix = "KAFKA_"


class HealthCheckConfig(BaseProjectConfig):
    PERCENTAGE_MINIMUM_FOR_WORKING_CAPACITY: float = 80.0
    PERCENTAGE_MAXIMUM_FOR_WORKING_CAPACITY: float = 100.0

    class Config(BaseProjectConfig.Config):
        env_prefix = "HEALTHCHECK_"


class HTTPServiceConfig(BaseProjectConfig):
    REQUESTS_TIMEOUT: int = 5 * 60  # 5 минут
    ATTEMPTS: int = 5
    BACKOFF_FACTOR: float = 0.1
    STATUSES_FOR_RETRY: list[int] = [401, 408]

    class Config(BaseProjectConfig.Config):
        env_prefix = "HTTP_SERVICE_"


class KeycloakConfig(BaseProjectConfig):
    REALM_NAME: str
    URL: AnyHttpUrl
    CLIENT_ID: str
    CLIENT_SECRET: str
    ALGORITHMS: list[str] = ["RS256"]

    class Config(BaseProjectConfig.Config):
        env_prefix = "KEYCLOAK_"


class RedisConfig(BaseProjectConfig):
    HOST: str
    PORT: str
    DB: str
    PASSWORD: Optional[str] = None

    class Config(BaseProjectConfig.Config):
        env_prefix = "REDIS_"


class Config(BaseProjectConfig):
    PROJECT_NAME: str
    ENVIRONMENT: str = "dev"
    DEBUG: bool = False

    LOG: LogConfig = LogConfig()
    CORS_CONFIG: CORSConfig = CORSConfig()
    TRACING_CONFIG: TracingConfig = TracingConfig()
    HEALTHCHECK_CONFIG: HealthCheckConfig = HealthCheckConfig()
    KEYCLOAK_CONFIG: KeycloakConfig = KeycloakConfig()
    # SENTRY_CONFIG: SentryConfig = SentryConfig()
    KAFKA_CONFIG: KafkaConfig = KafkaConfig()

    HTTP_SERVICE_CONFIG: HTTPServiceConfig = HTTPServiceConfig()

    POSTGRES_CONFIG: PostgresConfig = PostgresConfig()
    REDIS_CONFIG: RedisConfig = RedisConfig()


config: Config = Config()
