from pydantic_settings import BaseSettings
import platform


class Settings(BaseSettings):
    url: str = "https://repo1.maven.org/maven2"
    url1: str = "https://repo.maven.apache.org/maven2"
    if platform.system() == "Windows":
        storage_path: str = "C:\\tmp\\repostore-mvn-storage"
    else:
        storage_path: str = "/tmp/repostore-mvn-storage"

    class Config:
        env_file = ".env"


settings = Settings()
