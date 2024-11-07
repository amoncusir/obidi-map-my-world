from fastapi import APIRouter, FastAPI

# Module routers
from src.module.common.application.http import router as common_router
from src.module.geoquerier.application.http import router as geoquerier_router
from src.module.manager.application.http import router as manager_router
from src.module.recommendation.application.http import router as recommendation_router

router = APIRouter()

router.include_router(common_router)
router.include_router(geoquerier_router)
router.include_router(manager_router)
router.include_router(recommendation_router)


def build_fastapi(**kwargs) -> FastAPI:
    api = FastAPI(**kwargs)

    api.include_router(router)

    return api
