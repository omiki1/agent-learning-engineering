# 01｜LLM 应用基础：消息、上下文与结构化输出

## 1. 它是什么

LLM 应用不是“字符串进去、字符串出来”这么简单。真正的输入由消息（Message）、指令、上下文、工具定义和输出约束共同组成。

```text
System / Developer Instructions
User Message
Conversation Context
Retrieved Evidence
Tool Schemas
Output Schema
        ↓
      Model
        ↓
Text / Structured Data / Tool Calls
```

常见角色：

- system/developer：应用规则和边界。
- user：用户输入。
- assistant：模型可见输出。
- tool：工具执行结果。

温度（Temperature）控制采样随机性，但低温不等于事实正确。Token 是模型处理文本的计量单位；上下文窗口容纳输入与输出，不是无限数据库。

## 2. 为什么出现

自然语言灵活但难以被程序可靠消费。结构化输出（Structured Output）和 JSON Schema 让模型结果可以进入后续程序；Message 角色让不同来源的内容保留语义边界；Context 管理避免把不相关信息全部交给模型。

## 3. 不使用会怎样

- 用字符串拼接所有内容，容易发生角色混淆和 Prompt Injection。
- 只要求“输出 JSON”，仍可能缺字段、错类型或带额外说明。
- 上下文无限增长，导致成本、延迟和注意力退化。
- 把低 Temperature 当成确定性保证，回归测试会偶发失败。

## 4. 核心原理

### 4.1 Prompt 分层

```text
稳定规则：权限、身份、输出原则
任务指令：本次具体目标
业务数据：用户输入、检索证据、工具结果
输出契约：Schema、长度、语言
```

数据必须被当作数据，而不是可信指令。即使 System Prompt 说“不要泄露”，真正的秘密也不应进入模型上下文。

### 4.2 Structured Output

示例任务结构：

```json
{
  "intent": "weather_query",
  "needs_tool": true,
  "arguments": {"city": "Tokyo"}
}
```

Schema 校验分三层：

1. 语法：是不是合法 JSON。
2. 结构：字段、类型、枚举、额外属性是否合法。
3. 业务：城市是否支持、用户是否有权限、时间范围是否合理。

### 4.3 Context Budget

把 Context 看成有限预算：

```text
固定指令 + 当前问题 + 必要历史 + 检索证据 + 工具结果 + 输出空间
```

常用控制：裁剪、摘要、按需检索、去重、保留原始事实而非重复格式化文本。

## 5. 最小代码实现

不依赖模型也可以先练习结构验证：

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class Decision:
    intent: Literal["calculate", "chat"]
    needs_tool: bool
    expression: str | None

def validate(data: dict) -> Decision:
    allowed = {"intent", "needs_tool", "expression"}
    if set(data) - allowed:
        raise ValueError("存在额外字段")
    if data.get("intent") not in {"calculate", "chat"}:
        raise ValueError("未知 intent")
    return Decision(**data)
```

这个例子只验证结构。`expression` 是否安全，仍由 Calculator 工具验证。

## 6. 框架/SDK 实现

主流 SDK 通常提供：

- Pydantic/JSON Schema 生成。
- 结构化输出解析。
- Function Tool Schema。
- 流式事件和 Token Usage。

先检查 SDK 返回的是“解析后的对象”还是“模型生成的 JSON 文本”。不要把 `json.loads()` 成功误认为业务有效。

## 7. 实际场景

- 信息抽取：用 Schema，不需要 Agent。
- 意图分类：单次结构化输出或传统分类器。
- 报告生成：正文可以是文本，引用和元数据应结构化。
- Tool Calling：模型输出工具名和参数，应用验证后执行。

## 8. 常见错误

1. 一个 Prompt 同时承担身份、业务数据、输出格式和错误恢复，难以调试。
2. Schema 允许任意额外字段。
3. 把用户文本直接拼到 System Prompt。
4. 记录完整 Prompt 时把密钥和隐私写进日志。
5. 模型拒答或截断时仍强行解析 JSON。

## 9. Debug 方法

按顺序保存：模型输入摘要、Schema 版本、原始输出、解析错误、业务校验错误、Token 和延迟。把失败分类为：指令理解、格式、Schema、业务、截断、服务错误。

## 10. 思考题

1. Context 与 Conversation History 为什么不是同一个集合？
2. 哪些字段适合枚举，哪些字段不适合？
3. 如果模型输出结构合法但业务错误，应修改 Prompt、Schema 还是业务校验？

## 11. 实战任务与验收

实现“工单分类器”：输出 `category`、`priority`、`needs_human`、`reason`。准备 20 条输入，统计解析成功率和分类准确率。验收要求：非法值不能进入业务层；失败原因可定位；能解释为何本任务不需要 Agent。

