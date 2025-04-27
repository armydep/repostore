from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from typing import Optional
import httpx
import hashlib

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting app with URL: {settings.url}")
    yield
    print("🛑 App shutting down.")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to RepoStore 🚀"}


@app.api_route("/maven2/{full_path:path}", methods=["GET", "HEAD"])
def handle_mypath(full_path: str, request: Request):
    url = f"{settings.url}/{full_path}"
    print(f"Request_IN from client: {full_path}. {request.method}. fwd url: {url}")
    try:
        with httpx.Client() as client:
            response = client.get(url)
            if request.method == "HEAD":
                return Response(content=b"", headers=dict(response.headers))                
            response_body = response.text
            if response.headers.get("Content-Type", "") == "application/java-archive":
                response_body = response.content
            return Response(content=response_body, headers=dict(response.headers))
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {str(exc)}")
        return JSONResponse(
            status_code=502,
            content={"error": "Failed to fetch from url1", "details": str(exc)},
        )

    print("Unknown request type. {full_path}. {request.method}")
    return {
        "requested_subpath": full_path,
        "method": request.method,
        "info": "Request unsupported",
    }
