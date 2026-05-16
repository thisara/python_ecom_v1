import httpx
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from api.v1.router import api_router
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()

load_dotenv()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/order")