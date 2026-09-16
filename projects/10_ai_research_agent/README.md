# Project 10｜AI Research Agent

离线毕业项目垂直切片：计划→课程文档检索→证据门禁→带引用报告，并输出完整 Trace。Web 层为可选 FastAPI + 静态页面。

```powershell
python projects/10_ai_research_agent/app.py "什么时候应该使用 Multi-Agent？"
python -m pip install fastapi uvicorn
uvicorn service:app --app-dir projects/10_ai_research_agent --reload
```

这不是完整互联网研究产品；它是把 Planning、Tool、RAG、State、Workflow、Trace、Evaluation 接成一条可运行垂直链的参考。

