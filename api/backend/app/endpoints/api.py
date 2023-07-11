from fastapi import APIRouter

from app.endpoints.auth import router as auth_router


router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
