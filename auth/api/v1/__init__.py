from api.v1.authentication.controllers import authentication
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(authentication)
