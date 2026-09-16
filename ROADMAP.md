# Agent 开发学习路线（16 周）

## 使用规则

- `[x]` 只表示已经完成并通过验收，不表示“文件已经生成”。
- 每周默认时间分配：理论 20%、代码 30%、项目 40%、复盘 10%。
- 难度按 Level 1 理解 → Level 2 能写 → Level 3 能修改 → Level 4 能 Debug → Level 5 能设计递进。
- 每周结束后更新 `PROGRESS.md`；基础未通过验收时不机械进入下一周。
- 带版本变化风险的框架，在进入该周时重新查询官方文档、官方 GitHub 和官方示例。

## 资料交付清单

- [x] Stage 0–11 简体中文教材
- [x] 16 周学习安排和逐周验收
- [x] 两个渐进示例与 10 个项目参考实现
- [x] 架构案例、Debug Labs 和项目复盘模板
- [x] 30 条 Agent Evaluation 数据集与自动评测器
- [x] 2026-08-27 官方框架/MCP 资料快照

下面 Phase/周计划中的未勾选项表示“学习者尚未自我验收”，不表示资料缺失。

## 总体阶段

### Phase 1 Agent Foundation

- [ ] Stage 0：Agent 全景与最小循环
- [ ] Stage 1：Messages、Prompt、结构化输出与 Tool Calling
- [ ] Stage 2：ReAct 与可控 Agent Loop

### Phase 2 Agent Architecture

- [ ] Stage 3：State 与 Memory
- [ ] Stage 4：Workflow 与状态机
- [ ] Stage 5：RAG 与 Agentic RAG
- [ ] Stage 6：MCP

### Phase 3 Advanced Agent

- [ ] Stage 7：主流框架与官方 Agent SDK
- [ ] Stage 8：Multi-Agent
- [ ] Stage 9：Agent 工程化
- [ ] Stage 10：Agent Evaluation
- [ ] Stage 11：毕业项目与最终能力测试

## 第 1 周：Agent 全景与最小循环（Stage 0）

- [ ] 学习目标：解释 LLM 应用、Workflow、Agent、Multi-Agent 的边界；画出 Agent Loop。
- [x] 教材：`docs/00_agent_overview.md`。
- [x] Demo：`examples/00_simple_agent/`，纯 Python、无 Agent 框架、可显示轨迹。
- [ ] 练习：手绘消息和工具结果在循环中的变化；修改最大步数并制造一次失败。
- [ ] 项目任务：为 Calculator 增加除零错误实验，不重写运行时。
- [ ] 源码阅读：只读 `Agent.run`，按入口→循环→数据结构→工具调用→停止条件追踪。
- [ ] 复盘问题：为什么 Demo 的离线模型不是 LLM？为什么它仍能验证 Runtime？
- [ ] 验收：能不用代码提示写出伪代码；能解释 max steps；能定位工具错误；能判断一个固定流程不该使用 Agent。

## 第 2 周：LLM 应用基础（Stage 1）

- [ ] 学习目标：掌握 Message、System Prompt、Context、Temperature、Token、Structured Output。
- [ ] 教材：`docs/01_llm_foundation.md` 与结构化输出实验笔记。
- [ ] Demo：文本回答 → JSON 输出 → JSON Schema 校验三个版本。
- [ ] 练习：设计一个有约束的任务分解 Schema，并处理缺字段、错类型与额外字段。
- [ ] 项目任务：创建 `projects/01_tool_agent/` 的需求和最小模型适配层。
- [ ] 源码阅读：只研究一个官方 Python SDK 如何把 Responses 输出解析为类型对象。
- [ ] 复盘问题：Prompt 约定 JSON 与 Schema 强约束有什么不同？
- [ ] 验收：能解释上下文不等于记忆；能复现并定位一次结构化输出失败。

## 第 3 周：Tool Calling 逐层演进（Stage 1）

- [ ] 学习目标：理解 Tool Schema、选择、参数、返回值、异常、超时、重试和权限。
- [ ] 教材：`docs/02_tool_calling.md`。
- [ ] Demo：V1 单工具 → V2 多工具 → V3 Tool Registry → V4 Trace。
- [ ] 练习：实现 Calculator、公开天气 API 或替代 API、Local Search、File Reader。
- [ ] 项目任务：完成 `projects/01_tool_agent/`，保留每次工具调用记录。
- [ ] 源码阅读：只研究官方 SDK 中一次 Function Call 的对象结构与回传链路。
- [ ] 复盘问题：为什么工具描述会影响选择准确率？什么工具不应暴露给模型？
- [ ] 验收：能新增工具而不改 Agent 主循环；能处理参数错误、超时和未知工具。

## 第 4 周：ReAct 与 Agent Loop（Stage 2）

- [ ] 学习目标：理解 Reason、Action、Observation、Final Answer、停止条件和步数预算。
- [ ] 教材：`docs/03_agent_loop.md`。
- [ ] Demo：`examples/02_react/`，从单步工具调用扩展为多步循环。
- [ ] 练习：构造死循环、重复调用、JSON 错误和上下文膨胀四类故障。
- [ ] 项目任务：完成 `projects/02_react_agent/` 的 Mini Agent 与轨迹日志。
- [ ] 源码阅读：只研究一个开源 Agent Runtime 的 run loop 调用链。
- [ ] 复盘问题：模型说“完成”是否足以作为停止条件？
- [ ] 验收：不用框架实现循环；能限制步数、识别重复轨迹并解释何时不该使用 Agent。

## 第 5 周：State 与短期记忆（Stage 3）

- [ ] 学习目标：区分 History、Context、State、Memory、Checkpoint。
- [ ] 教材：`docs/04_memory.md` 的前半部分。
- [ ] Demo：内存变量与 SQLite 两种偏好存储。
- [ ] 练习：定义会话状态 Schema；实现保存、读取、修改、删除。
- [ ] 项目任务：启动 `projects/03_memory_agent/`，先实现内存变量版。
- [ ] 源码阅读：只研究 SQLite checkpoint 的写入与恢复路径。
- [ ] 复盘问题：聊天历史越多，助手就“记得越好”吗？
- [ ] 验收：能从 checkpoint 恢复任务；能避免把所有历史无限塞回上下文。

## 第 6 周：长期、语义与情节记忆（Stage 3）

- [ ] 学习目标：理解 Long-term、Semantic、Episodic、Working Memory 的用途和边界。
- [ ] 教材：`docs/04_memory.md` 的后半部分与对照实验报告。
- [ ] Demo：SQLite 精确读取 vs 向量数据库语义读取。
- [ ] 练习：设计记忆写入门槛、冲突处理、过期和删除策略。
- [ ] 项目任务：完成 `projects/03_memory_agent/` 三种方案的质量、成本和延迟比较。
- [ ] 源码阅读：只研究一个向量库的相似度查询入口和数据结构。
- [ ] 复盘问题：RAG 为什么不自动等于 Memory？
- [ ] 验收：能解释误记和污染风险；能为不同数据选择关系库或向量库。

## 第 7 周：从零实现 Workflow（Stage 4）

- [ ] 学习目标：掌握 Sequential、Router、Conditional Branch、Parallel、Retry、Loop、DAG。
- [ ] 教材：`docs/05_workflow.md` 的框架无关部分。
- [ ] Demo：用 Python 函数和显式 State 实现小型状态机。
- [ ] 练习：为每条边写进入条件、退出条件和失败策略。
- [ ] 项目任务：设计 `projects/04_research_workflow/` 的 State、Node、Edge，暂不接框架。
- [ ] 源码阅读：只研究自制状态机的调度入口和状态更新规则。
- [ ] 复盘问题：哪些决策应写死在边上，哪些才交给 LLM Router？
- [ ] 验收：能画 DAG；能实现条件分支、重试和人工批准节点。

## 第 8 周：LangGraph 与研究工作流（Stage 4）

- [ ] 学习目标：把已理解的 State/Node/Edge 映射到当前 LangGraph 抽象。
- [ ] 教材：`docs/05_workflow.md` 的框架实现部分，进入本周时更新 API。
- [ ] Demo：同一流程的自制状态机版与 LangGraph 版。
- [ ] 练习：增加并行检索、失败重试、checkpoint 和完整 Trace。
- [ ] 项目任务：完成 `projects/04_research_workflow/`。
- [ ] 源码阅读：只研究 LangGraph StateGraph 如何合并与保存 State。
- [ ] 复盘问题：框架减少了哪些代码，又隐藏了哪些运行细节？
- [ ] 验收：能显示完整轨迹；能从 checkpoint 恢复；能解释每个节点的确定性边界。

## 第 9 周：RAG 基础（Stage 5）

- [ ] 学习目标：理解 Chunk、Embedding、Vector Search、BM25、Hybrid Search、Rerank。
- [ ] 教材：`docs/06_agentic_rag.md` 的普通 RAG 部分。
- [ ] Demo：朴素检索 → BM25/向量 → 混合检索 → Rerank。
- [ ] 练习：构造“检索到了但回答错”和“根本没召回”的不同失败。
- [ ] 项目任务：为 `projects/05_agentic_rag/` 建立小型可评测语料与问题集。
- [ ] 源码阅读：只研究一个检索器的 query→score→top-k 链路。
- [ ] 复盘问题：生成失败与检索失败如何区分？
- [ ] 验收：能用 Recall@k 等指标定位召回问题；能解释切块策略的影响。

## 第 10 周：Agentic RAG（Stage 5）

- [ ] 学习目标：掌握 Query Rewrite、检索选择、重试、Web 补充与证据验证。
- [ ] 教材：`docs/06_agentic_rag.md` 的 Agentic RAG 部分。
- [ ] Demo：固定 RAG 与可决策检索流程的对照实验。
- [ ] 练习：限制最多改写和检索次数，避免“为了检索而检索”。
- [ ] 项目任务：完成 `projects/05_agentic_rag/` 并记录引用证据。
- [ ] 源码阅读：只研究一个 Agentic RAG 示例的路由条件。
- [ ] 复盘问题：哪些检索策略用 Workflow 足够，不需要 Agent？
- [ ] 验收：能解释每次检索决策；有停止条件；对照普通 RAG 的质量、成本和延迟。

## 第 11 周：MCP（Stage 6）

- [ ] 学习目标：理解 Host、Client、Server、Tool、Resource、Prompt、Transport、权限边界。
- [ ] 教材：`docs/07_mcp.md`，进入本周时按当前规范更新。
- [ ] Demo：最小 MCP Server 与本地 Client。
- [ ] 练习：暴露文件、数据查询、外部 API 三类能力并限制权限。
- [ ] 项目任务：完成 `projects/06_mcp_agent/`。
- [ ] 源码阅读：只研究官方 MCP SDK 的 tool registration 与 request dispatch。
- [ ] 复盘问题：MCP 解决互操作问题，但没有替你解决哪些 Agent 问题？
- [ ] 验收：能画 Host→Client→Server；能解释传输与权限；能排查工具发现和调用失败。

## 第 12 周：框架调研与官方 Agent SDK（Stage 7）

- [ ] 学习目标：比较 LangChain、LangGraph、OpenAI Agents SDK、AutoGen、CrewAI、MCP 生态。
- [ ] 教材：`docs/agent_framework_comparison.md`，只使用进入本周时核验的官方资料。
- [ ] Demo：用一个官方 Agent SDK 重做受控的小型 Agent，并与自制 Runtime 对照。
- [ ] 练习：把框架抽象映射回 Loop、State、Tool、Trace、Handoff。
- [ ] 项目任务：形成框架选型 ADR，不以“功能多”作为唯一理由。
- [ ] 源码阅读：只研究官方 Agent SDK 如何执行一次 Tool Calling。
- [ ] 复盘问题：更换框架时，哪些领域模型与工具代码应该保持不变？
- [ ] 验收：完成比较表；能为三个业务场景说明选型和不选型理由。

## 第 13 周：Multi-Agent（Stage 8）

- [ ] 学习目标：掌握 Supervisor、Worker、Planner、Executor、Reviewer、Handoff。
- [ ] 教材：`docs/08_multi_agent.md`。
- [ ] Demo：单 Agent vs Supervisor+Workers 的同题实验。
- [ ] 练习：跟踪消息重复、错误传播、通信开销和失败责任归属。
- [ ] 项目任务：完成 `projects/07_multi_agent/`。
- [ ] 源码阅读：只研究一个框架的 handoff 或 supervisor dispatch 链路。
- [ ] 复盘问题：角色 Prompt 不同是否足以证明需要多个 Agent？
- [ ] 验收：报告 Token、延迟、成功率和通信成本；能识别 Multi-Agent 过度设计。

## 第 14 周：Agent 工程化（Stage 9）

- [ ] 学习目标：掌握 FastAPI、Async、Streaming、Queue、Timeout、Rate Limit、Auth、Docker。
- [ ] 教材：`docs/09_agent_engineering.md`。
- [ ] Demo：同步调用 → Async → SSE；加入 request id、结构化日志和 Trace。
- [ ] 练习：模拟客户端断开、工具超时、重试风暴、限流和幂等问题。
- [ ] 项目任务：完成 `projects/08_agent_service/` 的最小垂直切片。
- [ ] 源码阅读：只研究服务入口到 Agent Runtime 的一次请求调用链。
- [ ] 复盘问题：Agent 状态应该存在 Web 进程内吗？
- [ ] 验收：服务可启动、可流式响应、可取消；错误可追踪；密钥不进入日志或仓库。

## 第 15 周：Agent Evaluation（Stage 10）

- [ ] 学习目标：掌握 Golden Dataset、Task Success、Tool Accuracy、Trajectory、Cost、Latency。
- [ ] 教材：`docs/10_agent_evaluation.md`。
- [ ] Demo：确定性断言 + LLM-as-Judge + 人工抽检的组合评测。
- [ ] 练习：设计至少 30 个正常、边界、对抗和工具失败问题。
- [ ] 项目任务：完成 `projects/09_agent_eval/` 与回归报告。
- [ ] 源码阅读：只研究一个官方 eval runner 如何加载样本和聚合指标。
- [ ] 复盘问题：Judge 分数提高是否等于真实任务成功率提高？
- [ ] 验收：自动统计成功率、工具准确率、步数、Token、成本、延迟和失败原因。

## 第 16 周：毕业项目与最终能力测试（Stage 11）

- [ ] 学习目标：完成从需求判断到架构、实现、Debug、Evaluation 的闭环。
- [ ] 教材：只补毕业项目实际遇到的专题，不生成新的大而全教程。
- [ ] Demo：Research Agent 的最小垂直切片和简单 Web UI。
- [ ] 练习：故障注入、证据冲突、长任务恢复、权限拒绝与回归测试。
- [ ] 项目任务：完成 `projects/10_ai_research_agent/` 的可演示版本与 `PROJECT_REVIEW.md`。
- [ ] 源码阅读：沿毕业项目的一次真实 Trace 反查框架入口、核心类、状态和工具调用链。
- [ ] 复盘问题：如果重写，哪些部分改为确定性 Workflow，哪些保留 Agent？
- [ ] 验收：独立完成一个无标准答案的 Agent 架构设计，并能在技术 Review 中解释取舍。

## Stage 0 验收维度

- [ ] 理论目标：能解释 LLM、Agent Loop、Tool、Observation、State、Memory、Workflow、RAG、MCP、Multi-Agent 的关系。
- [ ] 开发目标：能独立写出一个带最大步数和工具分发的最小循环。
- [ ] 项目目标：能运行并修改 `00_simple_agent`，新增一个简单只读工具。
- [ ] Debug 目标：能定位未知工具、参数 JSON 错误、工具异常和达到最大步数。
- [ ] 架构目标：面对固定、可预测步骤的任务，能说明为什么优先 Workflow 而不是 Agent。
