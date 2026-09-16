# 01 Tool Calling

目标：把“模型/路由器选择动作”和“程序执行动作”分开。这个离线例子使用命令前缀模拟结构化 Tool Call，集中练习 Tool Schema、Registry、参数和错误。

```powershell
python examples/01_tool_calling/main.py "calc: (8 + 4) / 2"
python examples/01_tool_calling/main.py "weather: Tokyo"
python examples/01_tool_calling/main.py "search: Agent Loop"
python examples/01_tool_calling/main.py "file: 00_agent_overview.md"
```

修改顺序：先新增一个纯函数，再注册 Schema，最后为成功/错误各写一个测试。不要为新增工具修改 `execute()`。

