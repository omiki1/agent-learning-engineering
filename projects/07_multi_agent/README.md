# Project 07｜Multi-Agent 对照实验

离线 Harness 同时运行“单组件基线”和“Supervisor→Researcher/Developer→Reviewer”方案，统计近似通信字符数和步骤数。这里的确定性组件用于测试编排；换成真实 Agent 后接口和指标保持不变。

```powershell
python projects/07_multi_agent/main.py
```

扩展：接真实模型，在同一 20 题数据集上记录成功率、Token、延迟和错误传播。只有质量收益超过额外成本才采用 Multi-Agent。

