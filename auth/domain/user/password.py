import string
import typing
from functools import cached_property

import argon2
from argon2.exceptions import Argon2Error, InvalidHashError
from argon2.profiles import RFC_9106_HIGH_MEMORY
from domain.base.value_object import ValueObject
from pydantic import AfterValidator, Field, RootModel
from sqlalchemy.util import OrderedSet


class PasswordHashing:
    password_hasher = argon2.PasswordHasher(
        time_cost=RFC_9106_HIGH_MEMORY.time_cost,
        memory_cost=RFC_9106_HIGH_MEMORY.memory_cost,
        parallelism=RFC_9106_HIGH_MEMORY.parallelism,
        hash_len=RFC_9106_HIGH_MEMORY.hash_len,
        salt_len=RFC_9106_HIGH_MEMORY.salt_len,
        type=RFC_9106_HIGH_MEMORY.type,
    )

    @classmethod
    def hash_password(cls, password: str) -> str:
        hashed_pass = cls.password_hasher.hash(password=password)
        return hashed_pass

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        try:
            cls.password_hasher.verify(hashed_password, password)
        except (Argon2Error, InvalidHashError):
            return False
        else:
            return True


SPECIAL_CHARACTERS = OrderedSet("!@#$%^&*()-_=+[]{}:;,.")
VALID_PASSWORD_CHARACTERS = SPECIAL_CHARACTERS | OrderedSet(string.ascii_letters) | OrderedSet(string.digits)


def valid_password(password: str):
    if any(ch not in VALID_PASSWORD_CHARACTERS for ch in password):
        raise TypeError(f'Invalid characters in password. Valid characters are {"".join(VALID_PASSWORD_CHARACTERS)}')
    if not any(ch in SPECIAL_CHARACTERS for ch in password):
        raise TypeError(f'Password must contain one of special characters {"".join(SPECIAL_CHARACTERS)}')
    return password.strip()


ValidPassword = typing.Annotated[str, AfterValidator(valid_password)]


class Password(ValueObject, RootModel):
    root: ValidPassword = Field(min_length=10)

    @cached_property
    def hashed(self) -> str:
        return PasswordHashing.hash_password(self.root)
