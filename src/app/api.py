from fastapi import FastAPI

from src.app.router import router


def build_fastapi() -> FastAPI:

    api = FastAPI(title="OrbidiMapMyWorld")

    api.include_router(router)

    return api
