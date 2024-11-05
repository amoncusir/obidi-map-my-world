from fastapi import APIRouter

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/health", status_code=204)
async def health():
    pass
