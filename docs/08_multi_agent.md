# 08｜Multi-Agent：只有边界真实存在时才拆分

## 1. 它是什么

多个 Agent 拥有独立职责、上下文或权限，通过 Supervisor、Handoff、消息或共享 Artifact 协作。

```text
Supervisor
 ├─ Researcher → evidence artifact
 ├─ Developer  → patch artifact
 └─ Reviewer   → findings
```

## 2. 为什么出现

当任务需要上下文隔离、独立权限、专业模型、并行工作或真正独立审查时，单 Agent 的 Prompt 和上下文会变得混杂。

## 3. 不使用会怎样

很多任务不会有问题。单 Agent + Tools + Workflow 通常更便宜、更快、更容易调试。只有角色边界带来可测收益时才拆。

## 4. 核心原理

### 4.1 模式

- Supervisor–Worker：中央分派，控制强。
- Planner–Executor：计划与执行分离，但计划可能过时。
- Reviewer/Critic：独立检查输出和证据。
- Handoff：控制权转交专家，适合对话路由。
- Debate：多观点竞争，成本高且可能同质化。

### 4.2 通信契约

Agent 之间传结构化 Artifact：任务 id、输入范围、输出 Schema、证据、置信度、未解决问题。不要反复转发完整对话。

### 4.3 终止与责任

Supervisor 有全局预算；每个 Worker 有局部预算。明确谁能结束、谁能重试、谁批准副作用。Reviewer 不应默认拥有修改/执行权限。

## 5. 最小实现

```python
task = supervisor.route(request)
artifact = workers[task.role].run(task)
review = reviewer.check(artifact)
return supervisor.decide(artifact, review)
```

这只是多组件。只有 Worker 自己包含动态模型循环，才称得上多个 Agent。

## 6. 框架实现

OpenAI Agents SDK 提供 manager-as-tools 与 Handoff；AutoGen 提供 AgentChat Team/GroupChat 和事件驱动 Core；CrewAI 提供 Crew/Process；LangGraph 可显式构建 Supervisor/Swarm。框架不能证明拆分合理。

## 7. 实际场景

代码安全审查需要独立只读 Reviewer；跨语言任务可给不同 Worker 不同工具链；客服 Handoff 可把对话转交不同权限域。

## 8. 常见错误

只换角色 Prompt、所有 Agent 共享完整上下文、无限互评、Supervisor 成为瓶颈、没有全局预算、Reviewer 与 Developer 使用相同证据和同一偏差、消息无 Schema。

## 9. Debug 方法

记录消息图、sender/receiver、Artifact 版本、每个 Agent Token/延迟、Handoff 原因、错误来源与传播。对照单 Agent 基线，逐个移除角色做消融实验。

## 10. 思考题

1. “Researcher”和“Writer”一定要是两个 Agent 吗？
2. 独立 Reviewer 如何避免只重复 Developer 的结论？
3. Supervisor 出错会怎样传播？

## 11. 实战任务与验收

实现 Supervisor–Researcher–Developer–Reviewer，并与单 Agent 完成同一组 20 个任务。验收：成功率、Token、延迟、通信量、错误传播；若多 Agent 无显著收益，应得出“不采用”的结论。

