import logging
from fastapi import APIRouter, Request
from app.core.config import settings
from app.services.virtual_repo_service import VirtualRepoService

router = APIRouter(prefix="/virtual", tags=["Virtual API"])

logger = logging.getLogger("virtual_router")


@router.api_route("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def get_resource(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    logger.info("get resource")
    resource = VirtualRepoService.getVirtualResource(repoName, groupId, artifactId, version, name, request)
    return resource


# archetype-catalog.xml. mvn generate package
@router.api_route("/{repoName}/{name}", methods=["GET", "HEAD"])
def get_catalog(repoName: str, name: str, request: Request):
    resource = VirtualRepoService.getVirtualRemoteCatalog(repoName, name, request)
    return resource


@router.put("/{repoName}/{groupId:path}/{artifactId}/{version}/{name}")
async def deploy(repoName: str, groupId: str, artifactId: str, version: str, name: str, request: Request):
    logger.info("deploy request")
    response = await VirtualRepoService.deployResource(repoName, groupId, artifactId, version, name, request)
    return response

