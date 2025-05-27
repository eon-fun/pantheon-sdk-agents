from loguru import logger
from pydantic import BaseModel, Extra, Field, SecretStr, ValidationInfo, field_validator  # noqa
from pydantic_settings import BaseSettings, SettingsConfigDict  # noqa


class Redis(BaseSettings):
    host: str = Field("localhost")
    port: int = Field(6379)
    db: int = Field(0)

    ttl_secs: int = Field(3600, description="1 hour")

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Relay(BaseSettings):
    host: str = Field("0.0.0.0")
    port: int = Field(9000)

    @property
    def url(self) -> str:
        return f"/ip4/{self.host}/tcp/{self.port}"


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    SERVICE_NAME: str = "relay-service"
    API_KEY: SecretStr = SecretStr("")
    DEBUG: bool = False
    redis: Redis = Redis()  # type: ignore
    relay: Relay = Relay()  # type: ignore

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
logger.info(f"Settings created: {settings}")
