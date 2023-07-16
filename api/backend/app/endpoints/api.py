from fastapi import APIRouter

from app.endpoints.auth import router as auth_router
from app.endpoints.posts import router as posts_router
from app.endpoints.reactions import router as reactions_router


router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
router.include_router(posts_router)
router.include_router(reactions_router)
