"""MCP server implementation for RepoInsight."""

import json
import sys
import signal
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import asdict
from typing import Any, Optional

from .cache import RepositoryCache
from .config import ensure_cache_directories, OPERATION_TIMEOUT
from .exceptions import RepoInsightError
from .github_client import GitHubClient
from .handlers import ToolHandlers
from .search import SearchIndex


class MCPServer:
    """MCP protocol server for RepoInsight."""

    def __init__(self, github_token: Optional[str] = None) -> None:
        """Initialize MCP server.

        Args:
            github_token: Optional GitHub personal access token.
        """
        ensure_cache_directories()

        self._github_client = GitHubClient(github_token)
        self._repo_cache = RepositoryCache(self._github_client)
        self._search_index = SearchIndex()
        self._handlers = ToolHandlers(
            self._github_client, self._repo_cache, self._search_index
        )

        self._tools = {
            "get_repo_summary": {
                "description": (
                    "Get a comprehensive summary of the GitHub repository "
                    "including metadata, statistics, recent activity, top "
                    "contributors, and main documentation"
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repository": {
                            "type": "string",
                            "description": (
                                "Repository URL or owner/name format"
                            ),
                        },
                    },
                    "required": ["repository"],
                    "additionalProperties": False,
                },
            },
            "search_doc": {
                "description": (
                    "Search for knowledge documentation corresponding to the "
                    "GitHub repository, quickly understanding repository "
                    "knowledge, news, recent issues, PRs, and contributors"
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repository": {
                            "type": "string",
                            "description": (
                                "Repository URL or owner/name format"
                            ),
                        },
                        "query": {
                            "type": "string",
                            "description": "Search query",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 10,
                        },
                    },
                    "required": ["repository", "query"],
                    "additionalProperties": False,
                },
            },
            "get_repo_structure": {
                "description": (
                    "Get the directory structure and file list of the GitHub "
                    "repository to understand project module splitting and "
                    "directory organization"
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repository": {
                            "type": "string",
                            "description": (
                                "Repository URL or owner/name format"
                            ),
                        },
                        "path": {
                            "type": "string",
                            "description": "Starting path (default: root)",
                            "default": "",
                        },
                        "depth": {
                            "type": "integer",
                            "description": "Maximum tree depth",
                            "default": 4,
                        },
                    },
                    "required": ["repository"],
                    "additionalProperties": False,
                },
            },
            "read_file": {
                "description": (
                    "Read the complete code content of specified files in the "
                    "GitHub repository to deeply analyze the implementation "
                    "details of the file code"
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repository": {
                            "type": "string",
                            "description": (
                                "Repository URL or owner/name format"
                            ),
                        },
                        "path": {
                            "type": "string",
                            "description": (
                                "File path relative to repository root"
                            ),
                        },
                    },
                    "required": ["repository", "path"],
                    "additionalProperties": False,
                },
            },
        }

    def handle_request(self, request: dict[str, Any]) -> dict[str, Any] | None:
        """Handle MCP request.

        Args:
            request: MCP request message.

        Returns:
            MCP response message, or None for notifications.
        """
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        # Handle notifications (no id = no response needed)
        if request_id is None:
            if method == "notifications/initialized":
                # Client confirmed initialization, no response needed
                return None
            # Other notifications can be ignored
            return None

        try:
            return self._dispatch_request(method, params, request_id)
        except RepoInsightError as e:
            return self._error_response(
                request_id, e.__class__.__name__, str(e)
            )
        except (ValueError, TypeError, KeyError) as e:
            return self._error_response(
                request_id, "InvalidRequest", f"Invalid request: {e}"
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            return self._error_response(
                request_id, "InternalError", f"Internal error: {e}"
            )

    def _dispatch_request(
        self, method: str | None, params: dict[str, Any], request_id: Any
    ) -> dict[str, Any]:
        """Dispatch request to appropriate handler.

        Args:
            method: Method name.
            params: Request parameters.
            request_id: Request ID.

        Returns:
            Response dictionary.
        """
        if method == "tools/list":
            return self._handle_tools_list(request_id)
        if method == "tools/call":
            return self._handle_tools_call(params, request_id)
        if method == "initialize":
            return self._handle_initialize(request_id)

        return self._error_response(
            request_id, "MethodNotFound", f"Unknown method: {method}"
        )

    def _handle_initialize(self, request_id: Any) -> dict[str, Any]:
        """Handle initialize request.

        Args:
            request_id: Request ID.

        Returns:
            Initialize response.
        """
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "repoinsight-mcp",
                    "version": "1.0.0",
                },
                "capabilities": {
                    "tools": {},
                },
            },
        }

    def _handle_tools_list(self, request_id: Any) -> dict[str, Any]:
        """Handle tools/list request.

        Args:
            request_id: Request ID.

        Returns:
            Tools list response.
        """
        tools = []
        for name, spec in self._tools.items():
            tools.append({
                "name": name,
                "description": spec["description"],
                "inputSchema": spec["inputSchema"],
            })

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools},
        }

    def _handle_tools_call(
        self, params: dict[str, Any], request_id: Any
    ) -> dict[str, Any]:
        """Handle tools/call request with timeout protection.

        Args:
            params: Tool call parameters.
            request_id: Request ID.

        Returns:
            Tool call response.
        """
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})

        def execute_tool() -> Any:
            if tool_name == "get_repo_summary":
                return self._handlers.handle_get_repo_summary(tool_params)
            elif tool_name == "search_doc":
                return self._handlers.handle_search_doc(tool_params)
            elif tool_name == "get_repo_structure":
                return self._handlers.handle_get_repo_structure(tool_params)
            elif tool_name == "read_file":
                return self._handlers.handle_read_file(tool_params)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(execute_tool)
                result = future.result(timeout=OPERATION_TIMEOUT)
        except FutureTimeoutError:
            return self._error_response(
                request_id,
                "Timeout",
                f"Tool execution timed out after {OPERATION_TIMEOUT} seconds. "
                f"The repository may be very large or the operation requires more time."
            )
        except ValueError as e:
            return self._error_response(
                request_id, "ToolNotFound", str(e)
            )

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(asdict(result), indent=2),
                    }
                ]
            },
        }

    def _error_response(
        self, request_id: Any, error_code: str, message: str
    ) -> dict[str, Any]:
        """Create error response.

        Args:
            request_id: Request ID.
            error_code: Error code.
            message: Error message.

        Returns:
            Error response.
        """
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": error_code,
                "message": message,
            },
        }

    def run_stdio(self) -> None:
        """Run server using stdio transport with signal handling."""
        def handle_signal(signum, frame):
            self.cleanup()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                # Only send response if not a notification
                if response is not None:
                    print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error = self._error_response(
                    None, "ParseError", "Invalid JSON"
                )
                print(json.dumps(error), flush=True)
            except (IOError, OSError) as e:
                # Log critical IO errors but try to continue or exit gracefully
                error = self._error_response(
                    None, "InternalError", f"IO Error: {e}"
                )
                print(json.dumps(error), flush=True)
            except Exception as e:  # pylint: disable=broad-exception-caught
                # Catch-all for unexpected runtime errors to prevent crash
                error = self._error_response(
                    None, "InternalError", f"Unexpected error: {e}"
                )
                print(json.dumps(error), flush=True)

    def cleanup(self) -> None:
        """Clean up resources."""
        self._search_index.close()
