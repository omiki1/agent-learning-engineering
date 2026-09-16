# 00 Simple Agent

这个 Demo 展示最小的 Agent Runtime：模型决定调用工具或给出最终回答，程序执行工具，把 Observation 回传给模型，然后继续循环。

它刻意不包含 Memory、Planning、RAG、并行工具、重试框架或 Agent 框架。

## 结构

```text
Question
   ↓
Model.respond()
   ├─ Final Answer → Stop
   └─ Tool Call
          ↓
      ToolRegistry.execute()
          ↓
      Observation
          └────────→ Model.respond()
```

`main.py` 中的关键边界：

- `Agent`：循环、最大步数和 Trace。
- `ToolRegistry`：工具发现和受控执行。
- `ScriptedModel`：可重复的离线模型替身，不是 LLM。
- `OpenAIModel`：可选真实模型适配器，Agent Runtime 无需改变。
- `safe_calculate`：使用 AST 白名单计算，不使用危险的 `eval()`。

## 离线运行

```powershell
python examples/00_simple_agent/main.py --offline
python examples/00_simple_agent/main.py --offline --question "请计算 (23 + 19) * 2"
```

离线模式只识别算术表达式。它的目标是让控制流和错误可以稳定复现，不用于证明模型具有推理能力。

## 可选真实模型运行

先安装当前 OpenAI Python SDK，并在当前终端设置 API Key：

```powershell
python -m pip install --upgrade openai
$env:OPENAI_API_KEY = "你的 API Key"
python examples/00_simple_agent/main.py --model gpt-5.6 --question "请计算 (23 + 19) * 2"
```

模型 ID 可以用 `--model` 显式传入，不在代码中假设“永远最新”的模型。该适配器使用 Responses API：保留模型输出项，再用匹配的 `call_id` 追加 `function_call_output`。实现依据 2026-08-27 查阅的官方文档：

- [OpenAI Function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)

真实模式可能产生 API 费用；Stage 0 验收不要求使用它。

## 观察 Trace

正常轨迹应接近：

```text
[step 1] model: tool_calls=calculator
[step 1] tool: calculator -> {"ok": true, "value": 84}
[step 2] model: final
```

注意模型的隐藏推理不会被打印。本 Demo 中的 `model` Trace 只记录可观察的输出类型、工具名和最终答案状态。

## 故障实验

```powershell
python examples/00_simple_agent/main.py --offline --question "请计算 10 / 0"
python examples/00_simple_agent/main.py --offline --question "请计算 2 ** 100"
```

回答以下问题：

1. 异常发生在模型、Registry 还是工具内部？
2. 为什么工具错误被转换成 Observation，而不是让进程退出？
3. 如果模型收到错误后继续重复同一调用，哪个停止条件兜底？

## 测试

```powershell
python -m unittest discover -s tests -v
```

