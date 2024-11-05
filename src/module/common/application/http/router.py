from fastapi import APIRouter

# Module routers
from .status import router as status_router

router = APIRouter()
router.include_router(status_router)
