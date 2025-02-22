import enum
import functools
import os

import pydantic
from pydantic import Field
from pydantic_settings import BaseSettings
from settings.cache import RedisSetting, get_redis_settings
from settings.data_storage import PostgresSettings, get_storage_settings
from settings.utils import load_dotenv


class AppStage(enum.StrEnum):
    dev = "dev"
    prod = "prod"


class AppSetting(BaseSettings):
    app_name: str = Field(default="auth_app")
    stage: AppStage = Field(default=AppStage.prod)

    storage: PostgresSettings
    cache: RedisSetting

    @pydantic.computed_field(return_type=bool)
    def cookie_secure(self):
        return app_settings.stage != AppStage.dev


@functools.cache
def get_app_settings() -> AppSetting:
    if os.environ.get("STAGE") == AppStage.dev.value:
        load_dotenv()

    return AppSetting(storage=get_storage_settings(), cache=get_redis_settings())


app_settings = get_app_settings()
