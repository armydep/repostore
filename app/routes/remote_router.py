import logging
from fastapi import APIRouter, Request
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.remote_client_service import RemoteClientService

router = APIRouter()

logger = logging.getLogger("proxy_service")

@router.api_route("/maven-repostore/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def proxy_maven(groupId: str, artifactId: str, version: str, name: str, request: Request):
    url = f"{settings.url}/{groupId}/{artifactId}/{version}/{name}"
    # logger.info(f"Proxying request: {request.method} {url}")
    resource = CacheService.getResource(groupId, artifactId, version, name)
    if resource is None:
        resource = RemoteClientService.getResource(url, request)
        CacheService.put(groupId, artifactId, version, name, resource)
    return resource
