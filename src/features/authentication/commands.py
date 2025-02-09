import abc
import typing
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from features.authentication.api.v1.schemas import LoginAPIRequestModel, SignUpFormModel
from features.authentication.exc import UserNotFoundError
from features.authentication.models.user import User
from features.authentication.password_hashing import PasswordHashing
from features.authentication.user_repo import UserRepository


class UserCommand(abc.ABC):
    @abc.abstractmethod
    async def execute(self, payload: typing.Any):
        ...


class DBUserCommand(UserCommand):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    @abc.abstractmethod
    async def execute(self, payload: typing.Any):
        ...


class UserCreateCommand(DBUserCommand):
    async def execute(self, payload: SignUpFormModel) -> uuid.UUID:
        """
        Method creates a new user with its password hashing

        :param payload: user creation form
        :return: id of created user
        """
        # password hashing
        payload.password = PasswordHashing.hash_password(password=payload.password)
        created_user_id = await UserRepository.create(user_data=payload, session=self.session)
        return created_user_id


class UserLoginCommand(DBUserCommand):
    async def execute(self, payload: LoginAPIRequestModel) -> tuple[User, bool]:
        """
        Method authenticates user with password hash update

        :param payload: user credentials
        :return:
        """
        user = await UserRepository.get_by_email(email=payload.email, session=self.session)

        if user is None:
            raise UserNotFoundError()

        is_authenticated = PasswordHashing.verify_password(password=payload.password, hashed_password=user.password)

        return user, is_authenticated
