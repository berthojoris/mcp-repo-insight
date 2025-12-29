"""Search and indexing for repository documentation."""

import sqlite3
from pathlib import Path
from typing import Optional

from .config import DB_FILE
from .models import DocumentResult


class SearchIndex:
    """SQLite FTS5-based search index for repository documentation."""

    def __init__(self) -> None:
        """Initialize search index."""
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(DB_FILE))
        self._create_tables()

    def _create_tables(self) -> None:
        """Create FTS5 tables for search."""
        cursor = self._conn.cursor()

        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS documents
            USING fts5(
                repository,
                path,
                title,
                content,
                tokenize='porter unicode61'
            )
        """)

        self._conn.commit()

    def index_document(
        self, repository: str, path: str, title: str, content: str
    ) -> None:
        """Index a document for search.

        Args:
            repository: Repository full name (owner/name).
            path: File path in repository.
            title: Document title.
            content: Document content.
        """
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO documents (repository, path, title, content)
            VALUES (?, ?, ?, ?)
        """,
            (repository, path, title, content),
        )
        self._conn.commit()

    def search_documents(
        self, repository: str, query: str, limit: int = 10
    ) -> list[DocumentResult]:
        """Search indexed documents.

        Args:
            repository: Repository full name (owner/name).
            query: Search query.
            limit: Maximum number of results.

        Returns:
            List of document results ordered by relevance.
        """
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT path, title, content, rank
            FROM documents
            WHERE repository = ? AND documents MATCH ?
            ORDER BY rank
            LIMIT ?
        """,
            (repository, query, limit),
        )

        results = []
        for row in cursor.fetchall():
            path, title, content, rank = row
            results.append(
                DocumentResult(
                    path=path,
                    title=title,
                    content=content[:500],
                    score=abs(rank),
                )
            )

        return results

    def clear_repository_index(self, repository: str) -> None:
        """Clear all indexed documents for a repository.

        Args:
            repository: Repository full name (owner/name).
        """
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM documents WHERE repository = ?", (repository,))
        self._conn.commit()

    def close(self) -> None:
        """Close database connection."""
        self._conn.close()


class DocumentIndexer:
    """Indexes documentation files from repository."""

    DOCUMENTATION_PATTERNS = [
        "README.md",
        "README.rst",
        "README.txt",
        "README",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "HISTORY.md",
        "LICENSE.md",
        "docs/**/*.md",
        "docs/**/*.rst",
        "documentation/**/*.md",
    ]

    def __init__(self, search_index: SearchIndex) -> None:
        """Initialize document indexer.

        Args:
            search_index: Search index instance.
        """
        self._search_index = search_index

    def index_repository(self, repository: str, repo_path: Path) -> int:
        """Index all documentation files in repository.

        Args:
            repository: Repository full name (owner/name).
            repo_path: Path to local repository.

        Returns:
            Number of documents indexed.
        """
        self._search_index.clear_repository_index(repository)

        indexed_count = 0
        for pattern in self.DOCUMENTATION_PATTERNS:
            if "**" in pattern:
                files = repo_path.glob(pattern)
            else:
                file_path = repo_path / pattern
                files = [file_path] if file_path.exists() else []

            for file_path in files:
                if file_path.is_file() and self._should_index(file_path):
                    self._index_file(repository, repo_path, file_path)
                    indexed_count += 1

        return indexed_count

    def _should_index(self, file_path: Path) -> bool:
        """Check if file should be indexed.

        Args:
            file_path: File path.

        Returns:
            True if file should be indexed.
        """
        if file_path.stat().st_size > 100_000:
            return False

        try:
            file_path.read_text(encoding="utf-8")
            return True
        except (UnicodeDecodeError, OSError):
            return False

    def _index_file(self, repository: str, repo_path: Path, file_path: Path) -> None:
        """Index a single file.

        Args:
            repository: Repository full name.
            repo_path: Repository root path.
            file_path: File to index.
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            relative_path = str(file_path.relative_to(repo_path))
            title = file_path.name

            self._search_index.index_document(repository, relative_path, title, content)
        except Exception:
            pass
