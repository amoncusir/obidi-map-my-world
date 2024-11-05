from fastapi import APIRouter

# Module routers
from .place import router as place_router

router = APIRouter()
router.include_router(place_router)
