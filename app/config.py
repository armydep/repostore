# config.py

class Settings:
    def __init__(self):
        # Default values
        self.url = "https://repo1.maven.org/maven2"
        self.url1 = "https://repo.maven.apache.org/maven2"
        self.storage_path = "/tmp/storage"

settings = Settings()