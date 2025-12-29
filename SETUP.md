# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. (Optional) Set GitHub Token

For higher API rate limits (60 req/hour → 5000 req/hour):

```bash
# Windows (PowerShell)
$env:GITHUB_TOKEN="your_token_here"

# Linux/macOS
export GITHUB_TOKEN=your_token_here
```

Get a token at: https://github.com/settings/tokens

Required scopes: None (public_repo access only)

### 3. Test the Server

```bash
python -m repoinsight_mcp.main --help
```

### 4. Run in Stdio Mode

```bash
python -m repoinsight_mcp.main
```

The server will now accept MCP requests via stdin/stdout.

### 5. Configure MCP Client

#### Claude Desktop

**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "python",
      "args": [
        "-m",
        "repoinsight_mcp.main"
      ],
      "cwd": "C:\\DEKSTOP\\MCP\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\DEKSTOP\\MCP\\repo_insight\\src",
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Important**: Update paths to match your installation.

#### Cline (VS Code)

1. Open VS Code
2. Install Cline extension
3. Open Cline settings
4. Add MCP server configuration (similar to above)

### 6. Test with MCP Client

Once configured, ask your AI agent:

```
Can you explore the FastAPI repository (tiangolo/fastapi) 
and show me its structure?
```

The agent should use the `get_repo_structure` tool.

## Troubleshooting

### ModuleNotFoundError

Ensure you're in the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Add src to PYTHONPATH:
```bash
# Windows (PowerShell)
$env:PYTHONPATH="C:\DEKSTOP\MCP\repo_insight\src"

# Linux/macOS
export PYTHONPATH="/path/to/repo_insight/src"
```

### GitHub Rate Limiting

Without token: 60 requests/hour
With token: 5000 requests/hour

Create token at: https://github.com/settings/tokens

### Port Already in Use

If running HTTP mode (future):
```bash
python -m repoinsight_mcp.main --port 8001
```

### Cache Issues

Clear cache:
```bash
# Windows
rmdir /s /q %USERPROFILE%\.repoinsight

# Linux/macOS
rm -rf ~/.repoinsight
```

## Verification

Test syntax of all modules:
```bash
python -m py_compile src/repoinsight_mcp/*.py
```

All should complete without errors.

## Next Steps

1. Configure MCP client
2. Test with sample repositories
3. Read AGENTS.md for development guidelines
4. Explore the codebase structure
