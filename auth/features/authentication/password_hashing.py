import argon2
from argon2.exceptions import VerifyMismatchError
from argon2.profiles import RFC_9106_HIGH_MEMORY


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
        except VerifyMismatchError:
            return False
        else:
            return True
