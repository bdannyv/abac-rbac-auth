from fastapi import APIRouter, Depends, exceptions, responses, status
from sqlalchemy.ext.asyncio import AsyncSession

from features.authentication.api.v1.schemas import (
    LoginAPIRequestModel,
    LoginAPIResponseModel,
    SignedUPModel,
    SignUpFormModel,
)
from features.authentication.commands import UserCreateCommand, UserLoginCommand
from features.authentication.jwt_handler import JWTService
from settings.auth import auth_settings
from settings.base import app_settings

authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])


def get_user_login_command(db_session: AsyncSession = Depends(...)):
    return UserLoginCommand(session=db_session)


@authentication_router.post(
    path="/login",
    summary="User login-password authentication",
    description="User login-password authentication. In case of successful authentication server responds with pair "
    "of JWT tokens",
    responses={
        status.HTTP_200_OK: {"model": LoginAPIResponseModel},
        status.HTTP_401_UNAUTHORIZED: {"description": "Wrong credentials"},
    },
)
async def log_in(
    credentials: LoginAPIRequestModel,
    command: UserLoginCommand = Depends(get_user_login_command),
    jwt_service: JWTService = Depends(JWTService),
):
    user, is_authenticated = command.execute(payload=credentials)
    if not is_authenticated:
        raise exceptions.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access, refresh = jwt_service.issue_token_pair(ent_id=user.id)

    response = responses.ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access": access,
        },
    )

    response.set_cookie(
        key="refresh",
        value=refresh,
        httponly=True,
        samesite="strict",
        expires=auth_settings.jwt_refresh_ttl,
        secure=app_settings.cookie_secure,
    )

    return response


def get_user_create_command(db_session: AsyncSession = Depends(...)):
    return UserCreateCommand(session=db_session)


@authentication_router.post(
    "/signup",
    summary="User registration",
    response_model=SignedUPModel,
    responses={status.HTTP_201_CREATED: {"description": "Successfully registered", "model": SignedUPModel}},
)
async def sign_up(sing_up_form: SignUpFormModel, command: UserCreateCommand = Depends(get_user_create_command)):
    created_user_id = await command.execute(payload=sing_up_form)
    return SignedUPModel(id=created_user_id)


@authentication_router.post(
    "/logout",
    summary="User logout",
    responses={status.HTTP_308_PERMANENT_REDIRECT: {"description": "Successfully logged out"}},
)
async def log_out():
    ...
