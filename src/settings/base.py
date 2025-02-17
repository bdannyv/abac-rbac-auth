import enum
import functools

import pydantic
from pydantic import Field
from pydantic_settings import BaseSettings


class AppStage(enum.StrEnum):
    dev = "dev"
    prod = "prod"


class AppSetting(BaseSettings):
    app_name: str = Field(default="auth_app")
    stage: AppStage = Field(default=AppStage.prod)

    @pydantic.computed_field
    def cookie_secure(self):
        return app_settings.stage != AppStage.dev


@functools.cache
def get_app_settings() -> AppSetting:
    return AppSetting()


app_settings = get_app_settings()
