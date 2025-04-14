import factory
import pytest
from domain.infra.event_bus import EventBus
from domain.user.command import SignUpCommand
from domain.user.event import UserCreatedEvent
from domain.user.factory import UserFactory
from domain.user.repository import UserRepository
from domain.user.service import EmailChecker
from models import User


class SignUpCommandFactory(factory.Factory):
    class Meta:
        model = SignUpCommand

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    login = factory.LazyAttribute(lambda o: o.email)


async def test_email_checker(user_record, db_session):
    """
    Checks if the email for a given user record exists in the database and validates against it.

    :param user_record: The user record containing the email information to be checked.
    :param db_session: The database session to be used for email validation.
    :return: None, performs assertion for email existence in the database.
    """
    await db_session.flush()
    exists = await EmailChecker.email_exists(db_session, email=user_record.email)
    assert exists


@pytest.fixture
def sign_up_command():
    return SignUpCommandFactory()


async def test_user_factory(sign_up_command):
    user = await UserFactory.create(sign_up_command)

    assert len(user.uncommitted_events) == 1
    assert isinstance(user.uncommitted_events[0], UserCreatedEvent)

    assert user.first_name == sign_up_command.first_name
    assert user.last_name == sign_up_command.last_name
    assert user.email == sign_up_command.email
    assert user.login == sign_up_command.login
    assert user.password == sign_up_command.password.hashed


async def test_events_save(sign_up_command, db_session):
    init_user = await UserFactory.create(sign_up_command)
    await UserRepository.save(init_user, db_session)

    await db_session.flush()

    user = await UserRepository.get(init_user.id, db_session)

    assert init_user.id == user.id
    assert init_user.version == user.version
    assert init_user.created_at == user.created_at
    assert init_user.first_name == user.first_name
    assert init_user.last_name == user.last_name
    assert init_user.email == user.email
    assert init_user.login == user.login
    assert init_user.password == user.password


async def test_user_projection(sign_up_command, db_session):
    user_agg = await UserFactory.create(sign_up_command)
    await EventBus.publish(*user_agg.uncommitted_events)

    user_projection = await db_session.get(User, user_agg.id)

    assert user_projection.id == user_agg.id

    assert user_projection.first_name == user_agg.first_name
    assert user_projection.last_name == user_agg.last_name
    assert user_projection.email == user_agg.email
    assert user_projection.password == user_agg.password
    assert user_projection.is_active
