from fastapi import APIRouter

from .category import router as category_router

# Module routers
from .place import router as place_router

router = APIRouter()
router.include_router(place_router)
router.include_router(category_router)
