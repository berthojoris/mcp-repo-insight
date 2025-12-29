# RepoInsight MCP

**Local-first MCP server for GitHub repository analysis**

RepoInsight MCP is a Python-based Model Context Protocol (MCP) server that enables AI agents to deeply understand public GitHub repositories. It provides structured tools for searching documentation, exploring project structure, and reading source code files.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
# Navigate to project folder
cd C:\DEKSTOP\MCP\repo_insight

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Claude Desktop

**Find your Python path first:**
```bash
# Windows
where python

# macOS/Linux  
which python3
```

**Edit config file:**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Paste this configuration** (update paths to match your system):

**Windows Example:**
```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "C:\\laragon\\bin\\python\\python-3.13\\python.exe",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\DEKSTOP\\MCP\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\DEKSTOP\\MCP\\repo_insight\\src"
      }
    }
  }
}
```

**macOS/Linux Example:**
```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "/usr/local/bin/python3",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "/path/to/repo_insight",
      "env": {
        "PYTHONPATH": "/path/to/repo_insight/src"
      }
    }
  }
}
```

**Important Notes:**
- Use **full Python path** (from `where python` or `which python3`)
- `cwd` must point to the project root (where `src/` folder exists)
- `PYTHONPATH` must point to the `src` folder inside your project
- On Windows, use double backslashes `\\` in paths

### Step 3: Restart Claude Desktop

1. **Quit Claude Desktop completely** (File → Quit, not just close window)
2. **Wait 5 seconds**
3. **Start Claude Desktop again**
4. **Test**: "Show me the structure of the fastapi/fastapi repository"

✅ **Done!** Your AI agent can now analyze any GitHub repository!

---

## ✅ Verify It's Working

In Claude Desktop, you should see:
- A small icon or indicator showing MCP servers are loaded
- When you ask to analyze a repo, Claude will use the tools automatically

**Test command:**
```
"Analyze the structure of django/django and show me the main components"
```

If it works, you'll see Claude using `get_repo_structure` tool and showing results!

---

## 🎯 What You Can Do

Once configured, ask your AI agent things like:

```
"Analyze the FastAPI repository structure"
→ Uses: get_repo_structure

"Search the Django repo for authentication documentation"
→ Uses: search_doc

"Read the main.py file from fastapi/fastapi"
→ Uses: read_file

"Debug the login issue in owner/repo by checking auth files"
→ Uses: All 3 tools together
```

---

## 🔑 GitHub Token (Optional)

**Without token**: 60 requests/hour (good for testing)  
**With token**: 5,000 requests/hour (83x more - better for heavy use)

### How to Create a Token:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name: `RepoInsight MCP`
4. **Select NO scopes** (leave all checkboxes unchecked)
   - ✅ We only need public repository access
   - ✅ No permissions needed for public repos
   - ✅ More secure with minimal permissions
5. Click **"Generate token"**
6. Copy the token (starts with `ghp_...`)

### Add Token to Config:

Update your Claude Desktop config to include the token:

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "C:\\laragon\\bin\\python\\python-3.13\\python.exe",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\DEKSTOP\\MCP\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\DEKSTOP\\MCP\\repo_insight\\src",
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Remember to restart Claude Desktop after adding the token!**

---

## Features

- **Local-First**: All data cached locally, minimal API calls
- **Secure**: Read-only access, path validation, no code execution
- **Fast**: SQLite FTS5 search, aggressive caching
- **MCP-Compliant**: Works with Claude Desktop, Cline, and other MCP clients
- **Deterministic**: Stable outputs for reliable AI reasoning

## Architecture

```
RepoInsight MCP
├── MCP Protocol Layer (stdio/HTTP)
├── Tool Handlers (search_doc, get_repo_structure, read_file)
├── GitHub API Client
├── Repository Cache
├── Search Index (SQLite FTS5)
└── File Reader (with security validation)
```

## Requirements

- Python 3.10 or higher
- Git installed and available in PATH
- (Optional) GitHub personal access token for higher API rate limits

## Installation

### From Source

```bash
# Clone or navigate to repository
cd repo_insight

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Usage

### Running the Server

#### Stdio Mode (Recommended for MCP clients)

```bash
# Using installed command
repoinsight-mcp

# Or with Python module
python -m repoinsight_mcp.main

# With GitHub token for higher rate limits
export GITHUB_TOKEN=your_token_here
repoinsight-mcp
```

### MCP Client Configuration

#### Claude Desktop (Recommended)

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Complete working configuration:**

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "C:\\path\\to\\python.exe",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\path\\to\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\path\\to\\repo_insight\\src"
      }
    }
  }
}
```

**With GitHub Token (5000 req/hour):**

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "C:\\path\\to\\python.exe",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\path\\to\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\path\\to\\repo_insight\\src",
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Finding your paths:**
```bash
# Python path
where python          # Windows
which python3         # macOS/Linux

# Project path - use absolute path where you cloned the project
```

#### Cline (VS Code Extension)

Add to Cline MCP settings:

```json
{
  "repoinsight": {
    "command": "repoinsight-mcp",
    "args": [],
    "env": {
      "GITHUB_TOKEN": "your_token_here"
    }
  }
}
```

## MCP Tools

RepoInsight provides **3 powerful tools** that enable AI agents to analyze, check, debug, and perform any task on GitHub repositories:

### 1. search_doc

**Search for knowledge documentation corresponding to the GitHub repository, quickly understanding repository knowledge, news, recent issues, PRs, and contributors.**

🎯 **Use Cases for AI Agents:**
- Quickly understand what a repository does
- Find relevant documentation for a feature
- Review recent issues and discussions
- Identify active contributors and maintainers
- Search for specific topics or implementations

**Input:**
```json
{
  "repository": "owner/repo",
  "query": "authentication flow",
  "limit": 10
}
```

**Output:**
```json
{
  "repository": {
    "name": "owner/repo",
    "description": "...",
    "stars": 1234,
    "language": "Python"
  },
  "documents": [...],
  "issues": [...],
  "pull_requests": [...],
  "contributors": [...]
}
```

### 2. get_repo_structure

**Get the directory structure and file list of the GitHub repository to understand project module splitting and directory organization.**

🎯 **Use Cases for AI Agents:**
- Understand the overall architecture
- Locate specific modules or components
- Analyze project organization patterns
- Find configuration files
- Map dependencies between modules
- Navigate large codebases efficiently

**Input:**
```json
{
  "repository": "owner/repo",
  "path": "",
  "depth": 4
}
```

**Output:**
```json
{
  "root": "/",
  "structure": [...],
  "stats": {
    "total_files": 123,
    "languages": {
      "Python": 45,
      "JavaScript": 30
    }
  }
}
```

### 3. read_file

**Read the complete code content of specified files in the GitHub repository to deeply analyze the implementation details of the file code.**

🎯 **Use Cases for AI Agents:**
- Debug code issues
- Analyze implementation details
- Review code quality
- Understand algorithms and logic
- Check for security vulnerabilities
- Extract API signatures
- Learn coding patterns

**Input:**
```json
{
  "repository": "owner/repo",
  "path": "src/main.py"
}
```

**Output:**
```json
{
  "path": "src/main.py",
  "language": "Python",
  "size": 1234,
  "encoding": "utf-8",
  "content": "..."
}
```

---

### 🤖 AI Agent Workflow Example

1. **Discover** - Use `search_doc` to understand the repository
2. **Navigate** - Use `get_repo_structure` to find relevant files
3. **Analyze** - Use `read_file` to examine implementation details
4. **Debug** - Read multiple files to trace bugs
5. **Review** - Check code quality and patterns

## Configuration

### Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token (optional, increases rate limits)

### Cache Location

Repositories are cached in:
- **Linux/macOS**: `~/.repoinsight/repos/`
- **Windows**: `%USERPROFILE%\.repoinsight\repos\`

Cache TTL: 24 hours (configurable in `config.py`)

### File Size Limits

- Maximum file size: 1MB
- Maximum tree depth: 10 levels

## Security

RepoInsight MCP is designed with security as a priority:

- **Read-only**: No file modification or code execution
- **Path validation**: Blocks path traversal attempts
- **Size limits**: Prevents memory exhaustion
- **Binary detection**: Rejects binary files
- **Local-first**: No data sent to external services (except GitHub API)

## Performance

- Repository indexing: < 60 seconds (medium repo)
- Cached search: < 500ms
- File read: < 200ms

## Project Structure

```
repo_insight/
├── src/
│   └── repoinsight_mcp/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── server.py            # MCP server
│       ├── handlers.py          # Tool handlers
│       ├── github_client.py     # GitHub API
│       ├── cache.py             # Repository caching
│       ├── search.py            # Search & indexing
│       ├── file_reader.py       # File reading
│       ├── models.py            # Data models
│       ├── config.py            # Configuration
│       └── exceptions.py        # Custom exceptions
├── AGENTS.md                    # Agent guidelines
├── repo_insight_mcp_prd.md      # Product requirements
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests (when implemented)
pytest
```

### Code Formatting

```bash
black src/
```

### Type Checking

```bash
mypy src/
```

## Troubleshooting

### Common Issues

#### 1. MCP Error -32000: Connection Closed

**Cause**: Server failed to start

**Solutions:**

**A. Use Full Python Path**
```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "C:\\Users\\YourName\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\DEKSTOP\\MCP\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\DEKSTOP\\MCP\\repo_insight\\src"
      }
    }
  }
}
```

Find your Python path:
```bash
where python          # Windows
which python3         # macOS/Linux
```

**B. Verify Dependencies**
```bash
cd C:\DEKSTOP\MCP\repo_insight
pip install -r requirements.txt
```

**C. Test Server Manually**
```bash
cd C:\DEKSTOP\MCP\repo_insight
set PYTHONPATH=C:\DEKSTOP\MCP\repo_insight\src
python -m repoinsight_mcp.main
```

If this works, your paths are correct.

---

#### 2. Protocol Version Error

If you see "Server's protocol version is not supported", the code has already been updated to use protocol version `2024-11-05`. Just restart Claude Desktop.

---

#### 3. Tools Don't Appear

**Check:**
- Config file is in the correct location
- JSON syntax is valid (no missing commas/braces)
- Paths use double backslashes `\\` on Windows
- Claude Desktop was completely quit and restarted (not just window closed)

**Verify config location:**
```bash
# Windows - should open the folder
explorer %APPDATA%\Claude

# macOS
open ~/Library/Application\ Support/Claude/
```

--- Rate Limiting

If you encounter GitHub API rate limits:
1. Create a personal access token: https://github.com/settings/tokens
2. **Select NO scopes** (public repos don't need permissions)
3. Add to config (see GitHub Token section above)
4. Restart Claude Desktop

### Cache Issues

Clear the cache:
```bash
# Windows
rmdir /s /q %USERPROFILE%\.repoinsight

# macOS/Linux
rm -rf ~/.repoinsight/repos/
```

### Import Errors

Ensure dependencies are installed:
```bash
cd C:\DEKSTOP\MCP\repo_insight
pip install -r requirements.txt
```

## Future Enhancements

- AST-based symbol navigation
- Semantic embedding search
- Private repository support
- Language Server Protocol integration
- HTTP/SSE transport mode

## License

[Add your license here]

## Contributing

Contributions welcome! Please ensure:
- Code follows AGENTS.md guidelines
- All security rules are respected
- Type hints are included
- Tests pass (when implemented)

## Authors

Project Author

---

Built with ❤️ for AI agents
