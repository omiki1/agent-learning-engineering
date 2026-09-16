# 07｜MCP：连接协议，不是 Agent 大脑

## 1. 它是什么

模型上下文协议（Model Context Protocol, MCP）采用 Host–Client–Server 架构：

```text
AI Application / Host
 ├─ MCP Client A ↔ MCP Server A ↔ Files
 └─ MCP Client B ↔ MCP Server B ↔ Database/API
```

MCP 使用标准化协议暴露 Tools、Resources 和 Prompts。当前官方 Python SDK 稳定线为 v2；旧教程常见的 `FastMCP` 已改为 `MCPServer`。

## 2. 为什么出现

每个 AI 应用为每个外部系统重复设计插件协议，会形成 N×M 集成。MCP 统一能力发现、Schema、调用、资源读取和 Prompt 获取，让 Server 可被不同 Host 使用。

## 3. 不使用会怎样

自定义 REST/函数仍可工作，小项目不一定需要 MCP。跨多个 Host 复用、动态发现或第三方生态连接时，自定义适配成本会变高。

## 4. 核心原理

### 4.1 组件

- Host：协调多个 Client、模型、用户同意和安全策略。
- Client：与一个 Server 建立隔离连接并处理协议。
- Server：暴露聚焦的能力，不应看到整个对话或其他 Server 数据。

### 4.2 三种 Primitive

| Primitive | 主要控制者 | 用途 |
| --- | --- | --- |
| Tool | 模型决定调用 | 执行动作/查询 |
| Resource | 应用决定读取 | 向上下文加载数据 |
| Prompt | 用户决定选择 | 可复用消息模板 |

### 4.3 Transport 与权限

常见 transport 包括 stdio、Streamable HTTP 等。stdio 凭据通常来自进程环境；远程 HTTP 需要认证、HTTPS、短期 Token、用户同意和服务端授权。Transport 已认证不代表具体工具已授权。

### 4.4 Capability Negotiation

Client 只调用 Server 声明支持的能力。工具列表可能变化；Host 要控制哪些 Server/Tool 对当前用户可见。

## 5. 最小代码实现（当前 v2）

```python
from mcp.server import MCPServer

mcp = MCPServer("course-tools")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@mcp.resource("course://overview")
def overview() -> str:
    return "Agent course overview"

@mcp.prompt()
def review(topic: str) -> str:
    return f"Review {topic} with examples and counterexamples."
```

`projects/06_mcp_agent/server.py` 同时展示文件、数据查询和外部 API 形态。实际运行前安装 `mcp[cli]` 并重新检查 SDK 文档。

## 6. Agent 框架接入

Host 获取 MCP tools 后，可以把 Schema 交给自己的 Agent Runtime、LangGraph 或 Agents SDK。MCP Tool 的错误仍应作为可观察结果处理；Host 负责选择、审批、超时和 Trace。

## 7. 实际场景

- IDE Host 连接文件、GitHub、数据库 Server。
- 企业助手连接多个业务域 Server，按用户权限过滤。
- 本地数据工具通过 stdio 隔离进程，远程 SaaS 通过 HTTPS/OAuth。

## 8. 常见错误

继续复制 v1 `FastMCP` 教程、Server 工具权限过宽、把绝对路径交给模型、把用户 Token 记录进 Trace、Server 聚合过多领域、Tool/Resource 语义混乱、认为安装 MCP 就有 Agent Planning。

## 9. Debug 方法

先单独启动 Server；用 Inspector 或内存 Client 检查 capabilities、list、call/read/get；验证 `is_error`；记录 request id、tool name、授权主体、耗时和结构化错误。区分连接、发现、Schema、授权、执行和结果注入六层。

## 10. 思考题

1. 查询员工目录应该是 Tool 还是 Resource？
2. 一个 Server 应否同时暴露财务和人事写操作？
3. Host 如何防止来自 Resource 的 Prompt Injection？

## 11. 实战任务与验收

实现 MCP Server：安全文件读取、参数化数据查询、一个外部只读 API；再用 Client 列表和调用。验收：当前 v2 API；路径与权限边界；错误可读；敏感写操作需审批；能解释 MCP 与 Tool Registry、Agent Loop 的关系。

