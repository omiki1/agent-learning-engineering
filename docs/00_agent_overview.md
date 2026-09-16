# 00｜Agent 全景：先理解运行机制，再学习框架

## 本章目标

完成本章后，你应该能够：

1. 区分普通 LLM 应用、工作流（Workflow）、智能体（Agent）和多智能体（Multi-Agent）。
2. 解释一次 Agent Loop 中 Reason、Action、Tool、Observation 的数据流。
3. 读懂一个不依赖 Agent 框架的最小 Python Runtime。
4. 说明最大步数、停止条件、工具权限和执行轨迹为何不是“附加功能”。
5. 面对一个需求，先判断是否真的需要 Agent。

本章只建立地图和最小实现。结构化输出、完整 Tool Calling、Memory、RAG、MCP 和框架 API 会在后续阶段分别展开。

---

## 1. 它是什么

### 1.1 LLM 与传统程序

传统程序主要执行开发者已经写明的规则：

```python
if amount > balance:
    reject()
else:
    pay()
```

大语言模型（Large Language Model, LLM）根据输入上下文预测输出。它擅长处理自然语言、非结构化信息和模糊任务，但输出具有概率性，不能天然保证事实正确、格式合法或动作安全。

因此，LLM 适合参与“理解和生成”，确定性程序仍应负责权限、金额、数据校验、状态持久化和不可逆操作。

### 1.2 Chat Model、Prompt 与 Message

- Chat Model：以消息序列为主要交互形式的模型。
- 提示词（Prompt）：给模型的任务说明和上下文，不只是一句话。
- 消息（Message）：带角色和内容的数据，例如 system/developer、user、assistant、tool。
- System Prompt：描述身份、边界和长期规则，但它不是安全边界；真正的权限仍由程序控制。

最小聊天应用通常是：

```text
User Message → LLM → Assistant Message
```

如果一次模型调用已经能可靠完成任务，就没有必要增加 Agent Loop。

### 1.3 Agent

本课程把 Agent 定义为：

> 一个让模型在受控循环中观察当前状态、选择下一步动作、调用外部能力，并根据结果继续决策，直到满足停止条件的运行系统。

关键不在“使用了 LLM”，而在模型拥有一定的动态决策权：下一步做什么，可能在运行时才确定。

### 1.4 Agent Loop

```text
LLM
 │
 ▼
Reason
 │
 ▼
Action
 │
 ▼
Tool
 │
 ▼
Observation
 │
 └────────→ LLM
```

概念上可以写成：

```python
while not finished:
    decision = model(context, tools)

    if decision.is_final:
        return decision.answer

    observation = execute(decision.tool_call)
    context.append(observation)
```

真实系统至少还要加入：最大步数、参数校验、未知工具处理、异常隔离、超时、权限、Trace 和取消。

### 1.5 Tool、Action 与 Observation

- 工具（Tool）：程序提供给模型的受控能力，例如计算、读文件、查数据库。
- 动作（Action）：模型输出的下一步操作，常见形式是工具名和结构化参数。
- 观察（Observation）：工具执行结果，被追加回上下文供模型继续决策。

模型只“提出调用请求”。真正执行工具的是应用程序。这一区分决定了权限边界：模型不应绕过 Tool Registry 直接执行任意代码。

### 1.6 Structured Output、Function Calling 与 Tool Calling

- 结构化输出（Structured Output）：让模型按预定义结构输出数据。
- 函数调用（Function Calling）：模型输出函数名和参数，由应用执行函数。
- 工具调用（Tool Calling）：更宽泛的概念，工具可以是函数、搜索、文件、MCP 服务等。

三者都不能消除业务校验。Schema 合法只说明“形状正确”，不说明城市、文件路径、金额或用户权限合理。

### 1.7 State 与 Memory

- 状态（State）：当前任务运行所需的显式数据，例如当前步骤、计划、检索结果、重试次数。
- 记忆（Memory）：跨步骤或跨会话保留并在未来有选择地取回的信息。
- History：发生过的原始消息序列。
- Context：本次模型调用实际看到的输入。
- 检查点（Checkpoint）：某时刻可恢复的状态快照。

必须牢记：

```text
History != Memory
Context != Memory
State != Memory
RAG != Memory
```

例如，“用户喜欢简洁回答”可以是长期记忆；“目前已完成第 2 个检索步骤”是任务状态；把 500 条历史全部塞入 Context 不是好的记忆设计。

### 1.8 Planning 与 Reflection

- 规划（Planning）：把目标拆成步骤，并在执行中调整。
- 反思（Reflection）：对结果或轨迹进行检查并提出修正。

它们不是每个 Agent 的必选组件。简单任务强行先规划、再反思，通常只会增加 Token、延迟和新的失败点。确定性检查能解决的问题，优先使用代码断言或验证节点。

### 1.9 Workflow

Workflow 把步骤和转移规则显式写在程序中：

```text
提取文本 → 校验 → 查询数据库 → 生成报告
```

Agent 把部分下一步决策交给模型：

```text
当前证据是否足够？
├─ 是 → 生成回答
├─ 否，缺内部知识 → 检索知识库
└─ 否，缺当前信息 → 搜索 Web
```

现代 AI 系统常见的合理形态是“确定性 Workflow 包住少数 Agent 节点”，而不是让模型决定一切。

### 1.10 RAG 与 Agent

检索增强生成（Retrieval-Augmented Generation, RAG）通常是：

```text
Query → Retrieve → Context → LLM → Answer
```

Agentic RAG 允许系统动态决定是否检索、检索哪里、是否改写 Query、是否重试。但只要固定检索流程就能稳定解决问题，就不需要 Agentic RAG。

### 1.11 MCP

模型上下文协议（Model Context Protocol, MCP）是一种连接 Host、Client 与外部 Server 的协议层：

```text
Agent / Host
      ↓
MCP Client
      ↓
MCP Server
      ↓
External Service
```

MCP 解决工具和资源如何以统一方式被发现、描述和调用。它不会自动提供好的规划、记忆、停止条件、权限策略或评测。

### 1.12 Multi-Agent

Multi-Agent 表示多个具有独立职责、上下文或决策边界的 Agent 通过消息、Handoff 或 Supervisor 协作。

```text
Supervisor
 ├─ Researcher
 ├─ Developer
 └─ Reviewer
```

“同一个 LLM 调三次”并不自动成为合理的 Multi-Agent 架构。若单 Agent 加几个确定性步骤即可完成，拆成多个角色会增加通信开销、延迟、Token 和错误传播。

---

## 2. 为什么会出现 Agent

普通 LLM 调用有三个常见边界：

1. 模型训练知识不能可靠代表当前外部世界。
2. 模型不能仅靠文本预测安全地完成数据库查询、文件读取或业务动作。
3. 复杂任务中，下一步可能依赖刚刚得到的结果，无法在编码时完全预定。

Tool Calling 解决“如何请求外部能力”，Agent Loop 解决“得到结果以后如何继续决策”。

例如研究任务：第一次搜索后发现关键词有歧义，系统需要先改写查询；读完来源后发现证据冲突，需要补充另一类来源。若这些分支难以穷举且允许一定自主性，Agent 才开始产生价值。

---

## 3. 不使用它会发生什么

这里的答案不是“所有系统都会失败”。恰恰相反，很多应用不使用 Agent 会更简单、更稳定。

只有当任务确实需要动态多步决策时，单次 LLM 调用可能出现：

- 无法访问当前数据，只能猜测。
- 无法根据工具结果调整后续步骤。
- 把一个复杂目标压进一次回答，缺少中间校验点。
- 发生失败时，只知道最终结果错，不知道在哪一步错。

如果任务步骤固定，不使用 Agent 通常不会有问题，使用 Workflow 即可。

---

## 4. 核心原理

### 4.1 数据流

```text
User Question
     ↓
Messages / State ───────────────┐
     ↓                          │
Model Decision                  │
  ├─ Final Answer → Stop        │
  └─ Tool Call                  │
         ↓                      │
     Validate                   │
         ↓                      │
     Execute Tool               │
         ↓                      │
     Observation ───────────────┘
```

### 4.2 Runtime 与模型分离

建议把系统分成两个边界：

- Model Adapter：把供应商响应转换为统一的 `ToolCall` 或最终文本。
- Agent Runtime：维护循环、工具注册、异常、Trace 和停止条件。

这样更换模型时，不必重写工具和业务状态；测试 Runtime 时，也可以使用确定性的假模型复现轨迹。

### 4.3 Tool Registry

Tool Registry 至少保存：

```text
name → description + parameter schema + function
```

它负责工具查找和执行边界。生产系统还应加入每用户授权、路径白名单、超时、限流、幂等和审计。

### 4.4 Stop Condition

常见停止条件：

- 模型给出 Final Answer。
- 达到最大步数。
- 达到 Token、时间或费用预算。
- 检测到重复轨迹。
- 用户取消。
- 安全策略拒绝继续。

“模型自己会停”不是可靠的工程假设。

### 4.5 Trace

日志告诉你发生了错误；Trace 应该能还原一次任务轨迹：

```text
step 1: model → calculator({expression: "(23+19)*2"})
step 1: tool  → {ok: true, value: 84}
step 2: model → final("结果是 84")
```

后续评测需要从 Trace 统计工具选择、平均步数、失败原因、Token、成本和延迟。

---

## 5. 最小代码实现

本工程的最小实现位于：

```text
examples/00_simple_agent/main.py
```

先只读主循环：

```python
for step in range(1, max_steps + 1):
    turn = model.respond(context, tool_schemas)
    context.extend(turn.context_items)

    if not turn.tool_calls:
        return turn.final_answer

    for call in turn.tool_calls:
        observation = registry.execute(call)
        context.append(observation)
```

实际文件额外处理了 Trace、未知工具、错误结果和空答案。仍然刻意没有加入 Memory、Planning、并行、重试和框架抽象。

离线 `ScriptedModel` 不是 LLM。它只生成确定的工具调用，用来验证 Runtime 的控制流并让测试可重复。换成 `OpenAIModel` 后，Runtime 不变，工具选择才由真实模型完成。

---

## 6. 框架实现

本阶段不使用 LangGraph、Agents SDK、AutoGen 或 CrewAI 实现 Agent。框架通常会封装：

- 模型适配器和消息格式。
- Tool Schema 生成与调用。
- Agent Loop 和 Handoff。
- State、Checkpoint 与持久化。
- Trace、Streaming 和生命周期钩子。

只有在你能指出最小代码中的对应位置后，框架抽象才有意义。Stage 4 会把自制 Workflow 映射到 LangGraph，Stage 7 会把自制 Runtime 映射到一个官方 Agent SDK。

---

## 7. 实际场景与架构选择

### 场景 A：把一段文本改成三条摘要

优先：单次 LLM 调用。步骤少、无外部工具、无需动态决策。

### 场景 B：上传 PDF，提取文本，固定查询两个数据库，生成固定模板报告

优先：Workflow。步骤已知，应在节点之间加入确定性校验和重试。

### 场景 C：开放式研究，需要根据已有证据决定继续搜索、改写 Query 或停止

候选：Workflow + Agent 节点。外层固定提取、权限、存储和报告格式；Agent 只决定证据探索策略。

### 场景 D：软件开发任务，需要研究、修改代码、运行测试和 Review

先尝试：单 Agent + 显式 Workflow。只有在上下文隔离、并行专业能力或独立审查确有收益时，再考虑 Multi-Agent。

---

## 8. 常见错误

1. 把“用了 LLM”叫做 Agent。
2. 固定三步流程仍让模型每次决定下一步。
3. 让 Tool Schema 只描述参数类型，不描述使用条件和边界。
4. 把 Schema 校验当成权限校验。
5. 没有最大步数和取消机制。
6. 工具错误直接抛出并丢失上下文，模型没有机会修正。
7. 把所有历史一直追加，导致 Context 和费用持续增长。
8. 只记录最终答案，不记录调用轨迹。
9. 为了“角色分工”过早引入 Multi-Agent。
10. 用框架默认行为代替业务架构决策。

---

## 9. Debug 方法

遇到 Agent 错误时，不要先改 Prompt。按层排查：

```text
输入是否正确？
  ↓
模型是否看到了正确的工具 Schema？
  ↓
模型选择了哪个 Action，参数是什么？
  ↓
Registry 是否找到正确工具？
  ↓
工具执行是否成功，返回结构是什么？
  ↓
Observation 是否被正确加入 Context？
  ↓
停止条件为何触发或没有触发？
```

四个首周故障实验：

| 故障 | 观察点 | 预期处理 |
| --- | --- | --- |
| 除零 | Tool Trace | 返回结构化错误，不让 Runtime 崩溃 |
| 未知工具 | Registry | 返回 `unknown_tool` |
| 非法 JSON 参数 | 参数解析 | 返回 `invalid_arguments` |
| 模型一直调用工具 | Agent Loop | 达到 `max_steps` 后明确失败 |

---

## 10. 思考题

先写答案，再查看后续课程中的讨论。

1. 普通 LLM 应用为什么不一定需要 Agent？
2. 一个流程虽然有十步，但每步都固定，它需要 Agent 吗？
3. 为什么模型不能直接获得任意文件读取能力？
4. Tool 返回自然语言和返回 JSON，各有什么优缺点？
5. State 中应该保存什么，Context 中又应该放什么？
6. 模型连续三次调用同一个工具，是合理重试还是死循环？你需要什么证据判断？
7. Multi-Agent 在什么条件下会比单 Agent 更差？
8. MCP Server 能被调用，是否意味着你的 Agent 架构已经合理？

---

## 11. 实战任务

### 任务 1：读懂，不修改

运行离线 Demo，画出 `context` 在两次模型调用前后的内容变化。

### 任务 2：做一个小修改

为 Calculator 增加你自己的测试问题，并预测 Trace，再运行验证。

### 任务 3：制造故障

输入除零表达式，解释错误在哪一层被捕获。然后临时把 `max_steps` 改为 1，观察停止行为。

### 任务 4：新增只读工具

先自行设计一个参数很少、无副作用的工具。写出：

- 工具名。
- 什么时候使用。
- 参数 Schema。
- 返回结构。
- 可能错误。
- 为什么权限风险较低。

设计通过 Review 后再实现。

### 任务 5：架构判断

场景：用户上传一篇 PDF，需要提取内容、查询企业数据库、搜索互联网并生成报告。

先回答：

1. 哪些步骤是固定 Workflow？
2. 哪些步骤可能允许 Agent 自主决策？
3. State 保存什么？
4. Memory 保存什么？
5. 哪些节点需要重试或人工批准？
6. 如何停止循环并评测成功？

---

## 第一周验收标准

### 理论目标

- 能用自己的话解释 Agent Loop 的五个关键节点。
- 能区分 History、Context、State、Memory、RAG。

### 开发目标

- 不看实现，写出带 Tool Registry 和最大步数的循环伪代码。
- 能在现有 Runtime 中增加一个简单工具，而不是复制一套新 Agent。

### 项目目标

- Demo 可运行，能够显示模型调用、工具调用、Observation 和 Final Answer。

### Debug 目标

- 能解释除零、未知工具、非法参数和步数耗尽分别由哪一层处理。

### 架构目标

- 对三个新场景分别选择单次 LLM、Workflow 或 Agent，并给出可反驳、可验证的理由。

