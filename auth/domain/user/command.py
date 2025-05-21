from domain.base.command import DomainCommand
from domain.user.password import Password
from pydantic import EmailStr, computed_field


class SignUpCommand(DomainCommand):
    first_name: str
    last_name: str

    email: EmailStr

    login: str
    password: Password

    @computed_field
    @property
    def email_str(self) -> str:
        return str(self.email)

    @classmethod
    def get_type(cls) -> str:
        return cls.__name__


class SignInCommand(DomainCommand):
    login: str
    password: Password

    @classmethod
    def get_type(cls) -> str:
        return cls.__name__
