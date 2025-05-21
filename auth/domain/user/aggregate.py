import dataclasses
import typing

from domain.base.aggregate import Aggregate
from domain.user.command import SignInCommand
from domain.user.event import UserCreatedEvent, UserSignedInEvent
from domain.user.exc import InvalidPassword, UserNotFound
from domain.user.password import Password


@dataclasses.dataclass
class UserAggregate(Aggregate):
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    login: typing.Optional[str] = None
    password: typing.Optional[str] = None

    async def sign_in(self, command: SignInCommand):
        if self.login is None:  # Should be loaded from events or newly created
            raise UserNotFound()

        # Assuming command.password is a Password object and self.password is a string (hashed)
        if not command.password.verify(self.password):
            raise InvalidPassword()

        event = UserSignedInEvent(aggregate_id=self.id)
        await self._apply_event(event)
        self.uncommitted_events.append(event)

    async def apply_user_created_event(self, event: UserCreatedEvent):
        self.first_name = event.event_data.first_name
        self.last_name = event.event_data.last_name
        self.email = event.event_data.email
        self.login = event.event_data.login
        self.password = event.event_data.password
        self.id = event.aggregate_id
        self.created_at = event.created_at

    async def apply_user_signed_in_event(self, event: UserSignedInEvent):
        # This event doesn't change state for now, but updates modification time
        self.updated_at = event.created_at

    def __post_init__(self):
        self._application_map = application_map


application_map = {
    UserCreatedEvent.get_type_str(): UserAggregate.apply_user_created_event,
    UserSignedInEvent.get_type_str(): UserAggregate.apply_user_signed_in_event,
}
