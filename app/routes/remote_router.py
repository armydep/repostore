import logging
from fastapi import APIRouter, Request, Response, HTTPException
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.remote_client_service import RemoteClientService
from app.services.repo_service import RepoService

router = APIRouter(prefix="/remote", tags=["Remote API"])

logger = logging.getLogger("proxy_service")


# archetype-catalog.xml. mvn generate package
@router.api_route("/{repoName}/{name}", methods=["GET", "HEAD"])
def maven_remote_get_catalog(repoName: str, name: str, request: Request):
    if not RepoService.is_exist_remote(repoName):
        logger.warning(f"Forbidden repoName access attempt: {repoName}")
        raise HTTPException(status_code=404, detail="Repository not found")
    url = f"{settings.url}/{name}"
    # logger.info(f"Proxying request1: {request.method} {url}")
    resource = CacheService.getResource("maven", "remote", repoName, "", "", "", name)
    if resource is None:
        resource = RemoteClientService.getResource(url, request)
        if (resource.status_code == 200) and request.method == "GET":
            CacheService.put("maven", "remote", repoName, "", "", "", name, resource)
    return resource


@router.api_route("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def maven_remote(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    if not RepoService.is_exist_remote(repoName):
        logger.warning(f"Forbidden repoName access attempt: {repoName}")
        raise HTTPException(status_code=404, detail="Repository not found")
    url = f"{settings.url}/{groupId}/{artifactId}/{version}/{name}"
    # logger.info(f"Proxying request: {request.method} {url}")
    resource = CacheService.getResource("maven", "remote", repoName, groupId, artifactId, version, name)
    # ?
    # if url.endswith("maven-metadata.xml"):
    #     raise HTTPException(status_code=404, detail="Resource not found")
    # should be removed when local repository added
    if resource is None:  # and not url.endswith("maven-metadata.xml"):
        resource = RemoteClientService.getResource(url, request)
        if (resource.status_code == 200) and request.method == "GET":
            CacheService.put("maven", "remote", repoName, groupId, artifactId, version, name, resource)
    return resource
