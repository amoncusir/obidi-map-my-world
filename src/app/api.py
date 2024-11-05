from fastapi import FastAPI

from app.router import router


def build_fastapi() -> FastAPI:

    api = FastAPI()

    api.include_router(router)

    return api
