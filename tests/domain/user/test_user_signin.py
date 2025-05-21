import pytest
import uuid
from faker import Faker

from domain.user.command import SignUpCommand, SignInCommand
from domain.user.service import UserDomainService
from domain.user.exc import UserNotFound, InvalidPassword
from domain.user.password import Password
from domain.user.event import UserSignedInEvent

fake = Faker()

# Helper function to create a user for tests
async def create_test_user(user_service: UserDomainService, login: str, password_str: str, email: str = None, first_name: str = None, last_name: str = None):
    if email is None:
        email = fake.email()
    if first_name is None:
        first_name = fake.first_name()
    if last_name is None:
        last_name = fake.last_name()

    signup_command = SignUpCommand(
        first_name=first_name,
        last_name=last_name,
        email=email,
        login=login,
        password=Password(hashed=password_str, is_hashed=False) # Will be hashed by Password model
    )
    return await user_service.sign_up_user(signup_command)

@pytest.mark.asyncio
async def test_successful_sign_in(user_service: UserDomainService):
    # Arrange
    test_login = fake.user_name() + str(uuid.uuid4()) # Ensure unique login
    test_password_plain = "strongPassword123"
    test_email = fake.email()

    # Create a user
    created_user_aggregate = await create_test_user(user_service, test_login, test_password_plain, email=test_email)
    assert created_user_aggregate is not None
    assert created_user_aggregate.login == test_login

    # Prepare SignInCommand
    signin_command = SignInCommand(
        login=test_login,
        password=Password(hashed=test_password_plain, is_hashed=False)
    )

    # Act
    signed_in_user_aggregate = await user_service.sign_in_user(signin_command)

    # Assert
    assert signed_in_user_aggregate is not None
    assert signed_in_user_aggregate.id == created_user_aggregate.id
    assert signed_in_user_aggregate.login == test_login
    
    # Check for UserSignedInEvent
    assert len(signed_in_user_aggregate.uncommitted_events) > 0
    signed_in_event_found = any(isinstance(event, UserSignedInEvent) for event in signed_in_user_aggregate.uncommitted_events)
    assert signed_in_event_found, "UserSignedInEvent not found in uncommitted events"

@pytest.mark.asyncio
async def test_sign_in_incorrect_password(user_service: UserDomainService):
    # Arrange
    test_login = fake.user_name() + str(uuid.uuid4())
    correct_password_plain = "correctPassword456"
    incorrect_password_plain = "wrongPassword789"
    test_email = fake.email()

    # Create a user
    await create_test_user(user_service, test_login, correct_password_plain, email=test_email)

    # Prepare SignInCommand with incorrect password
    signin_command = SignInCommand(
        login=test_login,
        password=Password(hashed=incorrect_password_plain, is_hashed=False)
    )

    # Act & Assert
    with pytest.raises(InvalidPassword):
        await user_service.sign_in_user(signin_command)

@pytest.mark.asyncio
async def test_sign_in_non_existent_user(user_service: UserDomainService):
    # Arrange
    non_existent_login = "nonExistentUser_" + fake.user_name() + str(uuid.uuid4())
    test_password_plain = "anyPassword123"

    # Prepare SignInCommand for a non-existent user
    signin_command = SignInCommand(
        login=non_existent_login,
        password=Password(hashed=test_password_plain, is_hashed=False)
    )

    # Act & Assert
    with pytest.raises(UserNotFound):
        await user_service.sign_in_user(signin_command)
