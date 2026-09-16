# Project 02｜ReAct Agent

需求：为“Agent Memory 与普通 History 的区别”生成一份基于课程文档的回答。Agent 必须先搜索，再读取最相关文档，最后回答；检测重复 Action 并限制步数。

```powershell
python projects/02_react_agent/main.py
python projects/02_react_agent/main.py --max-steps 1
```

扩展：注入一次 `read` 失败，让模型换下一个结果；记录停止原因和平均步数。

