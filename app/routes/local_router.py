import logging
from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.repo_service import RepoService
from app.services.local_repo_service import LocalRepoService

router = APIRouter(prefix="/local", tags=["Local API"])

logger = logging.getLogger("local_router")


@router.put("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}")
async def maven_local_deploy(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    logger.info("deploy request")
    response = await LocalRepoService.getDeployResource(repoName, groupId, artifactId, version, name, request)
    return response

@router.api_route("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def maven_local_get(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    resource = LocalRepoService.getLocalResource(repoName, groupId, artifactId, version, name)
    return resource