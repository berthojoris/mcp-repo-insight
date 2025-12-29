"""Repository caching and local storage management."""

import shutil
import time
from pathlib import Path
from typing import Optional

from git import Repo

from .config import CACHE_TTL_SECONDS, REPOS_DIR
from .exceptions import GitHubAPIError, InvalidRepositoryError
from .github_client import GitHubClient
from .models import RepositoryMetadata


class RepositoryCache:
    """Manages local caching of GitHub repositories."""

    def __init__(self, github_client: GitHubClient) -> None:
        """Initialize repository cache.

        Args:
            github_client: GitHub API client.
        """
        self._github_client = github_client
        REPOS_DIR.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, owner: str, name: str) -> Path:
        """Get local cache path for repository.

        Args:
            owner: Repository owner.
            name: Repository name.

        Returns:
            Path to local cache directory.
        """
        return REPOS_DIR / f"{owner}_{name}"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cached repository is still valid.

        Args:
            cache_path: Path to cached repository.

        Returns:
            True if cache is valid, False otherwise.
        """
        if not cache_path.exists():
            return False

        cache_time = cache_path.stat().st_mtime
        current_time = time.time()
        age_seconds = current_time - cache_time

        return age_seconds < CACHE_TTL_SECONDS

    def get_repository(self, owner: str, name: str) -> tuple[Path, RepositoryMetadata]:
        """Get repository from cache or clone if needed.

        Args:
            owner: Repository owner.
            name: Repository name.

        Returns:
            Tuple of (cache_path, metadata).

        Raises:
            GitHubAPIError: If repository cannot be fetched.
        """
        cache_path = self._get_cache_path(owner, name)

        metadata = self._github_client.get_repository_metadata(owner, name)

        if self._is_cache_valid(cache_path):
            self._update_cache_timestamp(cache_path)
            return cache_path, metadata

        return self._clone_repository(metadata, cache_path), metadata

    def _clone_repository(
        self, metadata: RepositoryMetadata, cache_path: Path
    ) -> Path:
        """Clone repository to local cache.

        Args:
            metadata: Repository metadata.
            cache_path: Target cache path.

        Returns:
            Path to cloned repository.

        Raises:
            GitHubAPIError: If clone fails.
        """
        if cache_path.exists():
            shutil.rmtree(cache_path)

        try:
            Repo.clone_from(
                metadata.clone_url,
                cache_path,
                depth=1,
                branch=metadata.default_branch,
            )
            return cache_path
        except Exception as e:
            if cache_path.exists():
                shutil.rmtree(cache_path)
            raise GitHubAPIError(f"Failed to clone repository: {e}")

    def _update_cache_timestamp(self, cache_path: Path) -> None:
        """Update cache timestamp to current time.

        Args:
            cache_path: Path to cached repository.
        """
        cache_path.touch(exist_ok=True)

    def clear_cache(self, owner: Optional[str] = None, name: Optional[str] = None) -> None:
        """Clear repository cache.

        Args:
            owner: Optional repository owner. If None, clears all caches.
            name: Optional repository name. Required if owner is provided.
        """
        if owner and name:
            cache_path = self._get_cache_path(owner, name)
            if cache_path.exists():
                shutil.rmtree(cache_path)
        elif not owner:
            if REPOS_DIR.exists():
                shutil.rmtree(REPOS_DIR)
                REPOS_DIR.mkdir(parents=True, exist_ok=True)
