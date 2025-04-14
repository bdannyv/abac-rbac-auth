import dataclasses
import typing

from domain.base.aggregate import Aggregate
from domain.user.event import UserCreatedEvent


@dataclasses.dataclass
class UserAggregate(Aggregate):
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    login: typing.Optional[str] = None
    password: typing.Optional[str] = None

    async def apply_user_created_event(self, event: UserCreatedEvent):
        self.first_name = event.event_data.first_name
        self.last_name = event.event_data.last_name
        self.email = event.event_data.email
        self.login = event.event_data.login
        self.password = event.event_data.password
        self.id = event.aggregate_id
        self.created_at = event.created_at

    def __post_init__(self):
        self._application_map = application_map


application_map = {UserCreatedEvent.get_type_str(): UserAggregate.apply_user_created_event}
