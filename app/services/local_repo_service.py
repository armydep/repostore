from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from app.services.repo_service import RepoService
from app.services.cache_service import CacheService
import logging

logger = logging.getLogger("local_repo_service")


class LocalRepoService:
    # _remote_repos = {"maven-remote-1"}
    # _local_repos = {"maven-local-1"}
    # _virtual_repos = {"maven-virtual-1"}

    @classmethod
    async def deployResource(cls, repoName, groupId, artifactId, version, name, request: Request) -> Response:
        if not RepoService.is_exist_local(repoName):
            logger.warning(f"Forbidden repoName access attempt: {repoName}")
            raise HTTPException(status_code=404, detail="Repository not found")
        # logger.info(f"Deploying resource: {groupId}/{artifactId}/{version}/{name}")
        content = await request.body()
        resource = Response(content=content, headers={})
        CacheService.put("maven", "local", repoName, groupId, artifactId, version, name, resource)
        return JSONResponse(status_code=200, content="ok")

    @classmethod
    def getLocalResource(cls, repoName, groupId, artifactId, version, name) -> Response:
        if not RepoService.is_exist_local(repoName):
            logger.warning(f"Forbidden repoName access attempt: {repoName}")
            raise HTTPException(status_code=404, detail="Repository not found")
        resource = CacheService.getResource("maven", "local", repoName, groupId, artifactId, version, name)
        if resource is None:
            return HTTPException(status_code=404, detail="Resource not found")
        return resource
