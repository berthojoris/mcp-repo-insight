# AGENTS.md

## Project: RepoInsight MCP (Python)

This document defines **how AI agents should work** when designing, implementing, and maintaining the **RepoInsight MCP** project.

The goal of this agent setup is to ensure the MCP server is:
- Correctly implemented according to the PRD
- MCP-compliant and agent-friendly
- Secure, local-first, and deterministic
- Easy to extend in future versions

---

## 1. Agent Mission

The AI agent's mission is to **design and implement a local-first MCP server in Python** that allows other AI agents to deeply understand public GitHub repositories.

The agent must:
- Follow the PRD strictly
- Prioritize clarity, correctness, and maintainability
- Avoid unnecessary abstractions
- Optimize for AI consumption, not human UI

---

## 2. Core Responsibilities

### 2.1 MCP Compliance
The agent must:
- Implement MCP tools exactly as specified
- Ensure tool names, inputs, and outputs are stable
- Avoid breaking changes without versioning

Supported tools:
- `search_doc`
- `get_repo_structure`
- `read_file`

---

### 2.2 Local-First Design

The agent must:
- Assume the MCP server runs locally
- Avoid cloud dependencies
- Avoid mandatory authentication
- Ensure all data is stored locally

Never:
- Send repository contents to external services
- Require internet access beyond GitHub public APIs

---

### 2.3 Read-Only & Safe Execution

The agent must enforce:
- Read-only access to repositories
- No file execution
- No shell command execution from MCP tools
- Strict file size limits

All repository access must be:
- Deterministic
- Non-destructive
- Fully auditable

---

## 3. Architectural Rules

### 3.1 Separation of Concerns

Agents must maintain clear boundaries between:

- MCP protocol layer
- GitHub data access layer
- Repository caching layer
- Indexing and search layer
- Tool handler layer

No tool handler should directly:
- Perform raw GitHub API calls
- Traverse filesystem without validation

---

### 3.2 Stateless Tools, Stateful Cache

- MCP tools must be stateless
- State must live only in:
  - Local filesystem cache
  - SQLite metadata database

Tools must not rely on global in-memory state.

---

### 3.3 Deterministic Outputs

Given the same inputs and cached repository state:
- Tools must return identical outputs
- Ordering must be stable
- Fields must not be omitted conditionally

This is critical for AI reasoning stability.

---

## 4. Coding Standards

### 4.1 Python Standards

- Python >= 3.10
- Use type hints everywhere
- Prefer dataclasses or Pydantic models
- Avoid metaprogramming

### 4.2 Error Handling

- Fail fast with clear error messages
- Never swallow exceptions silently
- Return structured MCP errors

Example:
```json
{
  "error": "FileTooLarge",
  "message": "File exceeds 1MB limit"
}
```

---

### 4.3 File Handling Rules

The agent must:
- Validate paths against repository root
- Block path traversal (`..`)
- Detect file encoding safely
- Reject binary files

---

## 5. Tool-Specific Agent Instructions

---

### 5.1 `search_doc`

The agent must:
- Index README and documentation files first
- Prefer official docs over issues
- Summarize issues and PRs concisely
- Avoid long unstructured text blobs

Never:
- Return full issue comment threads
- Return raw GitHub API payloads

---

### 5.2 `get_repo_structure`

The agent must:
- Return a stable directory tree
- Limit recursion depth
- Include file metadata useful for reasoning

Avoid:
- Excessive nesting
- Unbounded directory traversal

---

### 5.3 `read_file`

The agent must:
- Return the complete file content
- Include language and encoding metadata
- Enforce strict size limits

Never:
- Truncate code silently
- Return partial files without warning

---

## 6. Performance Guidelines

The agent must:
- Cache aggressively
- Avoid repeated GitHub API calls
- Index repositories only once per cache TTL

Performance targets:
- Repo indexing < 60s (medium repo)
- Cached reads < 200ms

---

## 7. Security Guidelines

The agent must:
- Treat all repository content as untrusted
- Never execute repository code
- Never deserialize untrusted data unsafely

Dependencies must be:
- Well-known
- Actively maintained
- Minimal in number

---

## 8. Extensibility Rules

The agent should design with future features in mind:
- AST parsing
- Symbol navigation
- Semantic search

However:
- Do NOT implement future features prematurely
- Keep v1 simple and stable

---

## 9. Documentation Responsibilities

The agent must:
- Keep README.md updated
- Document all MCP tools
- Provide example MCP configuration

Code without documentation is considered incomplete.

---

## 10. Agent Anti-Patterns (Strictly Forbidden)

The agent must NOT:
- Implement business logic inside MCP handlers
- Expose filesystem outside repo root
- Use global mutable state
- Depend on non-deterministic behavior
- Over-engineer abstractions

---

## 11. Definition of Done (DoD)

A task is considered DONE only if:
- Code matches PRD and this AGENTS.md
- MCP tools respond correctly
- Errors are structured and predictable
- Documentation is updated
- No security rules are violated

---

## 12. Final Instruction to AI Agents

> Build RepoInsight MCP as if another AI agent will rely on it to understand **critical production code**.

Clarity, determinism, and safety are more important than cleverness.
