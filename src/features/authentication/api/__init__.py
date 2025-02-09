import typing

from fastapi import APIRouter, HTTPException, status

from features.authentication.api.v1.controllers import authentication_router
from features.authentication.exc import AuthenticationCommandError, UserNotFoundError

authentication_domain_router = APIRouter(prefix="")

authentication_domain_router.include_router(authentication_router, prefix="/v1")


class AuthenticationErrorHandler(typing.Protocol):
    def __call__(self, request, exc):
        ...


class UserNotFoundErrorHandler(AuthenticationErrorHandler):
    def __call__(self, request, exc):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


exception_handlers_map: tuple[
    tuple[typing.Type[AuthenticationCommandError], typing.Type[AuthenticationErrorHandler]]
] = ((UserNotFoundError, UserNotFoundErrorHandler),)
