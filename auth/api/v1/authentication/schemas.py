import uuid

from domain.user.password import Password
from domain.utils import NonEmptyStr
from pydantic import BaseModel, EmailStr


class SignUpInput(BaseModel):
    first_name: NonEmptyStr
    last_name: NonEmptyStr

    email: EmailStr

    login: NonEmptyStr
    password: Password


class SignUpOutput(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    login: str
