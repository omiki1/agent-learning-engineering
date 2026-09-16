# 官方资料索引

核验日期：2026-08-27。快速变化的项目在实际使用前仍应重新打开官方文档确认。

## OpenAI

- [Responses API](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Agents、Runner 与编排](https://openai.github.io/openai-agents-python/agents/)
- [Tracing](https://openai.github.io/openai-agents-python/tracing/)

当前官方说明中，Agents SDK 默认以 Responses API 对接 OpenAI 模型，并由 `Agent` + `Runner` 管理工具、Handoff、Guardrail、Session 和多轮执行；如果希望自行拥有循环，则直接使用 Responses API。

## LangChain / LangGraph

- [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)

当前官方定位：LangChain 是较高层 Agent Framework；LangGraph 是低层编排 Runtime，强调 durable execution、streaming、human-in-the-loop 和 persistence。LangChain 的 Agent Runtime 构建在 LangGraph 之上。

## MCP

- [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [2026-07-28 Specification Update](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP Python SDK v2](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/index.md)
- [Python SDK First Steps](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/get-started/first-steps.md)

当前 Python SDK 稳定线为 v2，使用 `from mcp.server import MCPServer`。许多旧教程中的 `FastMCP` 属于 v1 API。Tools、Resources、Prompts 分别主要由模型、应用、用户控制。

## AutoGen / Microsoft Agent Framework

- [AutoGen AgentChat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/index.html)
- [AutoGen Core](https://microsoft.github.io/autogen/)
- [AutoGen → Microsoft Agent Framework Migration](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)

AutoGen 仍适合学习 AgentChat、事件驱动 Runtime 和 GroupChat 思想；微软官方迁移指南把 Microsoft Agent Framework 描述为新的长期基础。新项目选型必须同时评估迁移方向。

## CrewAI

- [CrewAI Documentation](https://docs.crewai.com/)

CrewAI 以 Agent、Task、Crew 和 Flow 为主要抽象，适合角色化协作和业务 Flow；学习时必须与单 Agent 或显式 Workflow 做成本和可靠性对照。

