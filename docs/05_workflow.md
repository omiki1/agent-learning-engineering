# 05｜Workflow、状态机与 LangGraph

## 1. 它是什么

Workflow 把步骤、状态和转移条件显式定义。常见模式：Sequential、Router、Conditional Branch、Parallel、Retry、Loop、Human Approval、DAG、Event-driven。

```text
Question → Analyze → Plan → Search ─┐
                          Read      │ parallel
                          Search ───┘
                              ↓
                         Verify
                    ┌─ insufficient → Search
                    └─ sufficient   → Answer
```

## 2. 为什么出现

大多数业务既包含确定性约束，又包含少量模糊决策。Workflow 让确定步骤可测试、可恢复，只把真正需要语义判断的节点交给 LLM。

## 3. 不使用会怎样

把整个流程交给 Agent 会降低可预测性；把所有分支写成嵌套 `if` 又难以观察、恢复和并行。状态机/Graph 提供显式控制结构。

## 4. 核心原理

### 4.1 Node 与 Edge

Node 做一件事并返回 State 更新；Edge 只决定下一节点。Node 尽量小到可以独立重试，又不要小到每行代码一个节点。

### 4.2 Router

确定性条件优先代码路由；意图模糊才用 LLM Router。LLM Router 的输出必须是受限枚举，并提供 fallback。

### 4.3 Parallel

并行节点不能无约束写同一 State 字段。需要 reducer、版本或合并规则。并行只改善独立 I/O 的延迟，不会自动改善质量。

### 4.4 Retry

- 暂态网络错误：指数退避 + 抖动。
- 参数可修复：回到模型并提供错误。
- 权限/业务拒绝：不重试。
- 副作用：先检查幂等状态。

### 4.5 Human-in-the-loop

审批前持久化 State；审批动作可 approve/edit/reject；恢复必须绑定同一 thread/task 和版本，防止批准过期动作。

## 5. 最小代码实现

```python
nodes = {"analyze": analyze, "search": search, "answer": answer}
current = "analyze"
while current != "END":
    update = nodes[current](state)
    state.update(update)
    current = route(current, state)
```

`projects/04_research_workflow` 在此基础上加入 Trace、重试计数和证据门禁。

## 6. LangGraph 实现

当前 LangGraph 定位是低层、长运行、有状态的 Agent 编排 Runtime，核心能力包括 durable execution、streaming、HITL 和 persistence。

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)
graph.add_node("analyze", analyze)
graph.add_node("search", search)
graph.add_edge(START, "analyze")
graph.add_conditional_edges("analyze", route)
app = graph.compile(checkpointer=checkpointer)
```

进入实际项目时重新核验当前 API。State 要可序列化；非确定性工作封装在可检查的节点/任务里。

## 7. 实际场景

- PDF 调研报告：固定解析和校验 + Agentic 搜索节点。
- 退款：政策 Workflow + 模糊分类 + 人工批准。
- 代码修复：分析→修改→测试→最多 N 次修复→Review。

## 8. 常见错误

State 保存不可序列化对象、多个并行节点互相覆盖、Router 无 fallback、所有异常一律重试、HITL 没有持久化、Node 里隐藏复杂循环、图很漂亮但没有业务不变量。

## 9. Debug 方法

记录每个 Node 的输入摘要、State diff、耗时、重试、下一 Edge 和 checkpoint id。支持从某个 checkpoint 重放，并比较两次 State diff。

## 10. 思考题

1. 搜索来源选择应写成 Edge 还是 Agent Tool Choice？
2. Node 应该在何处提交数据库事务？
3. 并行搜索一个失败，其他结果要不要保留？

## 11. 实战任务与验收

实现 Analyze→Plan→Search→Read→Summarize→Verify→Answer。验收：完整轨迹；证据不足会有限循环；每类异常有路由；可暂停审批并恢复；能够解释哪些节点根本不需要 LLM。

