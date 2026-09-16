# Project 09｜Agent Evaluation

包含 30 条离线评测样本，覆盖计算、天气、搜索、文件、普通对话和危险动作拒绝。评测器统计任务成功率、工具准确率、平均步数、近似 Token/成本、延迟和失败原因。

```powershell
python projects/09_agent_eval/evaluate.py
```

当前 Candidate 是确定性基线。把它替换为任意 Agent，但保持 `RunResult` 和数据集不变，即可做回归比较。

