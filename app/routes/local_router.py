import logging
from fastapi import APIRouter, Request
from app.services.local_repo_service import LocalRepoService

router = APIRouter(prefix="/local", tags=["Local API"])

logger = logging.getLogger("local_router")


@router.put("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}")
async def deploy(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    logger.info("deploy request")
    response = await LocalRepoService.deployResource(repoName, groupId, artifactId, version, name, request)
    return response


@router.api_route("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def get_resource(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    resource = LocalRepoService.getLocalResource(repoName, groupId, artifactId, version, name)
    if resource.status_code == 404:
        raise resource
    return resource
