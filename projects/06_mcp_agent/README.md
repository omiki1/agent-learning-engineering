# Project 06｜MCP Agent（Python SDK v2）

本项目按 2026-08-27 官方 Python SDK v2 文档编写，使用 `MCPServer`，不是旧版 `FastMCP`。

```powershell
python -m pip install "mcp[cli]"
python projects/06_mcp_agent/client.py
```

Server 暴露：

- `read_course_doc`：受限文件工具，只读 `docs/*.md`。
- `query_course_topics`：数据查询工具，不接受任意 SQL。
- `get_github_repo`：外部 API 工具，只访问固定 GitHub API Host。
- `course://overview`：Resource。
- `review_topic`：Prompt。

安全实验：尝试传 `../README.md`；确认文件工具拒绝。外部 API 需网络，失败应成为工具错误而不是 Server 崩溃。

