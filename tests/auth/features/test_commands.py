from unittest import mock

import pytest
import pytest_asyncio
from features.authentication.api.v1.schemas import LoginAPIRequestModel
from features.authentication.commands import UserCreateCommand, UserLoginCommand, UserLogoutCommand
from features.authentication.exc import UserNotFoundError
from features.authentication.jwt_service import JWTService
from features.authentication.password_hashing import PasswordHashing


@pytest_asyncio.fixture
async def login_request():
    return LoginAPIRequestModel(
        email="test@example.com",
        password="test_password",
    )


class TestUserCreateCommand:
    async def test_execute_success(self, db_session, user_create_form):
        # Arrange
        command = UserCreateCommand(session=db_session)
        user_create_form_init = user_create_form.model_copy(deep=True)
        # Act
        with mock.patch.object(PasswordHashing, "hash_password", return_value="hashed_password") as mock_hash:
            user_id = await command.execute(payload=user_create_form)

        # Assert
        assert user_id == user_create_form.id
        mock_hash.assert_called_once_with(password=user_create_form_init.password)

        # Verify user was created in DB
        from models.user import User

        user = await db_session.get(User, user_create_form.id)
        assert user is not None
        assert user.password == "hashed_password"


class TestUserLoginCommand:
    async def test_login_success(self, db_session, user_record, login_request):
        # Arrange
        command = UserLoginCommand(session=db_session)
        login_request.email = user_record.email

        # Act
        with mock.patch.object(PasswordHashing, "verify_password", return_value=True) as mock_verify:
            user, is_authenticated = await command.execute(payload=login_request)

        # Assert
        assert user.id == user_record.id
        assert is_authenticated is True
        mock_verify.assert_called_once_with(password=login_request.password, hashed_password=user_record.password)

    async def test_login_wrong_password(self, db_session, user_record, login_request):
        # Arrange
        command = UserLoginCommand(session=db_session)
        login_request.email = user_record.email

        # Act
        with mock.patch.object(PasswordHashing, "verify_password", return_value=False) as mock_verify:
            user, is_authenticated = await command.execute(payload=login_request)

        # Assert
        assert user.id == user_record.id
        assert is_authenticated is False
        mock_verify.assert_called_once_with(password=login_request.password, hashed_password=user_record.password)

    async def test_login_user_not_found(self, db_session, login_request):
        # Arrange
        command = UserLoginCommand(session=db_session)
        login_request.email = "nonexistent@example.com"

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await command.execute(payload=login_request)


class TestUserLogoutCommand:
    async def test_logout_success(self, encoded_token):
        # Arrange
        token_string, token_content = encoded_token

        # Act
        with (
            mock.patch.object(JWTService, "decode", return_value=token_content) as mock_decode,
            mock.patch.object(UserLogoutCommand.jwt_repo, "revoke_token") as mock_revoke,
        ):
            await UserLogoutCommand.execute(payload=token_string)

        # Assert
        mock_decode.assert_called_once_with(token_string)
        mock_revoke.assert_called_once_with(token_string, exp=token_content.exp)
