from fastapi import APIRouter

# Module routers
from src.module.common.application.http import router as common_router
from src.module.geoquerier.application.http import router as geoquerier_router
from src.module.placemanager.application.http import router as placemanager_router
from src.module.recommendation.application.http import router as recommendation_router

router = APIRouter()

router.include_router(common_router)
router.include_router(geoquerier_router)
router.include_router(placemanager_router)
router.include_router(recommendation_router)
