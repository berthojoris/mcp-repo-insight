# Product Requirements Document (PRD)

## Project Name
**RepoInsight MCP (Python)**

## Version
v1.0 (Initial Release)

## Owner
Project Author

## Status
Design / Planning

---

## 1. Purpose & Vision

### 1.1 Purpose
RepoInsight MCP is a **local-first MCP (Model Context Protocol) server** built with Python that enables AI agents to **inspect, analyze, and understand public GitHub repositories** in depth.

The MCP exposes structured tools that allow AI agents to:
- Discover repository knowledge and recent activity
- Understand project structure and modularization
- Read and analyze source code files in full

The MCP runs **locally** and acts as a **trusted code intelligence layer** for AI agents.

---

### 1.2 Vision
Enable AI agents to reason about unfamiliar codebases **like experienced senior developers** by providing:
- Clean repository context
- Navigable project structure
- Full source-level visibility
- Helpful semantic and metadata signals

---

## 2. Scope

### In Scope
- Public GitHub repositories
- Local execution only
- Read-only access
- Code exploration and understanding
- MCP-compliant tool interface

### Out of Scope (v1)
- Private repositories
- Authentication / OAuth
- Code modification or commits
- Code execution or sandboxing
- Advanced static analysis (call graphs, refactoring)

---

## 3. Target Users

- AI Agents (Claude Code, Cline, Droid, etc.)
- Developers using AI-assisted code exploration
- Security-conscious users preferring local tools
- Open-source contributors and reviewers

---

## 4. High-Level Architecture

```
AI Agent
   |
   |  MCP Protocol (stdio or HTTP/SSE)
   |
RepoInsight MCP Server (Python)
   |
   ├── GitHub Fetch Layer
   ├── Repository Cache
   ├── Index & Search Engine
   ├── Code Reader
   └── Tool Handlers
```

---

## 5. Technology Stack

### 5.1 Core Language
- Python 3.10+

### 5.2 Python Libraries

#### GitHub Access
- requests
- PyGithub
- gitpython (optional local clone)

#### MCP Server
- fastapi
- uvicorn
- pydantic
- sse-starlette (optional)

#### File & Code Analysis
- pathlib
- chardet
- pygments
- tree-sitter (future)
- radon (optional metrics)

#### Search & Indexing
- sqlite3
- SQLite FTS5
- whoosh (alternative)

#### Utilities
- rich
- orjson
- tqdm

---

## 6. Execution Model

### 6.1 Local Execution

```
python main.py
```

or as a CLI binary:

```
repoinsight-mcp
```

### 6.2 Communication
- MCP over stdio (preferred)
- MCP over HTTP (localhost)

---

## 7. MCP Tools Specification

---

### 7.1 Tool: search_doc

**Description**  
Search documentation, repository knowledge, recent activity, and contributors.

**Responsibilities**
- Parse README and documentation files
- Retrieve repository metadata
- Summarize recent issues and pull requests
- List contributors

**Inputs**
```json
{
  "query": "authentication flow",
  "limit": 10
}
```

**Outputs**
```json
{
  "repository": {
    "name": "owner/repo",
    "description": "...",
    "stars": 1234,
    "language": "Python"
  },
  "documents": [],
  "issues": [],
  "pull_requests": [],
  "contributors": []
}
```

---

### 7.2 Tool: get_repo_structure

**Description**  
Retrieve directory tree and file list to understand project architecture.

**Responsibilities**
- Traverse repository tree
- Identify key folders
- Provide basic statistics

**Inputs**
```json
{
  "path": "",
  "depth": 4
}
```

**Outputs**
```json
{
  "root": "/",
  "structure": [],
  "stats": {
    "total_files": 0,
    "languages": {}
  }
}
```

---

### 7.3 Tool: read_file

**Description**  
Read the complete content of a specified file.

**Responsibilities**
- Fetch raw file contents
- Detect encoding
- Provide metadata for reasoning

**Inputs**
```json
{
  "path": "src/main.py"
}
```

**Outputs**
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

## 8. Repository Processing Pipeline

1. Validate repository URL
2. Fetch metadata via GitHub API
3. Clone or shallow-fetch repository
4. Cache locally
5. Index files and documentation
6. Serve MCP tool requests

---

## 9. Caching Strategy

```
~/.repoinsight/
  └── repos/
      └── owner_repo/
```

- SQLite metadata cache
- Configurable TTL
- Manual cache cleanup

---

## 10. Security Considerations

- Public repositories only
- No credential storage
- No code execution
- File size and path validation

---

## 11. Performance Requirements

- Medium repo indexing < 60 seconds
- Cached search < 500 ms
- File read < 200 ms

---

## 12. Future Enhancements

- AST-based symbol navigation
- Semantic embedding search
- Private repo support
- Language Server integration

---

## 13. Success Metrics

- Accurate AI understanding of code structure
- Reduced hallucination
- Stable MCP responses
- Low latency and resource usage

---

## 14. Deliverables

- Python MCP server
- Tool definitions
- README documentation
- Example MCP config
- Optional Dockerfile

---

## 15. Final Notes

RepoInsight MCP is designed to be **local-first**, **secure**, and **AI-agent friendly**, serving as a bridge between raw source code and high-quality AI reasoning.

