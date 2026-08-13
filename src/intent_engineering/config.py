"""Runtime configuration loaded from environment variables and ``.env``."""

from openai import OpenAI
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the optional OpenAI-backed intent extraction step."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: SecretStr
    openai_model: str = "gpt-5.6"
    openai_baseurl: str | None = None

    @field_validator("openai_baseurl", mode="before")
    @classmethod
    def normalize_base_url(cls, value: object) -> object:
        """Treat an omitted or blank override as the OpenAI SDK default."""

        if isinstance(value, str):
            return value.strip() or None
        return value


def create_openai_client(settings: Settings) -> OpenAI:
    """Create a client using the optional ``OPENAI_BASEURL`` override."""

    return OpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        base_url=settings.openai_baseurl,
    )
