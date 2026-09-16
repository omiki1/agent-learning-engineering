# Project 04｜Research Workflow

纯 Python 状态机：Analyze→Plan→Search→Read→Verify→Answer。Evidence Gate 不通过时有限回到 Search；每个节点打印 State diff。

```powershell
python projects/04_research_workflow/main.py "什么时候应该用 Agent？"
```

扩展：把 State 持久化为 JSON checkpoint；再将同一 Node/Edge 映射到 LangGraph，并比较代码与 Trace。

