from domain.base.factory import AggregateFactory
from domain.user.aggregate import UserAggregate
from domain.user.command import SignUpCommand
from domain.user.event import UserCreatedEvent, UserCreationForm


class UserFactory(AggregateFactory[UserAggregate]):
    @classmethod
    async def create(cls, creation_command: SignUpCommand) -> UserAggregate:
        user = UserAggregate()
        create_event = UserCreatedEvent(
            event_type=UserCreatedEvent.get_type_str(),
            event_data=UserCreationForm.from_command(creation_command),
            aggregate_id=user.id,
            aggregate_type=user.get_type(),
            aggregate_version=user.get_version_increment(),
            correlation_id=creation_command.id,
            causation_type=creation_command.get_type(),
            causation_id=creation_command.id,
        )

        await user.apply(create_event)
        user.record_events(create_event)

        return user
