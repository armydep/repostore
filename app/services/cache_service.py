from typing import Optional, Tuple
from fastapi import Response
import threading
import os

from app.core.config import settings
import logging

logger = logging.getLogger("cache_service")

class CacheService:
    _storagerootpath: str = settings.storage_path
    _lock = threading.Lock()

    @classmethod
    def _build_file_path(cls, groupId: str, artifactId: str, version: str, name: str) -> str:
        return os.path.join(cls._storagerootpath, groupId.replace('.', '/'), artifactId, version, name)

    @classmethod
    def getResource(cls, groupId: str, artifactId: str, version: str, name: str) -> Optional[Response]:
        return None
        file_path = cls._build_file_path(groupId, artifactId, version, name)
        if os.path.isfile(file_path):
            with cls._lock:
                with open(file_path, "rb") as f:
                    content = f.read()
            metadata = {
                "Content-Length": str(len(content)),
                "Content-Type": "application/octet-stream"
            }
            return Response(content=content, headers=metadata)
        return None

    @classmethod
    def put(cls, groupId: str, artifactId: str, version: str, name: str, resource: Response) -> None:
        return
        file_path = cls._build_file_path(groupId, artifactId, version, name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with cls._lock:
            with open(file_path, "wb") as f:
                f.write(resource.body)

    @classmethod
    def clear(cls) -> None:
        pass  # No clear method needed for filesystem storage