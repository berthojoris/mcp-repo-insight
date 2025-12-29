"""Main entry point for RepoInsight MCP server."""

import argparse
import os
import sys
from typing import Optional

from rich.console import Console

from .server import MCPServer

console = Console()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RepoInsight MCP - Local-first GitHub repository analysis"
    )
    parser.add_argument(
        "--token",
        type=str,
        help="GitHub personal access token (or set GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["stdio", "http"],
        default="stdio",
        help="Server mode (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP server port (default: 8000)",
    )

    args = parser.parse_args()

    github_token: Optional[str] = args.token or os.environ.get("GITHUB_TOKEN")

    if args.mode == "stdio":
        # Don't print to stderr in stdio mode (interferes with MCP protocol)
        server = MCPServer(github_token)
        try:
            server.run_stdio()
        except KeyboardInterrupt:
            pass
        finally:
            server.cleanup()
    elif args.mode == "http":
        console.print(f"[bold green]RepoInsight MCP Server starting on port {args.port}[/bold green]")
        console.print("[yellow]HTTP mode not yet implemented. Use stdio mode.[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
