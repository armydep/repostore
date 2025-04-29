class RepoService:
    _remote_repos = {"maven-remote-1"}
    _local_repos = {"maven-local-1"}
    _virtual_repos = {"maven-virtual-1"}

    @classmethod
    def is_exist_remote(cls, repo_name: str) -> bool:
        return repo_name in cls._remote_repos

    @classmethod
    def is_exist_local(cls, repo_name: str) -> bool:
        return repo_name in cls._local_repos

    @classmethod
    def is_exist_virtual(cls, repo_name: str) -> bool:
        return repo_name in cls._virtual_repos

    # ------------- virtual -----------
    @classmethod
    def get_virtual_local_repos(cls, repo_name: str) -> list[str]:
        return ["maven-local-1"]

    @classmethod
    def get_virtual_remote_repos(cls, repo_name: str) -> list[str]:
        return ["maven-remote-1"]

    @classmethod
    def get_virtual_default_local_repo(cls, repo_name: str) -> str:
        return "maven-local-1"
