from fastapi import FastAPI

from src.app.fast_api_router import router


def build_fastapi(**kwargs) -> FastAPI:
    api = FastAPI(**kwargs)

    api.include_router(router)

    return api
