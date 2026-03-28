from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
def service_status():
    return {"status":"up"}