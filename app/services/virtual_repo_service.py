from fastapi import Request, Response, HTTPException
from app.services.repo_service import RepoService
from app.services.remote_repo_service import RemoteRepoService
from app.services.local_repo_service import LocalRepoService
import logging

logger = logging.getLogger("virtual_repo_service")


class VirtualRepoService:
    # _remote_repos = {"maven-remote-1"}
    # _local_repos = {"maven-local-1"}
    # _virtual_repos = {"maven-virtual-1"}

    @classmethod
    def getVirtualResource(cls, repoName, groupId, artifactId, version, name, request: Request) -> Response:
        if not RepoService.is_exist_virtual(repoName):
            logger.warning(f"Forbidden repoName access attempt: {repoName}")
            raise HTTPException(status_code=404, detail="Repository not found")
        # url = f"{settings.url}/{groupId}/{artifactId}/{version}/{name}"
        # logger.info(f"Proxying request: {request.method} {url}")
        resource = None
        local_repos = RepoService.get_virtual_local_repos(repoName)
        for local_repo in local_repos:
            resource = LocalRepoService.getLocalResource(local_repo, groupId, artifactId, version, name)
            if resource is not None and resource.status_code == 200:
                break

        if resource is None or resource.status_code != 200:
            remote_repos = RepoService.get_virtual_remote_repos(repoName)
            for remote_repo in remote_repos:
                resource = RemoteRepoService.getRemoteResource(remote_repo, groupId, artifactId, version, name, request)
                if resource is not None and resource.status_code == 200:
                    break

        return resource

    @classmethod
    def getVirtualRemoteCatalog(cls, repoName, name, request: Request) -> Response:
        if not RepoService.is_exist_virtual(repoName):
            logger.warning(f"Forbidden repoName access attempt: {repoName}")
            raise HTTPException(status_code=404, detail="Repository not found")
        # url = f"{settings.url}/{groupId}/{artifactId}/{version}/{name}"
        # logger.info(f"Proxying request: {request.method} {url}")
        resource = None
        remote_repos = RepoService.get_virtual_remote_repos(repoName)
        for remote_repo in remote_repos:
            resource = RemoteRepoService.getRemoteCatalog(remote_repo, name, request)
            if resource is not None and resource.status_code == 200:
                break
        return resource

    @classmethod
    async def deployResource(cls, repoName, groupId, artifactId, version, name, request: Request) -> Response:
        if not RepoService.is_exist_virtual(repoName):
            logger.warning(f"Forbidden repoName access attempt: {repoName}")
            raise HTTPException(status_code=404, detail="Repository not found")
        logger.info(f"Deploying resource: {groupId}/{artifactId}/{version}/{name}")
        local_repo = RepoService.get_virtual_default_local_repo(repoName)
        response = await LocalRepoService.deployResource(local_repo, groupId, artifactId, version, name, request)
        return response
