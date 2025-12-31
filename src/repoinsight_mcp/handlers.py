"""MCP tool handlers for RepoInsight."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .cache import RepositoryCache
from .config import DEFAULT_SEARCH_LIMIT
from .file_reader import FileReader
from .github_client import GitHubClient
from .models import (
    GetRepoStructureInput,
    GetRepoStructureOutput,
    GetRepoSummaryInput,
    GetRepoSummaryOutput,
    ReadFileInput,
    ReadFileOutput,
    SearchDocInput,
    SearchDocOutput,
)
from .search import DocumentIndexer, SearchIndex


class ToolHandlers:
    """Handlers for MCP tools."""

    def __init__(
        self,
        github_client: GitHubClient,
        repo_cache: RepositoryCache,
        search_index: SearchIndex,
    ) -> None:
        """Initialize tool handlers.

        Args:
            github_client: GitHub API client.
            repo_cache: Repository cache manager.
            search_index: Search index.
        """
        self._github_client = github_client
        self._repo_cache = repo_cache
        self._search_index = search_index
        self._indexer = DocumentIndexer(search_index)

    def handle_get_repo_summary(
        self, params: dict[str, Any]
    ) -> GetRepoSummaryOutput:
        """Handle get_repo_summary tool request.

        Args:
            params: Tool parameters.

        Returns:
            Repository summary.
        """
        input_data = GetRepoSummaryInput(repository=params["repository"])

        owner, name = GitHubClient.parse_repo_url(input_data.repository)
        cache_path, metadata = self._repo_cache.get_repository(owner, name)

        # Get README summary
        readme_summary = self._get_readme_summary(cache_path)

        # Execute parallel tasks
        with ThreadPoolExecutor() as executor:
            # Stats calculation (using tree with stats for efficiency)
            file_reader = FileReader(cache_path)
            stats_future = executor.submit(
                file_reader.get_file_tree_with_stats, "", 1
            )

            # API calls
            issues_future = executor.submit(
                self._github_client.get_recent_issues, owner, name, limit=5
            )
            pr_future = executor.submit(
                self._github_client.get_recent_pull_requests, owner, name, limit=5
            )
            contributors_future = executor.submit(
                self._github_client.get_contributors, owner, name, limit=10
            )

            _, language_stats, total_files = stats_future.result()
            issues = issues_future.result()
            pull_requests = pr_future.result()
            contributors = contributors_future.result()

        return GetRepoSummaryOutput(
            repository={
                "name": metadata.full_name,
                "description": metadata.description,
                "stars": metadata.stars,
                "forks": metadata.forks,
                "language": metadata.language,
                "default_branch": metadata.default_branch,
                "updated_at": metadata.updated_at,
            },
            readme_summary=readme_summary,
            recent_issues=[asdict(issue) for issue in issues],
            recent_pull_requests=[asdict(pr) for pr in pull_requests],
            top_contributors=[asdict(contrib) for contrib in contributors],
            languages=language_stats,
            total_files=total_files,
        )

    def _get_readme_summary(self, cache_path: Path) -> str | None:
        """Get summary from README file.

        Args:
            cache_path: Repository cache path.

        Returns:
            README summary or None.
        """
        readme_patterns = ["README.md", "README.rst", "README.txt", "README"]
        for pattern in readme_patterns:
            readme_path = cache_path / pattern
            if readme_path.exists() and readme_path.is_file():
                try:
                    content = readme_path.read_text(encoding="utf-8")
                    # Get first 500 characters as summary
                    readme_summary = content[:500].strip()
                    if len(content) > 500:
                        readme_summary += "..."
                    return readme_summary
                except (OSError, UnicodeDecodeError):
                    pass
        return None

    def handle_search_doc(self, params: dict[str, Any]) -> SearchDocOutput:
        """Handle search_doc tool request.

        Args:
            params: Tool parameters.

        Returns:
            Search results.
        """
        input_data = SearchDocInput(
            repository=params["repository"],
            query=params["query"],
            limit=params.get("limit", DEFAULT_SEARCH_LIMIT),
        )

        owner, name = GitHubClient.parse_repo_url(input_data.repository)
        cache_path, metadata = self._repo_cache.get_repository(owner, name)

        self._indexer.index_repository(metadata.full_name, cache_path)

        documents = self._search_index.search_documents(
            metadata.full_name, input_data.query, input_data.limit
        )

        issues = self._github_client.get_recent_issues(owner, name, limit=5)
        pull_requests = self._github_client.get_recent_pull_requests(
            owner, name, limit=5
        )
        contributors = self._github_client.get_contributors(
            owner, name, limit=10
        )

        return SearchDocOutput(
            repository={
                "name": metadata.full_name,
                "description": metadata.description,
                "stars": metadata.stars,
                "forks": metadata.forks,
                "language": metadata.language,
            },
            documents=[asdict(doc) for doc in documents],
            issues=[asdict(issue) for issue in issues],
            pull_requests=[asdict(pr) for pr in pull_requests],
            contributors=[asdict(contrib) for contrib in contributors],
        )

    def handle_get_repo_structure(
        self, params: dict[str, Any]
    ) -> GetRepoStructureOutput:
        """Handle get_repo_structure tool request.

        Args:
            params: Tool parameters.

        Returns:
            Repository structure.
        """
        input_data = GetRepoStructureInput(
            repository=params["repository"],
            path=params.get("path", ""),
            depth=params.get("depth", 4),
        )

        owner, name = GitHubClient.parse_repo_url(input_data.repository)
        cache_path, _ = self._repo_cache.get_repository(owner, name)

        file_reader = FileReader(cache_path)
        tree, language_stats, total_files = file_reader.get_file_tree_with_stats(
            input_data.path, input_data.depth
        )

        structure_dicts = [self._tree_node_to_dict(node) for node in tree]

        return GetRepoStructureOutput(
            root=input_data.path or "/",
            structure=structure_dicts,
            stats={
                "total_files": total_files,
                "languages": language_stats,
            },
        )

    def handle_read_file(self, params: dict[str, Any]) -> ReadFileOutput:
        """Handle read_file tool request.

        Args:
            params: Tool parameters.

        Returns:
            File content and metadata.
        """
        input_data = ReadFileInput(
            repository=params["repository"],
            path=params["path"],
        )

        owner, name = GitHubClient.parse_repo_url(input_data.repository)
        cache_path, _ = self._repo_cache.get_repository(owner, name)

        file_reader = FileReader(cache_path)
        content, file_metadata = file_reader.read_file(input_data.path)

        return ReadFileOutput(
            path=file_metadata.path,
            language=file_metadata.language,
            size=file_metadata.size,
            encoding=file_metadata.encoding,
            content=content,
        )

    def _tree_node_to_dict(self, node: Any) -> dict[str, Any]:
        """Convert TreeNode to dictionary.

        Args:
            node: TreeNode instance.

        Returns:
            Dictionary representation.
        """
        result: dict[str, Any] = {
            "name": node.name,
            "path": node.path,
            "type": node.type,
        }

        if node.size is not None:
            result["size"] = node.size

        if node.children is not None:
            result["children"] = [
                self._tree_node_to_dict(child) for child in node.children
            ]

        return result
