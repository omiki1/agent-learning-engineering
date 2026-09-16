# 11｜毕业项目：AI Research Agent

## 目标

不是做聊天机器人，而是完成一个带证据、可恢复、可评测的研究系统。

```text
Question
  ↓
Intent & Scope
  ↓
Plan
  ↓
Search/RAG ─→ Read ─→ Evidence Store
  ↑                      ↓
  └──── Evidence Gate ← Compare/Critic
                         ↓
                   Structured Report
                         ↓
                    Human Review
```

## 功能要求

- Planning：结构化计划和动态调整。
- Tool Calling：搜索、读取、检索和引用。
- RAG：本地资料和证据索引。
- Memory：用户偏好与任务 checkpoint 分开。
- Workflow：固定边界包住 Agentic 探索节点。
- MCP：至少一个独立 Server。
- Streaming：阶段事件而非隐藏推理。
- Trace：每步 State diff、工具和停止原因。
- Evaluation：30+ 问题、引用与轨迹指标。
- Error Handling：超时、空结果、冲突证据、取消和恢复。

## State 设计

```python
class ResearchState(TypedDict):
    run_id: str
    question: str
    scope: dict
    plan: list[dict]
    evidence: list[dict]
    open_questions: list[str]
    retries: dict[str, int]
    report: dict | None
    status: str
```

大网页/PDF 保存为 Artifact，State 只保存 id、摘要、来源、hash 和引用位置。

## Tool 设计

| Tool | 输入 | 输出 | 风险控制 |
| --- | --- | --- | --- |
| search | query、时间范围 | result ids | 来源和次数限制 |
| read_source | source id | text/artifact id | 下载大小/类型限制 |
| retrieve | query、filters | chunks | 租户和文档过滤 |
| save_report | run id、report | artifact id | 版本和路径限制 |

## Workflow/Agent 边界

确定性：鉴权、输入校验、文档解析、状态持久化、引用格式、预算、审批、导出。

Agentic：研究计划、搜索 Query、证据缺口判断、冲突比较。即使是 Agentic 节点，也必须有枚举输出、预算和 fallback。

## 里程碑

1. 垂直切片：一个问题→本地检索→带引用回答。
2. 证据层：多来源、Evidence Gate、abstain。
3. Runtime：循环、Trace、Checkpoint、取消。
4. 服务：FastAPI、SSE、简单 Web UI。
5. MCP：外部工具 Server。
6. Evaluation：30+ 数据集和回归阈值。

## Definition of Done

- 不联网也有离线 Demo。
- 每个结论能追溯到证据。
- 证据不足会停止或明确说明，不编造。
- 重启后能从 checkpoint 恢复且不重复副作用。
- 可观察 Token、延迟、工具成功率和轨迹。
- 与“固定 Workflow”和“单 Agent”基线对比。

## 项目复盘

1. 为什么使用 Agent？不用 Agent 能否完成？
2. 哪些步骤最终改成了 Workflow？
3. 最大 Bug 和发现方式是什么？
4. Agent 最常选错哪个 Tool？
5. 当前成本和延迟瓶颈在哪里？
6. 如果重写，State、Tools、Memory 和评测会怎样改变？

## 最终能力测试

独立设计一个 AI 软件开发 Agent。提交：需求判断、Workflow/Agent 边界、State、Tools、Memory、MCP、权限、数据流、目录、停止条件、失败恢复和 Evaluation。评分重点是能否解释取舍，而不是是否使用最多框架。

