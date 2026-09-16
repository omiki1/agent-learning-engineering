# 04｜State、Checkpoint 与 Memory

## 1. 它是什么

```text
History：发生过的原始消息
Context：本次模型实际看到的输入
State：任务运行的显式数据
Checkpoint：可恢复的 State 快照
Memory：未来可选择性取回的信息
```

短期记忆通常按会话/线程隔离；长期记忆跨会话保存。语义记忆保存事实，情节记忆保存经历，程序性记忆保存规则或做法，工作记忆保存当前任务临时信息。

## 2. 为什么出现

长任务需要恢复；助手需要记住用户偏好；模型上下文有限且昂贵。Memory 的目标不是保存一切，而是在正确时机保存值得记的信息，并在需要时取回。

## 3. 不使用会怎样

每轮都像第一次；任务中断后无法恢复。但无策略地保存所有内容会造成隐私风险、错误记忆、上下文污染和成本上升。

## 4. 核心原理

### 4.1 State Schema

```python
class ResearchState(TypedDict):
    question: str
    plan: list[str]
    current_step: int
    evidence_ids: list[str]
    retries: dict[str, int]
    status: str
```

保存原始数据和引用，不要保存只能供一个节点读取的重复格式化 Prompt。

### 4.2 Memory 生命周期

```text
Candidate → Validate → Deduplicate/Conflict Check → Persist
→ Retrieve → Rank → Inject → Update/Delete
```

写入门槛：是否跨会话有价值、是否获得授权、是否为可验证事实、是否过期。读取需要用户/租户隔离和 top-k 限制。

### 4.3 三种实现

| 方案 | 优点 | 缺点 | 适合 |
| --- | --- | --- | --- |
| 内存变量 | 简单、快 | 进程退出丢失 | 单元测试、Demo |
| SQLite/关系库 | 精确、可更新、可删除 | 语义召回弱 | 偏好、事实、任务状态 |
| 向量库 | 模糊语义召回 | 冲突、删除、可解释性更难 | 大量文本经验/知识 |

向量库不是 Memory 的同义词。结构化偏好通常先用关系库。

### 4.4 Checkpoint

Checkpoint 必须包含恢复所需状态和版本。外部副作用不能简单重放；节点要有幂等键，恢复时要知道动作是否已经提交。

## 5. 最小代码实现

```python
CREATE TABLE preference (
  user_id TEXT NOT NULL,
  key TEXT NOT NULL,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY(user_id, key)
)
```

读取偏好时必须带 `user_id`；更新用 upsert；提供删除和导出。`projects/03_memory_agent` 给出可运行 SQLite 版本。

## 6. 框架实现

LangGraph 当前把 thread-scoped State 通过 checkpointer 保存，把跨 thread 长期数据放到 Store。Checkpoint 支持恢复、HITL 和 time-travel 调试。即使框架提供 Memory，写入策略和隐私边界仍是业务责任。

## 7. 实际场景

- 用户偏好：结构化长期记忆，可修改/删除。
- 未完成研究任务：Checkpoint。
- 历史案例检索：向量/混合检索的情节记忆。
- 当前检索证据：State，不必成为长期记忆。

## 8. 常见错误

把 History 当 Memory、跨用户串数据、自动记住敏感信息、没有 TTL、错误事实覆盖正确事实、把向量相似度当真实性、恢复后重复付款/发信。

## 9. Debug 方法

Trace 写入候选、批准/拒绝原因、namespace、版本、检索 query、top-k、命中分数和最终注入片段。设计“忘记我”的删除测试和跨用户隔离测试。

## 10. 思考题

1. “用户今天心情不好”应该长期保存吗？
2. 同一偏好出现冲突如何处理？
3. Checkpoint 恢复时外部 API 已成功但响应丢失怎么办？

## 11. 实战任务与验收

分别实现内存、SQLite、向量召回三版偏好助手。比较准确率、延迟、可删除性、冲突处理和隐私风险。验收：跨用户不串数据；重启可恢复；用户能查看、修改和删除记忆。

