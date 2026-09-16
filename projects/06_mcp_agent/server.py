"""MCP Python SDK v2 server；需要 mcp[cli]。"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

from mcp.server import MCPServer


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
mcp = MCPServer("stu-agent-course")


@mcp.tool()
def read_course_doc(relative_path: str) -> str:
    """Read one Markdown document below the course docs directory."""
    target = (DOCS / relative_path).resolve()
    if DOCS.resolve() not in target.parents or target.suffix.lower() != ".md":
        raise PermissionError("only docs/*.md is allowed")
    return target.read_text(encoding="utf-8")[:5000]


@mcp.tool()
def query_course_topics(keyword: str, limit: int = 5) -> list[dict[str, int | str]]:
    """Return course documents containing a keyword; no arbitrary SQL is accepted."""
    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")
    rows = []
    for path in DOCS.glob("*.md"):
        count = path.read_text(encoding="utf-8").lower().count(keyword.lower())
        if count: rows.append({"document": path.name, "matches": count})
    return sorted(rows, key=lambda row: int(row["matches"]), reverse=True)[:limit]


@mcp.tool()
def get_github_repo(owner: str, repo: str) -> dict[str, object]:
    """Read public metadata for one GitHub repository from api.github.com."""
    safe_owner = urllib.parse.quote(owner, safe="")
    safe_repo = urllib.parse.quote(repo, safe="")
    url = f"https://api.github.com/repos/{safe_owner}/{safe_repo}"
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "stu-agent-course"})
    with urllib.request.urlopen(request, timeout=8) as response:
        data = json.load(response)
    return {"full_name": data["full_name"], "description": data.get("description"), "stars": data["stargazers_count"], "url": data["html_url"]}


@mcp.resource("course://overview")
def course_overview() -> str:
    """The course entry document."""
    return (ROOT / "README.md").read_text(encoding="utf-8")[:5000]


@mcp.prompt()
def review_topic(topic: str) -> str:
    """Create a review request for one course topic."""
    return f"请从定义、反例、Debug 和架构选择四方面复习：{topic}"


if __name__ == "__main__":
    mcp.run()

