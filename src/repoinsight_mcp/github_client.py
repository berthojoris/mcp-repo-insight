"""GitHub API client for fetching repository data."""

import re
from typing import Optional

import requests
from github import Github, GithubException

from .config import GITHUB_API_BASE
from .exceptions import GitHubAPIError, InvalidRepositoryError
from .models import Contributor, IssueResult, RepositoryMetadata


class GitHubClient:
    """Client for interacting with GitHub API."""

    def __init__(self, token: Optional[str] = None) -> None:
        """Initialize GitHub client.

        Args:
            token: Optional GitHub personal access token for higher rate limits.
        """
        self._token = token
        self._session = requests.Session()
        if token:
            self._session.headers["Authorization"] = f"token {token}"
            self._github = Github(token)
        else:
            self._github = Github()

    @staticmethod
    def parse_repo_url(url: str) -> tuple[str, str]:
        """Parse GitHub repository URL into owner and name.

        Args:
            url: GitHub repository URL or owner/name format.

        Returns:
            Tuple of (owner, name).

        Raises:
            InvalidRepositoryError: If URL format is invalid.
        """
        patterns = [
            r"github\.com[/:]([^/]+)/([^/\.]+?)(?:\.git)?$",
            r"^([^/]+)/([^/]+)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1), match.group(2)

        raise InvalidRepositoryError(f"Invalid repository URL or format: {url}")

    def get_repository_metadata(self, owner: str, name: str) -> RepositoryMetadata:
        """Fetch repository metadata from GitHub API.

        Args:
            owner: Repository owner.
            name: Repository name.

        Returns:
            Repository metadata.

        Raises:
            GitHubAPIError: If API request fails.
        """
        try:
            repo = self._github.get_repo(f"{owner}/{name}")
            return RepositoryMetadata(
                owner=owner,
                name=name,
                full_name=repo.full_name,
                description=repo.description,
                stars=repo.stargazers_count,
                forks=repo.forks_count,
                language=repo.language,
                default_branch=repo.default_branch,
                clone_url=repo.clone_url,
                updated_at=repo.updated_at.isoformat() if repo.updated_at else "",
            )
        except GithubException as e:
            raise GitHubAPIError(f"Failed to fetch repository metadata: {e}")

    def get_recent_issues(
        self, owner: str, name: str, limit: int = 10
    ) -> list[IssueResult]:
        """Fetch recent issues for repository.

        Args:
            owner: Repository owner.
            name: Repository name.
            limit: Maximum number of issues to return.

        Returns:
            List of recent issues.

        Raises:
            GitHubAPIError: If API request fails.
        """
        try:
            repo = self._github.get_repo(f"{owner}/{name}")
            issues = repo.get_issues(state="all", sort="updated", direction="desc")
            results = []

            for issue in issues[:limit]:
                if issue.pull_request:
                    continue
                results.append(
                    IssueResult(
                        number=issue.number,
                        title=issue.title,
                        state=issue.state,
                        created_at=issue.created_at.isoformat(),
                        updated_at=issue.updated_at.isoformat(),
                        author=issue.user.login if issue.user else "unknown",
                        url=issue.html_url,
                        is_pull_request=False,
                    )
                )

            return results
        except GithubException as e:
            raise GitHubAPIError(f"Failed to fetch issues: {e}")

    def get_recent_pull_requests(
        self, owner: str, name: str, limit: int = 10
    ) -> list[IssueResult]:
        """Fetch recent pull requests for repository.

        Args:
            owner: Repository owner.
            name: Repository name.
            limit: Maximum number of PRs to return.

        Returns:
            List of recent pull requests.

        Raises:
            GitHubAPIError: If API request fails.
        """
        try:
            repo = self._github.get_repo(f"{owner}/{name}")
            pulls = repo.get_pulls(state="all", sort="updated", direction="desc")
            results = []

            for pr in pulls[:limit]:
                results.append(
                    IssueResult(
                        number=pr.number,
                        title=pr.title,
                        state=pr.state,
                        created_at=pr.created_at.isoformat(),
                        updated_at=pr.updated_at.isoformat(),
                        author=pr.user.login if pr.user else "unknown",
                        url=pr.html_url,
                        is_pull_request=True,
                    )
                )

            return results
        except GithubException as e:
            raise GitHubAPIError(f"Failed to fetch pull requests: {e}")

    def get_contributors(self, owner: str, name: str, limit: int = 10) -> list[Contributor]:
        """Fetch repository contributors.

        Args:
            owner: Repository owner.
            name: Repository name.
            limit: Maximum number of contributors to return.

        Returns:
            List of contributors.

        Raises:
            GitHubAPIError: If API request fails.
        """
        try:
            repo = self._github.get_repo(f"{owner}/{name}")
            contributors = repo.get_contributors()
            results = []

            for contributor in contributors[:limit]:
                results.append(
                    Contributor(
                        login=contributor.login,
                        contributions=contributor.contributions,
                        avatar_url=contributor.avatar_url,
                    )
                )

            return results
        except GithubException as e:
            raise GitHubAPIError(f"Failed to fetch contributors: {e}")
