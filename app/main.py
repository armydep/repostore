import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import setup_logging
from app.routes.remote_router import router as remote_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger("lifespan")
    logger.info(f"🚀 Starting app with URL: {settings.url}")
    yield
    print("🛑 App shutting down.")

app = FastAPI(lifespan=lifespan)

app.include_router(remote_router)