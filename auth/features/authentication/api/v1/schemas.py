import uuid

import pydantic


class LoginAPIRequestModel(pydantic.BaseModel):
    email: str
    password: str


class LoginAPIResponseModel(pydantic.BaseModel):
    ...


class SignUpFormModel(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    first_name: str
    last_name: str
    email: str
    password: str


class SignedUPModel(pydantic.BaseModel):
    id: uuid.UUID
