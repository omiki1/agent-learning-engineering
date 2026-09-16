# Project 01｜Tool Agent

需求：根据用户问题选择 Calculator、Weather、Local Search 或 File Reader，执行后给出结果。先回答：哪些工具需要网络？文件根目录是什么？每个工具的错误如何返回？

参考实现使用离线 Router，重点是 Registry 和安全边界。扩展任务：把 `RouterModel` 换成真实 Tool Calling 模型，Registry 不变。

```powershell
python projects/01_tool_agent/main.py "请计算 (9 + 3) * 2"
python projects/01_tool_agent/main.py "Tokyo 天气"
python projects/01_tool_agent/main.py "搜索 Memory"
```

验收：新增工具不改 `run()`；未知工具和参数错误可观察；文件读取不能逃逸 `docs/`。

