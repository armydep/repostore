from fastapi.responses import JSONResponse
import httpx
from typing import Optional
from fastapi import Request, Response
from app.core.config import settings
import logging

logger = logging.getLogger("remote_client")


class RemoteClientService:
    _storagerootpath: str = settings.storage_path

    @classmethod
    def getResource(cls, url: str, request: Request) -> Optional[Response]:
        try:
            with httpx.Client() as client:
                if request.method == "HEAD":
                    response = client.head(url)
                    return Response(content=b"", headers=dict(response.headers), status_code=response.status_code)

                upstream_response = client.get(url)
        except httpx.RequestError as exc:
            logger.error(f"Failed to proxy request to {url}: {str(exc)}")
            return JSONResponse(
                status_code=502,
                content={"error": "Failed to fetch from upstream", "details": str(exc)},
            )

        response_headers = {k: v for k, v in upstream_response.headers.items() if k.lower() != "content-length"}

        if upstream_response.headers.get("Content-Type", "").startswith("application/java-archive"):
            body = upstream_response.content
        else:
            body = upstream_response.text

        resource = Response(content=body, headers=response_headers, status_code=upstream_response.status_code)
        return resource
