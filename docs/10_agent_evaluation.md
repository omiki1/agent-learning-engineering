# 10｜Agent Evaluation：答案、轨迹与成本一起评

## 1. 它是什么

Agent Evaluation 评估任务结果和执行过程：

```text
Task Success Rate
Tool Selection Accuracy
Argument Accuracy
Trajectory Quality
Average Steps / Tokens / Cost / Latency
Safety / Policy Compliance
Failure Reason Distribution
```

## 2. 为什么出现

Agent 可能答案碰巧正确但走了危险路径，也可能工具和检索正确却在最后生成失败。只看几个 Demo 无法判断回归和长尾风险。

## 3. 不使用会怎样

Prompt 修改靠感觉；框架升级后悄悄退化；成本与延迟持续上升；错误无法归因到模型、工具、检索或流程。

## 4. 核心原理

### 4.1 Dataset

每条至少包含：输入、期望结果/约束、允许或禁止工具、最大步数、标签和评分方法。覆盖正常、边界、工具错误、权限、对抗和应拒答样本。

### 4.2 Grader

- Deterministic：精确值、Schema、工具名、引用 id、禁止动作。
- LLM-as-Judge：语义质量、完整性、写作；必须有 rubric、校准集和人工抽检。
- Human：高风险、安全、主观质量的最终标尺。

### 4.3 Trajectory

评估是否选对工具、参数是否正确、是否重复、是否遵守预算、是否绕过审批、Observation 是否被正确使用。

### 4.4 统计

分层报告平均值和分位数；按类别切片。比较基线时记录模型、Prompt、Schema、工具版本、随机性和日期。

## 5. 最小代码实现

```python
for case in dataset:
    run = agent.run(case["input"])
    metrics.append({
        "success": check_answer(run, case),
        "tool_ok": check_tools(run.trace, case),
        "steps": len(run.trace),
        "latency_ms": run.latency_ms,
    })
```

`projects/09_agent_eval` 含 30 条 JSONL 数据和离线评测器。

## 6. 框架实现

可以使用平台 Evals、LangSmith 或自定义 runner。框架方便存 Trace 和聚合，但任务定义、rubric、数据泄漏和 Judge 偏差仍需自己管理。

## 7. 实际场景

Tool Agent：工具/参数准确率；RAG：Recall@k、引用正确率；客服动作：政策与审批合规；Multi-Agent：成功率提升是否抵消 Token/延迟。

## 8. 常见错误

测试集来自 Prompt 示例、只测简单成功、Judge 与被测模型相同且无校准、平均数掩盖长尾、只评最终文本、价格变动却硬编码成本、每次运行环境不同。

## 9. Debug 方法

失败先按 taxonomy 分类：intent、planning、tool_selection、arguments、tool_runtime、retrieval、state、loop、generation、policy。选代表轨迹做人工 Review，再决定改 Prompt、工具、数据、路由或模型。

## 10. 思考题

1. 两个答案都正确，步骤更少的一定更好吗？
2. LLM Judge 如何防止偏爱更长回答？
3. 线上成功率与离线集冲突时先相信谁？

## 11. 实战任务与验收

设计至少 30 个问题，自动统计成功率、工具选择、步数、Token、成本、延迟与失败原因；设定回归阈值。验收：固定基线、可重复运行、按类别切片、Judge 经人工校准、危险轨迹即使答案正确也判失败。

