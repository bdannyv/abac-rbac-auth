from domain.base.event import DomainEvent
from domain.user.command import SignUpCommand
from domain.utils import NonEmptyStr
from pydantic import BaseModel


class UserCreationForm(BaseModel):
    first_name: NonEmptyStr
    last_name: NonEmptyStr

    email: str

    login: NonEmptyStr
    password: NonEmptyStr

    @classmethod
    def from_command(cls, command: SignUpCommand) -> "UserCreationForm":
        return cls(
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email_str,
            login=command.login,
            password=command.password.hashed,
        )


class UserDomainEvent(DomainEvent):
    pass


class UserCreatedEvent(UserDomainEvent):
    event_data: UserCreationForm


class UserSignedInEvent(UserDomainEvent):
    pass


user_event_repo: dict[str, type[UserDomainEvent]] = {
    UserCreatedEvent.get_type_str(): UserCreatedEvent,
    UserSignedInEvent.get_type_str(): UserSignedInEvent,
}
