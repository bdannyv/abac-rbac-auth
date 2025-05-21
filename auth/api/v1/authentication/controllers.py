from api.v1.authentication.schemas import SignInInput, SignInOutput, SignUpInput, SignUpOutput
from auth.core.security import create_access_token
from domain.user.command import SignInCommand, SignUpCommand
from domain.user.exc import InvalidPassword, UserNotFound
from domain.user.password import Password
from domain.user.service import UserDomainService, user_service_factory
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

authentication = APIRouter(prefix="/authentication")


@authentication.post("/sign-up", response_model=SignUpOutput)
async def sign_up(sign_up_data: SignUpInput, user_service: UserDomainService = Depends(user_service_factory)):
    """
    Handles the sign-up process for new users by accepting their data, processing the
    sign-up command, and returning the created user's information.

    __sign_up_data__: Contains the sign-up details provided by the user, such as first name, last name, email, login,
    and password.

    _sign_up_data_: SignUpInput

    __user_service__: A dependency-injected domain service responsible for handling user-related operations.

    _user_service_: UserDomainService

    __return__: An object containing the details of the newly created user, including
        their ID, first name, last name, email, and login.
    """
    command = SignUpCommand(
        first_name=sign_up_data.first_name,
        last_name=sign_up_data.last_name,
        email=sign_up_data.email,
        login=sign_up_data.login,
        password=sign_up_data.password,
    )

    new_user = await user_service.sign_up_user(command)

    return SignUpOutput(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        login=new_user.login,
    )


@authentication.post("/sign-in", response_model=SignInOutput)
async def sign_in(sign_in_data: SignInInput, user_service: UserDomainService = Depends(user_service_factory)):
    """
    Handles the sign-in process for existing users.

    __sign_in_data__: Contains the login and password provided by the user.
    _sign_in_data_: SignInInput

    __user_service__: A dependency-injected domain service responsible for handling user-related operations.
    _user_service_: UserDomainService

    __return__: An object containing the user's ID and login upon successful authentication.
    _return_: SignInOutput

    __raises__:
        - HTTPException 404: If the user with the provided login is not found.
        - HTTPException 401: If the provided password is invalid.
    """
    command = SignInCommand(
        login=sign_in_data.login,
        password=Password(hashed=sign_in_data.password, is_hashed=False),  # Password will be hashed on init
    )

    try:
        user = await user_service.sign_in_user(command)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except InvalidPassword:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    # The create_access_token function uses the configured expiry time by default
    access_token = create_access_token(data={"sub": user.login})

    return SignInOutput(id=user.id, login=user.login, token=access_token)
