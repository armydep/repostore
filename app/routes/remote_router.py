import logging
from fastapi import APIRouter, Request, Response, HTTPException
from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.remote_client_service import RemoteClientService

router = APIRouter()

logger = logging.getLogger("proxy_service")

#archetype-catalog.xml. mvn generate package
@router.api_route("/maven2/{name}", methods=["GET", "HEAD"])
def proxy_maven1(name: str, request: Request):
    url = f"{settings.url}/{name}"
    logger.info(f"Proxying request1: {request.method} {url}")
    resource = CacheService.getResource("", "", "", name)
    if resource is None:
        resource = RemoteClientService.getResource(url, request)
        if(resource.status_code == 200) and request.method == "GET":
            CacheService.put("", "", "", name, resource)
    return resource


@router.api_route("/maven2/{groupId:path}/{artifactId}/{version}/{name}", methods=["GET", "HEAD"])
def proxy_maven(groupId: str, artifactId: str, version: str, name: str, request: Request):
    url = f"{settings.url}/{groupId}/{artifactId}/{version}/{name}"
    logger.info(f"Proxying request: {request.method} {url}")
    resource = CacheService.getResource(groupId, artifactId, version, name)
    if url.endswith("maven-metadata.xml"):
        raise HTTPException(status_code=404, detail="Resource not found")
    # should be removed when local repository added
    if resource is None: #and not url.endswith("maven-metadata.xml"):
        resource = RemoteClientService.getResource(url, request)
        if(resource.status_code == 200) and request.method == "GET":
            CacheService.put(groupId, artifactId, version, name, resource)
    return resource

@router.put("/maven2/{groupId:path}/{artifactId}/{version}/{name}")
async def deploy_resource(groupId: str, artifactId: str, version: str, name: str, request: Request):
    logger.info(f"Deploying resource: {groupId}/{artifactId}/{version}/{name}")

    content = await request.body()
    # content_type = request.headers.get("content-type", "application/octet-stream")

    # metadata = {
        # "Content-Type": content_type
        # ,maven-metadata.xml
        # "Content-Length": str(len(content))
    # }

    resource = Response(content=content, headers={})
    CacheService.put(groupId, artifactId, version, name, resource)

    return {"message": "Resource deployed successfully."}