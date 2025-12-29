"""Configuration and constants for RepoInsight MCP."""

from pathlib import Path
from typing import Final

HOME_DIR: Final[Path] = Path.home()
CACHE_DIR: Final[Path] = HOME_DIR / ".repoinsight"
REPOS_DIR: Final[Path] = CACHE_DIR / "repos"
DB_FILE: Final[Path] = CACHE_DIR / "metadata.db"

MAX_FILE_SIZE_BYTES: Final[int] = 1024 * 1024
MAX_RECURSION_DEPTH: Final[int] = 10
CACHE_TTL_SECONDS: Final[int] = 86400

GITHUB_API_BASE: Final[str] = "https://api.github.com"
DEFAULT_SEARCH_LIMIT: Final[int] = 10

def ensure_cache_directories() -> None:
    """Create cache directories if they don't exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
