# How to Use RepoInsight MCP - Complete Guide

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ Python 3.10 or higher installed
- ✅ Git installed
- ✅ Claude Desktop installed (or another MCP client)

---

## 🚀 Step-by-Step Setup

### Step 1: Install Dependencies (1 minute)

Open terminal/command prompt and run:

```bash
# Navigate to the project folder
cd C:\DEKSTOP\MCP\repo_insight

# Install required packages
pip install -r requirements.txt
```

**Expected output**: You'll see packages installing. Wait until it finishes.

✅ **Done!** Dependencies installed.

---

### Step 2: Configure Claude Desktop (2 minutes)

#### 2.1 Find the config file:

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```
(Paste this in File Explorer address bar)

**macOS**:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### 2.2 Edit the config file:

If file doesn't exist, create it. Then add:

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "python",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\DEKSTOP\\MCP\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\DEKSTOP\\MCP\\repo_insight\\src"
      }
    }
  }
}
```

**IMPORTANT**: 
- Replace `C:\\DEKSTOP\\MCP\\repo_insight` with YOUR actual path!
- Use double backslashes `\\` on Windows
- Use forward slashes `/` on macOS/Linux

#### 2.3 Save the file

✅ **Done!** Configuration saved.

---

### Step 3: Restart Claude Desktop (30 seconds)

1. **Quit** Claude Desktop completely (File → Quit)
2. **Wait** 5 seconds
3. **Start** Claude Desktop again

✅ **Done!** MCP server is now loaded.

---

## 🎯 Test It Works

In Claude Desktop, type:

```
Show me the structure of the fastapi/fastapi repository
```

**What should happen:**
1. Claude will use the `get_repo_structure` tool
2. It will clone the FastAPI repo (first time only, ~10-20 seconds)
3. It will show you the directory structure

**If you see the structure**: ✅ **SUCCESS! Everything works!**

---

## 💡 What You Can Do Now

### Example 1: Understand a Repository
```
"What does the django/django repository do? Search for documentation."
```

### Example 2: Find Files
```
"Show me the structure of the flask repository, focusing on the src folder"
```

### Example 3: Read Code
```
"Read the main.py file from fastapi/fastapi and explain how it works"
```

### Example 4: Debug Issues
```
"In the requests/requests repository, find and read the authentication module"
```

### Example 5: Compare Implementations
```
"Compare how FastAPI and Flask handle routing. Read their routing files."
```

---

## 🔑 Optional: Add GitHub Token (Better Performance)

### Why add a token?
- **Without**: 60 API requests/hour
- **With**: 5,000 API requests/hour (83x more!)

### How to get a token:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name it: `RepoInsight MCP`
4. **Don't select any scopes** (we only need public repo access)
5. Click **"Generate token"**
6. **Copy the token** (starts with `ghp_...`)

### How to add it:

Edit your config file again and add the token:

```json
{
  "mcpServers": {
    "repoinsight": {
      "command": "python",
      "args": ["-m", "repoinsight_mcp.main"],
      "cwd": "C:\\DEKSTOP\\MCP\\repo_insight",
      "env": {
        "PYTHONPATH": "C:\\DEKSTOP\\MCP\\repo_insight\\src",
        "GITHUB_TOKEN": "ghp_your_actual_token_here"
      }
    }
  }
}
```

Restart Claude Desktop.

✅ **Done!** Now you have 5,000 requests/hour.

---

## 🛠️ Troubleshooting

### Problem: "Module not found" error

**Solution**:
```bash
# Make sure you're in the right folder
cd C:\DEKSTOP\MCP\repo_insight

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Problem: Claude doesn't show RepoInsight tools

**Solution**:
1. Check config file path is correct
2. Check `cwd` and `PYTHONPATH` match your installation
3. Quit Claude Desktop COMPLETELY
4. Restart Claude Desktop
5. Check for errors in Claude's developer console

---

### Problem: "Rate limit exceeded"

**Solution**: Add a GitHub token (see above)

---

### Problem: "Repository not found"

**Solution**: 
- Make sure the repository is **public**
- Use format: `owner/repo` (e.g., `fastapi/fastapi`)
- Or full URL: `https://github.com/owner/repo`

---

## 📂 How It Works Behind the Scenes

### First Time You Analyze a Repo:
```
1. Claude asks RepoInsight to get repo structure
2. RepoInsight clones the repo to: ~/.repoinsight/repos/
3. RepoInsight indexes documentation
4. Returns structure to Claude
5. Claude shows you the results
```

### Next Time (Cached):
```
1. Claude asks for the same repo
2. RepoInsight checks cache (valid for 24 hours)
3. Returns data instantly (< 200ms)
4. Much faster! ⚡
```

---

## 🎓 Advanced Usage

### Clear Cache
If you want to refresh a repository:

**Windows**:
```bash
rmdir /s /q %USERPROFILE%\.repoinsight
```

**macOS/Linux**:
```bash
rm -rf ~/.repoinsight
```

### Run Server Manually (for testing)
```bash
cd C:\DEKSTOP\MCP\repo_insight
python -m repoinsight_mcp.main
```

This starts the server in your terminal. You'll see log messages.

Press `Ctrl+C` to stop.

---

## 🎯 The 3 Tools Explained

### 1. search_doc
- Searches README, docs, issues, PRs
- Shows contributors
- Good for: Understanding what a repo does

**Example**: 
```
"Search django/django for migration documentation"
```

### 2. get_repo_structure
- Shows directory tree
- Lists all files and folders
- Shows language statistics
- Good for: Finding files, understanding organization

**Example**:
```
"Show me the structure of tensorflow/tensorflow"
```

### 3. read_file
- Reads complete file content
- Detects programming language
- Max 1MB per file
- Good for: Code analysis, debugging

**Example**:
```
"Read the setup.py file from requests/requests"
```

---

## ✅ Summary

You now have RepoInsight MCP installed and working!

**You can:**
- ✅ Analyze any public GitHub repository
- ✅ Search documentation and issues
- ✅ Navigate repository structure
- ✅ Read and analyze source code
- ✅ Debug issues across multiple files
- ✅ Learn from open source projects

**Your AI agent can now deeply understand GitHub repositories!** 🎉

---

## 📚 More Help

- **Full documentation**: See `README.md`
- **Quick reference**: See `QUICK_REFERENCE.md`
- **AI agent workflows**: See `AI_AGENT_USAGE_GUIDE.md`
- **Architecture details**: See `ARCHITECTURE_DIAGRAM.md`

---

**Need help?** Check the Troubleshooting section above or review the documentation files!
