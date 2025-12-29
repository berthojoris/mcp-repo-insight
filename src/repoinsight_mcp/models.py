"""Pydantic models for RepoInsight MCP."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RepositoryMetadata:
    """Repository metadata from GitHub."""

    owner: str
    name: str
    full_name: str
    description: Optional[str]
    stars: int
    forks: int
    language: Optional[str]
    default_branch: str
    clone_url: str
    updated_at: str


@dataclass
class DocumentResult:
    """Search result for documentation."""

    path: str
    title: str
    content: str
    score: float


@dataclass
class IssueResult:
    """Issue or pull request summary."""

    number: int
    title: str
    state: str
    created_at: str
    updated_at: str
    author: str
    url: str
    is_pull_request: bool = False


@dataclass
class Contributor:
    """Repository contributor."""

    login: str
    contributions: int
    avatar_url: str


@dataclass
class FileMetadata:
    """File metadata."""

    path: str
    size: int
    language: Optional[str]
    encoding: str


@dataclass
class TreeNode:
    """Repository tree node."""

    name: str
    path: str
    type: str
    size: Optional[int] = None
    children: Optional[list["TreeNode"]] = None


@dataclass
class GetRepoSummaryInput:
    """Input for get_repo_summary tool."""

    repository: str


@dataclass
class SearchDocInput:
    """Input for search_doc tool."""

    repository: str
    query: str
    limit: int = 10


@dataclass
class GetRepoStructureInput:
    """Input for get_repo_structure tool."""

    repository: str
    path: str = ""
    depth: int = 4


@dataclass
class ReadFileInput:
    """Input for read_file tool."""

    repository: str
    path: str


@dataclass
class GetRepoSummaryOutput:
    """Output for get_repo_summary tool."""

    repository: dict[str, Any]
    readme_summary: Optional[str]
    recent_issues: list[dict[str, Any]]
    recent_pull_requests: list[dict[str, Any]]
    top_contributors: list[dict[str, Any]]
    languages: dict[str, int]
    total_files: int


@dataclass
class SearchDocOutput:
    """Output for search_doc tool."""

    repository: dict[str, Any]
    documents: list[dict[str, Any]]
    issues: list[dict[str, Any]]
    pull_requests: list[dict[str, Any]]
    contributors: list[dict[str, Any]]


@dataclass
class GetRepoStructureOutput:
    """Output for get_repo_structure tool."""

    root: str
    structure: list[dict[str, Any]]
    stats: dict[str, Any]


@dataclass
class ReadFileOutput:
    """Output for read_file tool."""

    path: str
    language: Optional[str]
    size: int
    encoding: str
    content: str
