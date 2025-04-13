from domain.user.exc import EmailAlreadyExists
from fastapi import HTTPException
from starlette import status


class AuthenticationErrorHandler:
    def __call__(self, request, exc):
        ...


class EmailAlreadyExistsHandler(AuthenticationErrorHandler):
    def __call__(self, request, exc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


exception_handlers_map = ((EmailAlreadyExists, EmailAlreadyExistsHandler),)
