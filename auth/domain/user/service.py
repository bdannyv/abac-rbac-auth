import functools

from core.data_storage import session_factory
from domain.infra.event_bus import EventBus
from domain.infra.utils import pg_advisory_lock
from domain.user.aggregate import UserAggregate
from domain.user.command import SignUpCommand
from domain.user.exc import EmailAlreadyExists
from domain.user.factory import UserFactory
from domain.user.queries import email_exists
from domain.user.repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class EmailChecker:
    @classmethod
    async def email_exists(cls, session: AsyncSession, email: str) -> bool:
        exists_q = email_exists(email)
        exists_result = await session.execute(exists_q)
        return exists_result.scalar()


class UserDomainService:
    user_repo = UserRepository
    user_factory = UserFactory
    event_bus = EventBus

    @classmethod
    async def sign_up_user(cls, command: SignUpCommand) -> UserAggregate:
        """
        Creates and saves a new user entity in the database after checking if the provided email
        already exists. If the email exists, raises an exception to prevent duplicate registration.
        The operation is atomic, ensuring no partial writes in case of errors and locking rows with
        requested email.

        :param command: The command object containing the necessary parameters for user creation.
        :type command: SignUpCommand
        :return: The newly created user entity.
        :rtype: User
        :raises EmailAlreadyExists: If the provided email already exists in the system.
        """
        async with session_factory() as session:
            async with session.begin_nested():
                # within transaction actions with provided email are locked with query below
                await pg_advisory_lock(session=session, value=command.email_str)
                exists = await EmailChecker.email_exists(session=session, email=command.email_str)
                if exists:
                    raise EmailAlreadyExists(email=command.email_str)

                with await cls.user_factory.create(command) as user:
                    await cls.user_repo.save(user, session)
                    await cls.event_bus.publish(*user.uncommitted_events)

        return user


@functools.cache
def user_service_factory() -> UserDomainService:
    return UserDomainService()
