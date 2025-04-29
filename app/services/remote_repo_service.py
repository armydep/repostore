from typing import Optional, Tuple
from fastapi import Request, Response, HTTPException
from app.services.repo_service import RepoService
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.remote_client_service import RemoteClientService
import logging

logger = logging.getLogger("remote_repo_service")


class RemoteRepoService:
    # _remote_repos = {"maven-remote-1"}
    # _local_repos = {"maven-local-1"}
    # _virtual_repos = {"maven-virtual-1"}

    @classmethod
    def getRemoteResource(
        cls, repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request
    ) -> Response:
        if not RepoService.is_exist_remote(repoName):
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

    @classmethod
    def getRemoteCatalog(cls, repoName: str, name: str, request: Request) -> Response:
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
