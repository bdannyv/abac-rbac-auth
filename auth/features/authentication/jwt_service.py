import typing
import uuid
from datetime import datetime

import jwt
import pydantic
from settings.auth import auth_settings
from utils.singleton import Singleton


class JWTToken(pydantic.BaseModel):
    ent_id: typing.Annotated[
        typing.Optional[uuid.UUID], pydantic.PlainSerializer(str, when_used="json", return_type=str)
    ] = pydantic.Field(default_factory=uuid.uuid4)
    jti: typing.Annotated[
        typing.Optional[uuid.UUID], pydantic.PlainSerializer(str, when_used="json", return_type=str)
    ] = pydantic.Field(default_factory=uuid.uuid4)
    iss: str = auth_settings.jwt_iss
    aud: tuple[str] = auth_settings.jwt_aud
    exp: int

    def __post_init__(self):
        self.id = self.id or uuid.uuid4()


class JWTService(Singleton):
    @classmethod
    def issue_token_pair(
        cls, ent_id: uuid.UUID
    ) -> tuple[typing.Annotated[str, "Access token"], typing.Annotated[str, "Refresh token"]]:
        access = cls.encode(exp=auth_settings.jwt_access_ttl, ent_id=ent_id)
        refresh = cls.encode(exp=auth_settings.jwt_refresh_ttl)

        return access, refresh

    @classmethod
    def encode(cls, exp: int, **data) -> str:
        basic = JWTToken(exp=int(datetime.now().timestamp()) + exp, **data)
        payload = basic.model_dump(mode="json")

        return jwt.encode(payload=payload, key=auth_settings.jwt_key, algorithm=auth_settings.jwt_algo)

    @staticmethod
    def decode(token: str) -> JWTToken:
        payload = jwt.decode(
            token, algorithms=auth_settings.jwt_algo, key=auth_settings.jwt_key, audience=auth_settings.jwt_aud
        )
        return JWTToken(**payload)
