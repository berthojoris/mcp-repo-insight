"""File reading utilities with security validation."""

import os
from pathlib import Path
from typing import Optional

import chardet
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

from .config import MAX_FILE_SIZE_BYTES
from .exceptions import (
    BinaryFileError,
    FileNotFoundError,
    FileTooLargeError,
    PathTraversalError,
)
from .models import FileMetadata, TreeNode


class FileReader:
    """Secure file reader with validation."""

    def __init__(self, repo_path: Path) -> None:
        """Initialize file reader.

        Args:
            repo_path: Root path of repository.
        """
        self._repo_path = repo_path.resolve()

    def validate_path(self, file_path: str) -> Path:
        """Validate and resolve file path.

        Args:
            file_path: Relative file path.

        Returns:
            Resolved absolute path.

        Raises:
            PathTraversalError: If path contains traversal attempts.
            FileNotFoundError: If file doesn't exist.
        """
        if ".." in file_path:
            raise PathTraversalError(f"Path traversal detected: {file_path}")

        full_path = (self._repo_path / file_path).resolve()

        if not str(full_path).startswith(str(self._repo_path)):
            raise PathTraversalError(f"Path outside repository: {file_path}")

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not full_path.is_file():
            raise FileNotFoundError(f"Not a file: {file_path}")

        return full_path

    def read_file(self, file_path: str) -> tuple[str, FileMetadata]:
        """Read file content with validation.

        Args:
            file_path: Relative file path.

        Returns:
            Tuple of (content, metadata).

        Raises:
            FileTooLargeError: If file exceeds size limit.
            BinaryFileError: If file is binary.
        """
        full_path = self.validate_path(file_path)

        file_size = full_path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            raise FileTooLargeError(
                f"File exceeds {MAX_FILE_SIZE_BYTES / 1024 / 1024}MB limit"
            )

        raw_content = full_path.read_bytes()
        encoding_result = chardet.detect(raw_content)
        encoding = encoding_result["encoding"] or "utf-8"

        if encoding_result["confidence"] < 0.7:
            raise BinaryFileError(f"File appears to be binary: {file_path}")

        try:
            content = raw_content.decode(encoding)
        except UnicodeDecodeError:
            raise BinaryFileError(f"Cannot decode file: {file_path}")

        language = self._detect_language(full_path)

        metadata = FileMetadata(
            path=file_path,
            size=file_size,
            language=language,
            encoding=encoding,
        )

        return content, metadata

    def _detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file.

        Args:
            file_path: File path.

        Returns:
            Language name or None.
        """
        try:
            lexer = get_lexer_for_filename(str(file_path))
            return lexer.name
        except ClassNotFound:
            return None

    def get_file_tree(
        self, base_path: str = "", max_depth: int = 4
    ) -> list[TreeNode]:
        """Get directory tree structure.

        Args:
            base_path: Starting path (relative to repo root).
            max_depth: Maximum recursion depth.

        Returns:
            List of tree nodes.
        """
        if base_path:
            start_path = self.validate_path(base_path)
        else:
            start_path = self._repo_path

        return self._build_tree(start_path, self._repo_path, 0, max_depth)

    def _build_tree(
        self, current_path: Path, repo_root: Path, depth: int, max_depth: int
    ) -> list[TreeNode]:
        """Recursively build directory tree.

        Args:
            current_path: Current directory path.
            repo_root: Repository root path.
            depth: Current depth.
            max_depth: Maximum depth.

        Returns:
            List of tree nodes.
        """
        if depth >= max_depth:
            return []

        nodes = []
        try:
            items = sorted(current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        except PermissionError:
            return []

        for item in items:
            if item.name.startswith("."):
                continue

            relative_path = str(item.relative_to(repo_root))
            node = TreeNode(
                name=item.name,
                path=relative_path,
                type="directory" if item.is_dir() else "file",
            )

            if item.is_file():
                try:
                    node.size = item.stat().st_size
                except OSError:
                    node.size = 0
            elif item.is_dir():
                node.children = self._build_tree(item, repo_root, depth + 1, max_depth)

            nodes.append(node)

        return nodes

    def get_language_stats(self) -> dict[str, int]:
        """Get language statistics for repository.

        Returns:
            Dictionary mapping language names to file counts.
        """
        stats, _ = self.get_repo_stats()
        return stats

    def get_repo_stats(self) -> tuple[dict[str, int], int]:
        """Get repository statistics (languages and file count).

        Returns:
            Tuple of (language_stats, total_files).
        """
        stats: dict[str, int] = {}
        total_files = 0

        for root, dirs, files in os.walk(self._repo_path):
            # Modify dirs in-place to skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file
                total_files += 1
                language = self._detect_language(file_path)
                if language:
                    stats[language] = stats.get(language, 0) + 1

        return stats, total_files
