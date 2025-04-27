from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from typing import Optional
import httpx
import hashlib
from app.routes.proxy_router import router as proxy_routes
from app.core.config import settings
from app.core.logger import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    print(f"🚀 Starting app with URL: {settings.url}")
    yield
    print("🛑 App shutting down.")


app = FastAPI(lifespan=lifespan)


app.include_router(proxy_routes)