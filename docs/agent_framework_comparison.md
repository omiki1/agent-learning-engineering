# Agent 框架比较与选型（2026-08-27 快照）

> 框架变化很快。本文比较定位和抽象，不把某个短期 API 当作永恒答案。实际安装前重新查阅 `resources/official_sources.md`。

## 比较表

| Framework | 定位 | Workflow | Agent | Multi-Agent | State | Memory | Tools | MCP | 适用场景 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LangChain | 高层 LLM/Agent 框架与集成层 | 通过 LangGraph | `create_agent` 预制循环 | 可组合 | 基于 LangGraph | 短期/长期接口 | 丰富集成、动态工具 | 可集成 | 快速构建常见 Agent、需要多模型/工具生态 |
| LangGraph | 低层有状态编排 Runtime | 强：Graph/DAG/Loop/HITL | 自定义或 prebuilt | Supervisor/Swarm 等生态 | 强、显式 State | Checkpointer + Store | 自由组合 | 可集成 | 长运行、恢复、精细控制、Workflow+Agent 混合 |
| OpenAI Agents SDK | 轻量官方 Agent 编排 SDK | `Runner`、agents-as-tools、Handoff | 强 | Manager/Handoff | Context、Session、Run result | Session/自定义存储 | Function/MCP/Hosted tools | 强 | OpenAI Responses 生态、Guardrail、Handoff、内置 Trace |
| AutoGen AgentChat/Core | 对话式与事件驱动多 Agent 框架 | Core 可做事件流程 | 强 | GroupChat/Team | Agent/Team state | 扩展与自定义 | Function、Workbench | 有 | 研究多 Agent 协作、事件驱动/分布式 Runtime |
| Microsoft Agent Framework | 微软新的 Agent/Workflow 长期方向 | 强 | 强 | 强 | Thread/Workflow state | provider-dependent | 工具与中间件 | 需按当前文档 | 新微软生态项目；应同时查看迁移与成熟度 |
| CrewAI | 角色化 Agent、Task、Crew 与 Flow | Flow、router/listen | 强 | Crew/层级流程 | Flow state | 内置/扩展 | 丰富工具 | 需按当前文档 | 角色化业务自动化、快速构建 Crew/Flow |
| MCP | 协议/生态，不是 Agent 框架 | 无 | 无 | 无 | 协议交互状态 | Resource 不是 Memory | Tools/Resources/Prompts | 本身 | 跨 Host/Server 的能力互操作与权限隔离 |

## 当前定位变化

### LangChain 与 LangGraph

官方当前把 LangChain 定位为高层 Agent Framework，把 LangGraph 定位为低层 orchestration runtime。LangChain `create_agent` 运行在 LangGraph 上。需要快速常见 Agent 用 LangChain；需要节点、边、持久化、HITL 和长任务控制时直接用 LangGraph。

### OpenAI Agents SDK

当前 SDK 以 `Agent` + `Runner` 管理工具循环、Guardrail、Handoff、Session 和 Trace，OpenAI 模型默认使用 Responses API。若要完全控制循环，直接使用 Responses API 或自己的 Runtime。

### AutoGen 的方向

AutoGen AgentChat/Core 仍是重要学习对象，尤其是 GroupChat、消息和事件驱动 Runtime。但微软官方已发布 AutoGen → Microsoft Agent Framework 迁移指南，并把后者描述为新的长期基础。新项目不应只根据旧 AutoGen 教程选型。

### CrewAI

CrewAI 把 Agent、Task、Crew、Process 与 Flow 放在核心位置，适合角色化协作和业务自动化。必须用单 Agent/Workflow 基线验证 Crew 是否真的提高成功率。

### MCP

MCP 只解决互操作：Host/Client/Server 发现和调用 Tools、Resources、Prompts。它不替代 Agent Loop、Workflow、Memory 或 Evaluation。

## 选型决策树

```text
单次模型/结构化抽取能完成？ ──是→ 不用 Agent 框架
        │否
步骤是否固定且需要可靠恢复？ ──是→ Workflow Runtime
        │否/部分
是否需要动态工具循环？ ──是→ Agent SDK 或自制 Runtime
        │
是否需要低层 Graph/HITL/Checkpoint？ ──是→ LangGraph 类 Runtime
        │
是否主要在 OpenAI 生态并需要 Handoff/Trace？ ──是→ OpenAI Agents SDK
        │
是否有真实多 Agent、事件驱动/角色化需求？
        ├─ 事件/研究 → AutoGen/Core 或 Microsoft Agent Framework
        └─ Crew/业务 Flow → CrewAI
跨应用复用工具？ → 在以上架构外增加 MCP
```

## 评分矩阵

按业务权重打分，而不是比较功能数量：

| 维度 | 问题 |
| --- | --- |
| 控制 | 能否显式定义停止、状态和审批？ |
| 可恢复 | 长任务中断后能否幂等恢复？ |
| 可观察 | 是否能记录模型、工具、状态 diff 和成本？ |
| 生态 | 需要哪些模型、工具、数据库和 MCP？ |
| 锁定 | 领域逻辑能否脱离框架测试？ |
| 成熟度 | API、迁移路线、维护者方向是否清晰？ |
| 团队 | 团队是否理解其隐藏的 Runtime？ |

## 推荐学习深度

```text
深入：LangGraph（Workflow/State）
+ OpenAI Agents SDK（官方 Agent SDK）
+ MCP v2（协议）

理解思想：LangChain、AutoGen/Microsoft Agent Framework、CrewAI
```

## 源码阅读路线

每次只研究一个问题：

1. LangGraph：StateGraph 编译后如何调度 Node、保存 checkpoint。
2. Agents SDK：Runner 如何从模型 Tool Call 进入函数并形成 RunItem。
3. AutoGen Core：Runtime 如何按消息类型路由到 handler。
4. CrewAI Flow：router/listen 如何改变 Flow state。
5. MCP SDK：`@mcp.tool()` 如何从签名生成 Schema 并注册 handler。

## 选型验收题

分别为“工单分类”“长运行报表审批”“开放式研究”“跨 IDE 文件工具”“三角色代码审查”选型。必须同时说明不选择其他方案的原因、最小可行架构和回退策略。

