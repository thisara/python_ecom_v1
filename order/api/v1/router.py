from fastapi import APIRouter
from api.v1 import health, order

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(order.router)