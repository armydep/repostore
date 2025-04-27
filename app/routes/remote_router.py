import httpx
import logging
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.services.cache_service import CacheService

router = APIRouter()

logger = logging.getLogger("proxy_service")

@router.api_route("/maven-repostore/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def proxy_maven(groupId: str, artifactId: str, version: str, name: str, request: Request):
    url = f"{settings.url}/{groupId}/{artifactId}/{version}/{name}"
    logger.info(f"Proxying request: {request.method} {url}")
    resource = CacheService.getResource(groupId, artifactId, version, name)
    if resource is None:
        try:
            with httpx.Client() as client:
                if request.method == "HEAD":
                    response = client.head(url)
                    return Response(content=b"", headers=dict(response.headers))

                upstream_response = client.get(url)
        except httpx.RequestError as exc:
            logger.error(f"Failed to proxy request to {url}: {str(exc)}")
            return JSONResponse(
                status_code=502,
                content={"error": "Failed to fetch from upstream", "details": str(exc)},
            )

        response_headers = {
            k: v
            for k, v in upstream_response.headers.items()
            if k.lower() != "content-length"
        }

        if upstream_response.headers.get("Content-Type", "").startswith(
            "application/java-archive"
        ):
            body = upstream_response.content
        else:
            body = upstream_response.text

        resource = Response(content=body, headers=response_headers)

        CacheService.put(groupId, artifactId, version, name, resource)

    return resource
