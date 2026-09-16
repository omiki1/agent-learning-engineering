# 09｜Agent 工程化：把不确定内核放进可靠系统

## 1. 它是什么

```text
Web UI
  ↓ HTTP/SSE/WebSocket
FastAPI / Gateway
  ↓
Agent Service
  ↓
Runtime ─ Tool Registry ─ Memory/RAG/MCP
  ↓             ↓
Queue        Database/Object Store
```

## 2. 为什么出现

Agent 延迟长、外部依赖多、会循环、产生副作用。生产系统需要并发、取消、恢复、权限、限流、观测和成本治理。

## 3. 不使用会怎样

请求占满 Web Worker、客户端断开后任务继续烧钱、重试造成重复动作、状态留在进程内、日志泄露敏感信息、故障无法重放。

## 4. 核心原理

### API 与任务

- 短任务：同步或 SSE。
- 长任务：提交 task，返回 id，队列执行，查询/订阅状态。
- 每个请求有 request_id、user_id、thread_id、trace_id。

### Async

Async 适合 I/O 并发，不会让 CPU 工作自动变快。同步 SDK 要放线程池或更换 async client。设置连接、读取和总超时。

### Streaming

区分 token、tool status、artifact、final、error、heartbeat。不要把内部隐藏推理流给用户。断开连接要传播取消或转为后台任务。

### Reliability

幂等键、指数退避、熔断、限流、dead-letter、checkpoint、状态机版本。副作用采用 outbox/事务或明确补偿。

### Security

认证后仍要逐工具授权；最小权限、沙箱、路径白名单、SQL 参数化、Prompt Injection 隔离、Secret 脱敏、审计和人工批准。

## 5. 最小实现

```python
@app.post("/runs")
async def create_run(req: RunRequest, user=Depends(auth)):
    run_id = await queue.submit(user.id, req, idempotency_key=req.key)
    return {"run_id": run_id, "status": "queued"}
```

`projects/08_agent_service` 提供 FastAPI 可选示例，核心逻辑可以脱离 Web 层测试。

## 6. 框架实现

FastAPI 负责传输和依赖注入；队列负责持久任务；数据库存 State/Trace；对象存储存大型 Artifact；LangGraph/Temporal 等负责 durable workflow；OpenTelemetry/平台 Trace 负责观测。不要让一个框架承担所有边界。

## 7. 实际场景

研究报告：后台任务 + SSE 进度 + Artifact 下载；客服动作：同步查询 + HITL 写操作；代码 Agent：隔离 worktree/sandbox + 测试 + 审批。

## 8. 常见错误

全局内存保存会话、无取消、在日志打印 Prompt/Token、对 429 立即并发重试、把 SSE 当消息队列、数据库事务跨越模型调用、无租户隔离。

## 9. Debug 方法

沿 trace_id 查询 API→queue→runtime→tool→DB；仪表盘监控 p50/p95/p99、错误率、运行中任务、平均步数、Token/成本、工具失败率和取消率。故障注入网络超时、进程重启、客户端断开和重复提交。

## 10. 思考题

1. Agent State 为什么不能只放 Redis TTL？
2. 客户端断开后任务应取消还是继续？
3. 工具调用超时后如何判断是否已经产生副作用？

## 11. 实战任务与验收

构建 FastAPI + Agent Service 最小垂直切片，支持提交、流式事件、取消、状态查询和 Trace。验收：并发、断开、重启、限流和幂等测试；密钥/隐私不进入日志；写操作有授权与审批。

