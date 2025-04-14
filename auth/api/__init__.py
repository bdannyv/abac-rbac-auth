from api.v1 import v1_router
from fastapi import APIRouter

base_router = APIRouter(prefix="")
base_router.include_router(v1_router)
