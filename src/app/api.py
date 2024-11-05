from fastapi import FastAPI

from src.app import application
from src.app.router import router


def build_fastapi() -> FastAPI:
    # Must be the first component to instance
    app = application()

    api = FastAPI(
        title="OrbidiMapMyWorld",
        debug=app.debug,
    )

    api.include_router(router)

    return api
