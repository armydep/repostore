import logging
from fastapi import APIRouter, Request, Response, HTTPException
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.remote_client_service import RemoteClientService
from app.services.repo_service import RepoService
from app.services.remote_repo_service import RemoteRepoService

router = APIRouter(prefix="/remote", tags=["Remote API"])

logger = logging.getLogger("remote_router")


@router.api_route("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def maven_remote(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    resource = RemoteRepoService.getRemoteResource(repoName, groupId, artifactId, version, name, request)
    if resource.status_code != 200:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


# archetype-catalog.xml. mvn generate package
@router.api_route("/{repoName}/{name}", methods=["GET", "HEAD"])
def maven_remote_get_catalog(repoName: str, name: str, request: Request):
    resource = RemoteRepoService.getRemoteCatalog(repoName, name, request)
    if resource.status_code != 200:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
