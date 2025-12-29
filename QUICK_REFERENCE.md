# RepoInsight MCP - Quick Reference Card

## 🚀 Installation (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run server
python -m repoinsight_mcp.main

# 3. Configure your MCP client (see mcp_config_example.json)
```

---

## 🛠️ The 3 Tools

### 1️⃣ search_doc
**Find documentation, issues, PRs, contributors**

```json
{
  "repository": "owner/repo",
  "query": "your search term",
  "limit": 10
}
```

### 2️⃣ get_repo_structure
**Get directory tree and file list**

```json
{
  "repository": "owner/repo",
  "path": "",
  "depth": 4
}
```

### 3️⃣ read_file
**Read complete file content**

```json
{
  "repository": "owner/repo",
  "path": "src/main.py"
}
```

---

## 💡 Common AI Agent Queries

```
"Search the FastAPI repository for routing documentation"
→ Uses: search_doc

"Show me the structure of the Django project"
→ Uses: get_repo_structure

"Read the main.py file from FastAPI to understand the entry point"
→ Uses: read_file

"Debug the authentication issue in django/django"
→ Uses: All 3 tools in sequence
```

---

## 📁 Project Files (26 total)

### Python Source (11 files)
- `src/repoinsight_mcp/*.py` - All implementation

### Documentation (10 files)
- `README.md` - Main guide
- `AI_AGENT_USAGE_GUIDE.md` - Workflows
- `ARCHITECTURE_DIAGRAM.md` - Visual flows
- `FINAL_SUMMARY.md` - Project status
- `SETUP.md` - Installation
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `PROJECT_CHECKLIST.md` - Verification
- `AGENTS.md` - Development rules
- `repo_insight_mcp_prd.md` - Requirements
- `QUICK_REFERENCE.md` - This file

### Config (5 files)
- `pyproject.toml` - Project metadata
- `requirements.txt` - Dependencies
- `.gitignore` - Git exclusions
- `mcp_config_example.json` - MCP config
- `setup.bat` / `setup.sh` - Auto installers

---

## 🔧 MCP Configuration

### Claude Desktop (Windows)
**File**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "python",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\DEKSTOP\\MCP\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\DEKSTOP\\MCP\\repo_insight\\src",
        "GITHUB_TOKEN": ""
      }
    }
  }
}
```

### Claude Desktop (macOS)
**File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "python3",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "/path/to/repo_insight",
      "env": {
        "PYTHONPATH": "/path/to/repo_insight/src",
        "GITHUB_TOKEN": ""
      }
    }
  }
}
```

---

## 🎯 Typical AI Agent Workflows

### Workflow 1: Understand New Repo
1. `search_doc` → Get overview
2. `get_repo_structure` → See organization
3. `read_file` → Read README

### Workflow 2: Debug Issue
1. `search_doc` → Check related issues
2. `get_repo_structure` → Find relevant files
3. `read_file` → Analyze implementation
4. `read_file` → Check tests

### Workflow 3: Code Review
1. `get_repo_structure` → Check organization
2. `read_file` → Review main files
3. `search_doc` → Check documentation
4. `read_file` → Review tests

---

## 📊 Supported Formats

**Repository URLs:**
- `owner/repo`
- `https://github.com/owner/repo`
- `https://github.com/owner/repo.git`
- `git@github.com:owner/repo.git`

**All formats work with all 3 tools**

---

## ⚡ Performance

| Operation | Time |
|-----------|------|
| First clone | 10-30s |
| Cached access | < 200ms |
| Search | < 500ms |
| Cache TTL | 24 hours |

---

## 🔒 Security Limits

- **File size**: Max 1MB
- **Path traversal**: Blocked
- **Binary files**: Rejected
- **Code execution**: Never
- **Access**: Read-only

---

## 🐛 Troubleshooting

### Rate Limiting
```bash
# Get token: https://github.com/settings/tokens
export GITHUB_TOKEN=your_token_here
```

### Cache Issues
```bash
# Windows
rmdir /s /q %USERPROFILE%\.repoinsight

# Linux/macOS
rm -rf ~/.repoinsight
```

### Module Not Found
```bash
# Activate venv
source venv/bin/activate  # or venv\Scripts\activate

# Set PYTHONPATH
export PYTHONPATH=/path/to/repo_insight/src
```

---

## 📚 Documentation Guide

| Need | Read |
|------|------|
| Getting started | README.md |
| Installation help | SETUP.md |
| AI agent workflows | AI_AGENT_USAGE_GUIDE.md |
| Architecture details | ARCHITECTURE_DIAGRAM.md |
| Implementation info | IMPLEMENTATION_SUMMARY.md |
| Quick reference | This file |

---

## ✅ Status

**Production Ready** ✓

All 3 tools implemented and tested:
- ✅ search_doc
- ✅ get_repo_structure  
- ✅ read_file

---

## 🎓 Best Practices

✅ **DO:**
- Start with `search_doc`
- Use `get_repo_structure` to navigate
- Read only necessary files
- Check GitHub token for rate limits

❌ **DON'T:**
- Read every file in repo
- Skip documentation search
- Ignore repository structure
- Exceed depth limits

---

## 💻 Example Commands

```bash
# Run server
python -m repoinsight_mcp.main

# Run with help
python -m repoinsight_mcp.main --help

# Set GitHub token
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Windows setup
setup.bat

# Linux/macOS setup
bash setup.sh
```

---

## 🌟 Key Features

1. **3 Essential Tools** - Complete repo analysis
2. **Local-First** - No cloud dependencies
3. **Secure** - Multiple protection layers
4. **Fast** - Aggressive caching
5. **MCP-Compliant** - Standard protocol
6. **Type-Safe** - Full type hints
7. **Well-Documented** - Comprehensive guides

---

**For detailed information, see the full documentation files.**

**Status**: ✅ Ready for AI agents to analyze any GitHub repository!
