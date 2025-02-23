import typing

from fastapi import APIRouter, HTTPException, status
from features.authentication.api.v1.controllers import authentication_router
from features.authentication.exc import EmailAlreadyExists, UserNotFoundError
from jwt.exceptions import InvalidTokenError

authentication_domain_router = APIRouter(prefix="")

authentication_domain_router.include_router(authentication_router, prefix="/v1")


class AuthenticationErrorHandler:
    def __call__(self, request, exc):
        ...


class UserNotFoundErrorHandler(AuthenticationErrorHandler):
    def __call__(self, request, exc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.msg)


class InvalidJWTErrorHandler(AuthenticationErrorHandler):
    def __call__(self, request, exc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.args[0])


class EmailAlreadyExistsHandler(AuthenticationErrorHandler):
    def __call__(self, request, exc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.msg)


exception_handlers_map: tuple[tuple[typing.Type[Exception], typing.Type[AuthenticationErrorHandler]], ...] = (
    (UserNotFoundError, UserNotFoundErrorHandler),
    (InvalidTokenError, InvalidJWTErrorHandler),
    (EmailAlreadyExists, EmailAlreadyExistsHandler),
)
