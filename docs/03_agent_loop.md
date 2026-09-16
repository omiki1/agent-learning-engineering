# 03｜Agent Loop 与 ReAct：让循环可控、可停、可解释

## 1. 它是什么

ReAct 把推理与行动交替组织。工程上不需要暴露模型隐藏思维，只需记录可观察轨迹：模型输出的 Action、工具 Observation、状态更新和最终答案。

```text
Question → Model → Action → Tool → Observation ┐
                    ↑                           │
                    └───────────────────────────┘
                              ↓
                         Final Answer
```

## 2. 为什么出现

复杂任务的下一步取决于刚取得的数据。Loop 允许模型根据 Observation 修正参数、换工具或结束。

## 3. 不使用会怎样

单次调用只能预先猜测工具结果；把所有可能步骤硬塞进一个 Prompt，失败点不可见。但固定流程不需要 Agent Loop，应使用 Workflow。

## 4. 核心原理

### 4.1 状态机视角

```text
THINKING → TOOL_REQUESTED → TOOL_RUNNING → OBSERVED → THINKING
THINKING → FINISHED
ANY → FAILED / CANCELLED / BUDGET_EXCEEDED
```

### 4.2 停止条件

- 最终回答。
- `max_steps`。
- 时间/Token/费用预算。
- 重复 `(tool, normalized_args)`。
- 用户取消或审批拒绝。
- 不可恢复错误。

### 4.3 错误恢复

参数错误可以作为 Observation 让模型修正；依赖暂态失败由程序有限重试；权限拒绝不能通过反复改 Prompt 绕过；未知系统错误应停止并保存 Trace。

### 4.4 上下文增长

每一步都追加模型输出和工具结果。控制策略：工具结果结构化和截断、重复内容去重、历史摘要、外部保存大型 Artifact、只回传句柄和必要片段。

## 5. 最小代码实现

```python
seen = set()
for step in range(max_steps):
    turn = model(context, tools)
    if turn.final:
        return turn.answer
    for call in turn.calls:
        fingerprint = (call.name, normalize(call.arguments))
        if fingerprint in seen:
            raise RepeatedAction(fingerprint)
        seen.add(fingerprint)
        result = execute(call)
        context.append(as_observation(call.id, result))
raise StepLimitExceeded()
```

## 6. 框架实现

- LangChain `create_agent`：预制模型节点和工具节点循环，运行在 LangGraph 上。
- LangGraph：把模型、工具、验证、审批显式建成 Node/Edge。
- OpenAI Agents SDK：`Runner` 管理多轮、工具、Handoff、Guardrail 和 Trace。

框架的 iteration limit 仍需结合业务预算；默认值不是架构设计。

## 7. 实际场景

- SQL 修复循环：生成查询→只读执行→根据错误修复→最多 2 次。
- 研究：搜索→读来源→证据门禁→必要时补查。
- 客服：查订单→按政策节点决定可否退款→高风险操作人工批准。

## 8. 常见错误

无限重试、模型自称完成就结束、Action 指纹未归一化、多个工具结果顺序错、把每次完整网页塞进上下文、把隐藏推理当唯一 Debug 依据。

## 9. Debug 方法

把一次运行保存为 Trajectory：输入、每步可观察输出、工具结果、状态差异、预算和停止原因。先判断错误属于选择、参数、工具、Observation 注入、状态更新还是终止。

## 10. 思考题

1. 同一搜索工具换了 query，算重复调用吗？
2. 工具失败后应由 Runtime 重试还是让模型决定？
3. 最终答案正确但用了危险工具，任务算成功吗？

## 11. 实战任务与验收

实现 Mini ReAct Agent，并注入四种故障：重复工具、非法参数、工具超时、上下文过大。验收：每种故障有明确停止原因；能够重放轨迹；同题多次运行的成功率和平均步数可统计。

