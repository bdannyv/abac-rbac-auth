from api.v1.authentication.schemas import SignUpInput, SignUpOutput
from domain.user.command import SignUpCommand
from domain.user.service import UserDomainService, user_service_factory
from fastapi import APIRouter
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
