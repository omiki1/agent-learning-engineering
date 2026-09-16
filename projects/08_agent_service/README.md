# Project 08｜Agent Service

`core.py` 是可脱离 Web 测试的运行服务，产生 `started/tool/final` 事件。`app.py` 是可选 FastAPI/SSE 适配层。

```powershell
python projects/08_agent_service/core.py
python -m pip install fastapi uvicorn
uvicorn app:app --app-dir projects/08_agent_service --reload
```

接口：`POST /runs` 创建任务，`GET /runs/{id}` 查询，`GET /runs/{id}/events` 获取 SSE。

注意：内存 Store 只用于 Demo。生产版必须持久化、认证、逐工具授权、限流、取消传播和 Secret 脱敏。

