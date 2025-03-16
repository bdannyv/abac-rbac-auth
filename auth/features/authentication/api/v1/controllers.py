import typing

from fastapi import APIRouter, Depends, exceptions, responses, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from features.authentication.api.v1.schemas import LoginAPIRequestModel, SignedUPModel, SignUpFormModel
from features.authentication.commands import UserCreateCommand, UserLoginCommand, UserLogoutCommand
from features.authentication.jwt_service import JWTService
from features.utils import ACCESS_TOKEN_COOKIE_NAME, REFRESH_TOKEN_COOKIE_NAME, access_token_cookie
from infra.data_storage import get_session
from settings.auth import auth_settings
from settings.base import app_settings
from sqlalchemy.ext.asyncio import AsyncSession

authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])


def user_login_command_dependency(db_session: AsyncSession = Depends(get_session)) -> UserLoginCommand:
    return UserLoginCommand(session=db_session)


def get_user_create_command_dependency(db_session: AsyncSession = Depends(get_session)):
    return UserCreateCommand(session=db_session)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/authentication/login")


@authentication_router.post(
    path="/login",
    summary="User login-password authentication",
    description="User login-password authentication. In case of successful authentication server responds with pair "
    "of JWT tokens",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Wrong credentials"},
    },
    status_code=status.HTTP_200_OK,
)
async def log_in(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    command: typing.Annotated[UserLoginCommand, Depends(user_login_command_dependency)],
    jwt_service: typing.Annotated[JWTService, Depends(JWTService)],
):
    user, is_authenticated = await command.execute(
        payload=LoginAPIRequestModel(email=form_data.username, password=form_data.password)
    )

    if not is_authenticated:
        raise exceptions.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access, access_content, refresh, refresh_content = jwt_service.issue_token_pair(ent_id=user.id)

    response = responses.ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Success"},  # "access_token": access, "token_type": "bearer"}
    )

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh,
        httponly=True,
        samesite="lax",
        expires=auth_settings.jwt_refresh_ttl,
        secure=app_settings.cookie_secure,
    )

    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access,
        httponly=True,
        samesite="lax",
        expires=auth_settings.jwt_access_ttl,
        secure=app_settings.cookie_secure,
    )

    return response


@authentication_router.post(
    "/signup",
    summary="User registration",
    response_model=SignedUPModel,
    responses={status.HTTP_201_CREATED: {"description": "Successfully registered", "model": SignedUPModel}},
)
async def sign_up(
    sing_up_form: SignUpFormModel, command: UserCreateCommand = Depends(get_user_create_command_dependency)
):
    created_user_id = await command.execute(payload=sing_up_form)
    return SignedUPModel(id=created_user_id)


@authentication_router.post(
    "/logout",
    summary="User logout",
    responses={status.HTTP_308_PERMANENT_REDIRECT: {"description": "Successfully logged out"}},
)
async def log_out(
    token: typing.Annotated[str, Depends(access_token_cookie)],
    _: typing.Annotated[str, Depends(oauth2_scheme)],  # to see authorize button on Swagger (for dev purposes)
    command: UserLogoutCommand = Depends(UserLogoutCommand),
):
    await command.execute(token)
    return responses.ORJSONResponse(status_code=status.HTTP_200_OK, content="Successfully logged out")
