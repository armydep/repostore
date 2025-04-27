import httpx
import logging
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from app.core.config import settings

router = APIRouter()

logger = logging.getLogger("proxy_service")

@router.api_route("/maven2/{full_path:path}", methods=["GET", "HEAD"])
def proxy_maven(full_path: str, request: Request):
    url = f"{settings.url}/{full_path}"
    logger.info(f"Proxying request: {request.method} {url}")

    try:
        with httpx.Client(timeout=5.0) as client:
            if request.method == "HEAD":
                response = client.head(url)
                return Response(content=b"", headers=dict(response.headers))

            upstream_response = client.get(url)
            response_headers = {
                k: v for k, v in upstream_response.headers.items()
                if k.lower() != "content-length"
            }

            if upstream_response.headers.get("Content-Type", "").startswith("application/java-archive"):
                body = upstream_response.content
            else:
                body = upstream_response.text

            return Response(content=body, headers=response_headers)

    except httpx.RequestError as exc:
        logger.error(f"Failed to proxy request to {url}: {str(exc)}")
        return JSONResponse(
            status_code=502,
            content={"error": "Failed to fetch from upstream", "details": str(exc)},
        )