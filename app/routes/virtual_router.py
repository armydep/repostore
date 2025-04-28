import logging
from fastapi import APIRouter, Request, Response, HTTPException
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.repo_service import RepoService

router = APIRouter(prefix="/virtual", tags=["Virtual API"])

logger = logging.getLogger("proxy_service")


@router.put("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}")
async def maven_virtual_deploy(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    if not RepoService.is_allowed(repoName):
        logger.warning(f"Forbidden repoName access attempt: {repoName}")
        raise HTTPException(status_code=404, detail="Repository not found")
    # logger.info(f"Deploying resource: {groupId}/{artifactId}/{version}/{name}")
    content = await request.body()
    resource = Response(content=content, headers={})
    CacheService.put("maven-local", groupId, artifactId, version, name, resource)
    return {"message": "Resource deployed successfully."}


@router.api_route("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def maven_virtual_get(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    if not RepoService.is_allowed(repoName):
        logger.warning(f"Forbidden repoName access attempt: {repoName}")
        raise HTTPException(status_code=404, detail="Repository not found")
    url = f"{settings.url}/{groupId}/{artifactId}/{version}/{name}"
    # logger.info(f"Proxying request: {request.method} {url}")
    resource = CacheService.getResource("maven-local", groupId, artifactId, version, name)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
