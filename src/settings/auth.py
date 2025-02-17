import functools
from datetime import timedelta

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.base import app_settings


class AuthenticationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="auth_")

    jwt_access_ttl: int = Field(default=timedelta(minutes=10).total_seconds(), description="JWT token lifetime")
    jwt_refresh_ttl: int = Field(default=timedelta(days=10).total_seconds(), description="JWT token lifetime")
    jwt_aud: tuple[str] = Field(default=("urn:user",), description="JWT token audience claim")
    jwt_iss: str = f"urn:{app_settings}"
    jwt_key: str
    jwt_algo: str = Field(default="HS256")


@functools.cache
def get_auth_settings() -> AuthenticationSettings:
    return AuthenticationSettings()


auth_settings = get_auth_settings()
