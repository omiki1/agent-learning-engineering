# 02｜Tool Calling：模型提议，程序执行

## 1. 它是什么

工具调用（Tool Calling）允许模型返回工具名与结构化参数，由应用程序执行，再把结果作为 Observation 回传。

```text
Model → {name: "weather", arguments: {city: "Tokyo"}}
Application → validate → authorize → execute
Tool → {ok: true, temperature: 31}
Application → Tool Result → Model
```

## 2. 为什么出现

模型不能可靠知道实时天气、账户余额或本地文件，也不应直接获得数据库和操作系统权限。工具把外部能力封装为可验证、可审计的最小接口。

## 3. 不使用会怎样

- 模型猜测实时或私有数据。
- 应用从自由文本中用正则解析动作，脆弱且危险。
- 权限、超时和错误无法集中处理。

## 4. 核心原理

### 4.1 好的 Tool Schema

```json
{
  "name": "read_note",
  "description": "读取课程 notes 目录中的 UTF-8 文本文件；仅在用户明确要求查看笔记时使用",
  "parameters": {
    "type": "object",
    "properties": {"relative_path": {"type": "string"}},
    "required": ["relative_path"],
    "additionalProperties": false
  }
}
```

描述必须说明：何时用、何时不用、参数语义、限制和返回值。参数越接近业务意图越好，例如 `customer_id` 优于任意 SQL。

### 4.2 执行链

```text
Parse → Schema Validate → Authorization → Normalize
→ Timeout/Retry Policy → Execute → Normalize Result → Trace
```

### 4.3 错误分层

- `unknown_tool`：模型选择不存在的工具。
- `invalid_arguments`：JSON 或 Schema 错。
- `permission_denied`：调用者无权限。
- `tool_error`：业务或依赖失败。
- `timeout` / `rate_limited`：暂态失败，可按策略重试。

错误结果应可被模型读取，但系统异常、密钥和内部堆栈不要原样暴露。

### 4.4 重试与幂等

读取工具可以有限重试；付款、发信、删除等有副作用的工具必须有幂等键和人工确认，不能因为网络超时就盲目重放。

## 5. 最小代码实现

本工程 `examples/00_simple_agent/main.py` 已实现 Registry。核心接口：

```python
tool = registry.get(call.name)
args = json.loads(call.arguments)
authorize(user, tool, args)
result = tool.handler(**args)
return json.dumps({"ok": True, "value": result})
```

V1 一个 `if name == ...`；V2 多个工具；V3 Registry；V4 校验和错误；V5 Agent Loop；V6 Trace、超时与权限。

## 6. 框架/SDK 实现

OpenAI Responses API 中，模型返回 `function_call`，应用以相同 `call_id` 追加 `function_call_output`。完整输出项要保留给后续轮次。LangChain、Agents SDK 和 MCP SDK 可以自动从函数签名/Pydantic 生成 Schema，但业务授权仍由应用负责。

## 7. 实际场景

| Tool | 推荐接口 | 不推荐接口 |
| --- | --- | --- |
| 计算 | `calculate(expression)` + AST 白名单 | `eval(code)` |
| 文件 | `read_note(relative_path)` + 根目录限制 | `read_file(absolute_path)` |
| 数据库 | `get_order(order_id)` | `execute_sql(sql)` |
| 邮件 | `draft_email(...)` 后人工批准 | `send_raw_email(anything)` |

## 8. 常见错误

工具太多、名称相似、描述含糊、返回巨大、没有超时、把异常堆栈回传、读写工具权限相同、把 Prompt 当授权。

## 9. Debug 方法

Trace 至少记录 `tool_name`、参数摘要、授权决定、开始/结束时间、结果状态、重试次数和关联 `call_id`。敏感字段必须脱敏。

## 10. 思考题

1. “搜索”和“读取搜索结果”应是一个工具还是两个？
2. 文件读取工具如何阻止 `../` 路径逃逸？
3. 为什么超时不意味着操作没有成功？

## 11. 实战任务与验收

完成 Calculator、Weather/API、Local Search、File Reader 四工具 Agent。验收：新增工具不改主循环；四类错误可复现；读文件限制在允许目录；对副作用工具给出审批和幂等设计。

