from typing import Dict

class Artifact:
    def __init__(self, content: bytes, metadata: Dict[str, str]):
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        return f"Resource(content_length={len(self.content)}, metadata={self.metadata})"