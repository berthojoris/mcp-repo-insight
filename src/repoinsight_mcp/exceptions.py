"""Custom exceptions for RepoInsight MCP."""


class RepoInsightError(Exception):
    """Base exception for RepoInsight MCP."""

    pass


class InvalidRepositoryError(RepoInsightError):
    """Raised when repository URL is invalid."""

    pass


class FileTooLargeError(RepoInsightError):
    """Raised when file exceeds size limit."""

    pass


class PathTraversalError(RepoInsightError):
    """Raised when path contains traversal attempts."""

    pass


class FileNotFoundError(RepoInsightError):
    """Raised when file doesn't exist in repository."""

    pass


class BinaryFileError(RepoInsightError):
    """Raised when attempting to read binary file."""

    pass


class GitHubAPIError(RepoInsightError):
    """Raised when GitHub API request fails."""

    pass
