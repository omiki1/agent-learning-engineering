# 现代 AI Agent 开发学习工程

这是一套一次性交付、能力导向的 Agent 自学资料。目标不是背诵某个框架的 API，而是能够独立判断何时需要 LLM、工作流（Workflow）或智能体（Agent），并完成设计、实现、调试、评测与工程化。

学习顺序固定为：

```text
原理 → 最小实现 → 框架实现 → 工程化 → 项目实战 → 调试 → 评测 → 架构设计
```

## 当前状态

- 资料状态：Stage 0–11 教材、练习和项目参考实现一次性提供
- 建议起点：Stage 0——Agent 全景与最小循环
- 使用方式：可以按 16 周学习，也可以按主题检索
- 验收原则：资料已经提供不等于学习者已经掌握

如需记录自己的掌握情况，可使用 [PROGRESS.md](PROGRESS.md)；完整目录见 [ROADMAP.md](ROADMAP.md)。

## 学习路线

```text
基础概念与最小循环
        ↓
Tool Calling 与 ReAct
        ↓
State、Memory、Workflow
        ↓
RAG、MCP、主流框架
        ↓
Multi-Agent 与工程化
        ↓
Evaluation 与毕业项目
```

完整的 16 周计划见 [ROADMAP.md](ROADMAP.md)。每周时间建议保持：理论 20%、代码 30%、项目 40%、复盘 10%。

## 技术栈

技术栈会随阶段逐步引入，不在开始时一次安装：

| 阶段 | 主要技术 |
| --- | --- |
| Stage 0–2 | Python 3.11+、标准库、JSON Schema、可选 OpenAI Python SDK |
| Stage 3 | SQLite、向量数据库实验 |
| Stage 4 | 自制状态机、LangGraph |
| Stage 5 | Embedding、BM25、Hybrid Search、Rerank |
| Stage 6 | MCP Python SDK、MCP Server/Client |
| Stage 7–8 | OpenAI Agents SDK、LangGraph；AutoGen/CrewAI 以比较为主 |
| Stage 9 | FastAPI、Async、SSE/WebSocket、Redis、PostgreSQL、Docker |
| Stage 10–11 | 自动评测、Trace、回归测试、简单 Web UI |

第三方框架开始使用前，必须重新检查其当前官方文档、官方仓库与推荐 API，路线中的技术名不代表锁定版本。

## 目录

```text
docs/       分阶段教材，只按学习进度生成
notes/      学习者自己的笔记
examples/   单一概念的最小 Demo
projects/   各阶段项目，按需求→设计→实现→Debug→评测推进
exercises/  练习与设计题
resources/  数据集、样例资料与资源索引
tests/      自动化测试
```

`projects/` 提供 01–10 的可运行参考实现。建议先按 README 自己设计，再查看代码，而不是从复制答案开始。

## 环境变量

需要连接真实模型、数据库或外部工具时，把 [.env.example](.env.example) 复制为 `.env` 并填入自己的凭据：

```powershell
Copy-Item .env.example .env
```

`.env` 已被 `.gitignore` 忽略，**不要提交真实 API Key、邮箱授权码或数据库口令**。只跑离线 Demo 和单元测试时不需要任何凭据。

## 运行第一个 Demo

离线模式不需要 API Key，也不需要安装第三方包：

```powershell
python examples/00_simple_agent/main.py --offline
```

指定一个算术问题：

```powershell
python examples/00_simple_agent/main.py --offline --question "请计算 (23 + 19) * 2"
```

运行测试：

```powershell
python -m unittest discover -s tests -v
```

可选的真实模型模式及其边界见 [examples/00_simple_agent/README.md](examples/00_simple_agent/README.md)。Stage 0 的重点是读懂循环，不是配置云服务。

## 项目列表

| 项目 | 核心能力 | 状态 |
| --- | --- | --- |
| 01 Tool Agent | 多工具选择与工具注册 | 资料已提供 |
| 02 ReAct Agent | Agent Loop、停止条件、错误恢复 | 资料已提供 |
| 03 Memory Agent | 短期/长期记忆、SQLite、向量检索 | 资料已提供 |
| 04 Research Workflow | 状态机、路由、并行、重试、轨迹 | 资料已提供 |
| 05 Agentic RAG | 查询改写、混合检索、重试与验证 | 资料已提供 |
| 06 MCP Agent | MCP Server、Client、权限边界 | 资料已提供 |
| 07 Multi-Agent | Supervisor/Worker 与单 Agent 对照 | 资料已提供 |
| 08 Agent Service | FastAPI、流式输出、队列与可观测性 | 资料已提供 |
| 09 Agent Eval | 30+ 测试集、成功率、成本与回归 | 资料已提供 |
| 10 AI Research Agent | 综合毕业项目与 Web UI | 资料已提供 |

## 自学约定

1. 每个项目先读需求并自行画出 Tool、State 和数据流，再看参考实现。
2. 遇到 Bug 时先根据 Trace 定位，不立即重写。
3. 每个项目结束后回答项目 README 中的复盘问题。
4. 不因为“代码能运行”就判定掌握；必须完成对应验收。

## 完整教材

| 文档 | 主题 |
| --- | --- |
| `docs/00_agent_overview.md` | Agent 全景与架构判断 |
| `docs/01_llm_foundation.md` | Message、Prompt、Context、Structured Output |
| `docs/02_tool_calling.md` | Tool Schema、Registry、错误与权限 |
| `docs/03_agent_loop.md` | ReAct、循环、停止条件、Trace |
| `docs/04_memory.md` | State、Checkpoint 与多类 Memory |
| `docs/05_workflow.md` | 状态机、DAG、路由、并行、HITL、LangGraph |
| `docs/06_agentic_rag.md` | RAG、Hybrid、Rerank、Agentic RAG |
| `docs/07_mcp.md` | MCP v2 架构、Server/Client 与权限边界 |
| `docs/agent_framework_comparison.md` | 当前主流框架与选型 |
| `docs/08_multi_agent.md` | Supervisor、Handoff 与过度设计判断 |
| `docs/09_agent_engineering.md` | API、Async、Streaming、可靠性与安全 |
| `docs/10_agent_evaluation.md` | 数据集、指标、Trajectory 与回归测试 |
| `docs/11_capstone.md` | AI Research Agent 毕业项目 |
