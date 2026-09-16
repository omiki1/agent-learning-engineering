"""一个无 Agent 框架的最小、可观察 Agent Loop。"""

from __future__ import annotations

import argparse
import ast
import json
import operator
import re
import sys
from dataclasses import dataclass
from typing import Any, Callable, Protocol


JsonObject = dict[str, Any]


# Codex/现代终端按 UTF-8 读取输出；避免 Windows 默认代码页造成中文 Trace 乱码。
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class ToolCall:
    call_id: str
    name: str
    arguments: str


@dataclass
class ModelTurn:
    """模型一次可观察输出；不包含或伪造隐藏推理。"""

    context_items: list[Any]
    tool_calls: list[ToolCall]
    final_answer: str | None = None


class Model(Protocol):
    def respond(self, context: list[Any], tools: list[JsonObject]) -> ModelTurn:
        """选择工具调用或给出最终回答。"""


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: JsonObject
    handler: Callable[..., Any]

    def schema(self) -> JsonObject:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": True,
        }


class ToolRegistry:
    def __init__(self, tools: list[Tool]) -> None:
        self._tools = {tool.name: tool for tool in tools}

    @property
    def schemas(self) -> list[JsonObject]:
        return [tool.schema() for tool in self._tools.values()]

    def execute(self, call: ToolCall) -> str:
        """始终返回 JSON Observation，让模型有机会看到并修正错误。"""
        tool = self._tools.get(call.name)
        if tool is None:
            return _json_observation(
                ok=False,
                error="unknown_tool",
                message=f"工具不存在：{call.name}",
            )

        try:
            arguments = json.loads(call.arguments)
        except json.JSONDecodeError as exc:
            return _json_observation(
                ok=False,
                error="invalid_arguments",
                message=f"参数不是合法 JSON：{exc.msg}",
            )

        if not isinstance(arguments, dict):
            return _json_observation(
                ok=False,
                error="invalid_arguments",
                message="工具参数必须是 JSON object",
            )

        try:
            value = tool.handler(**arguments)
        except TypeError as exc:
            return _json_observation(
                ok=False,
                error="invalid_arguments",
                message=str(exc),
            )
        except Exception as exc:  # Demo 中把工具边界的异常转换为 Observation。
            return _json_observation(
                ok=False,
                error="tool_error",
                message=f"{type(exc).__name__}: {exc}",
            )

        return _json_observation(ok=True, value=value)


class Agent:
    def __init__(
        self,
        model: Model,
        registry: ToolRegistry,
        *,
        max_steps: int = 4,
        trace_sink: Callable[[str], None] = print,
    ) -> None:
        if max_steps < 1:
            raise ValueError("max_steps 必须大于等于 1")
        self.model = model
        self.registry = registry
        self.max_steps = max_steps
        self.trace_sink = trace_sink

    def run(self, question: str) -> str:
        context: list[Any] = [{"role": "user", "content": question}]

        for step in range(1, self.max_steps + 1):
            turn = self.model.respond(context, self.registry.schemas)
            context.extend(turn.context_items)

            if not turn.tool_calls:
                if not turn.final_answer:
                    raise RuntimeError("模型既没有调用工具，也没有给出最终回答")
                self._trace(step, "model", "final")
                return turn.final_answer

            tool_names = ", ".join(call.name for call in turn.tool_calls)
            self._trace(step, "model", f"tool_calls={tool_names}")

            for call in turn.tool_calls:
                observation = self.registry.execute(call)
                self._trace(step, "tool", f"{call.name} -> {observation}")
                context.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": observation,
                    }
                )

        raise RuntimeError(f"达到最大步数 {self.max_steps}，Agent 被强制停止")

    def _trace(self, step: int, phase: str, detail: str) -> None:
        self.trace_sink(f"[step {step}] {phase}: {detail}")


class ScriptedModel:
    """确定性的离线模型替身，只用于测试 Runtime，不是 LLM。"""

    def respond(self, context: list[Any], tools: list[JsonObject]) -> ModelTurn:
        del tools  # 离线脚本知道固定 Demo 工具；真实模型会读取 Schema。
        last_item = context[-1]

        if isinstance(last_item, dict) and last_item.get("type") == "function_call_output":
            observation = json.loads(last_item["output"])
            if observation.get("ok"):
                answer = f"计算结果是 {observation['value']}。"
            else:
                answer = (
                    "工具执行失败："
                    f"{observation.get('error')} - {observation.get('message')}"
                )
            return ModelTurn(context_items=[], tool_calls=[], final_answer=answer)

        question = _last_user_text(context)
        expression = _extract_expression(question)
        if expression is None:
            return ModelTurn(
                context_items=[],
                tool_calls=[],
                final_answer="离线模型只演示算术工具调用，请在问题中加入算术表达式。",
            )

        call = ToolCall(
            call_id="offline-calculator-1",
            name="calculator",
            arguments=json.dumps({"expression": expression}, ensure_ascii=False),
        )
        context_item = {
            "type": "function_call",
            "call_id": call.call_id,
            "name": call.name,
            "arguments": call.arguments,
        }
        return ModelTurn(context_items=[context_item], tool_calls=[call])


class OpenAIModel:
    """OpenAI Responses API 的薄适配层；需要可选的 openai 包和 API Key。"""

    def __init__(self, model: str) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "真实模型模式需要安装 openai：python -m pip install --upgrade openai"
            ) from exc

        self.client = OpenAI()
        self.model = model

    def respond(self, context: list[Any], tools: list[JsonObject]) -> ModelTurn:
        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "你是一个受控的计算助手。遇到算术问题必须调用 calculator；"
                "收到工具结果后，用简体中文简洁回答。"
            ),
            input=context,
            tools=tools,
        )

        calls = [
            ToolCall(
                call_id=item.call_id,
                name=item.name,
                arguments=item.arguments,
            )
            for item in response.output
            if item.type == "function_call"
        ]
        return ModelTurn(
            # 完整保留输出项；推理模型的关联上下文也必须随工具结果回传。
            context_items=list(response.output),
            tool_calls=calls,
            final_answer=response.output_text or None,
        )


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_calculate(expression: str) -> int | float:
    """只允许数字和有限算术操作，避免使用 eval。"""
    if len(expression) > 100:
        raise ValueError("表达式过长")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return _BINARY_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError(f"不支持的表达式节点：{type(node).__name__}")

    result = evaluate(tree)
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def build_registry() -> ToolRegistry:
    return ToolRegistry(
        [
            Tool(
                name="calculator",
                description="计算只含数字、括号、加减乘除、整除和取模的算术表达式。",
                parameters={
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "例如：(23 + 19) * 2",
                        }
                    },
                    "required": ["expression"],
                    "additionalProperties": False,
                },
                handler=safe_calculate,
            )
        ]
    )


def _json_observation(*, ok: bool, **payload: Any) -> str:
    return json.dumps({"ok": ok, **payload}, ensure_ascii=False)


def _last_user_text(context: list[Any]) -> str:
    for item in reversed(context):
        if isinstance(item, dict) and item.get("role") == "user":
            return str(item.get("content", ""))
    return ""


def _extract_expression(text: str) -> str | None:
    candidates = re.findall(r"[\d\s+\-*/().]+", text)
    candidates = [candidate.strip() for candidate in candidates if re.search(r"\d", candidate)]
    return max(candidates, key=len) if candidates else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--question",
        default="请计算 (23 + 19) * 2",
        help="交给 Agent 的问题",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="显式使用确定性的离线模型（未传 --model 时也默认离线）",
    )
    parser.add_argument(
        "--model",
        help="使用真实 OpenAI 模型，例如 gpt-5.6；需要 SDK 和 OPENAI_API_KEY",
    )
    parser.add_argument("--max-steps", type=int, default=4)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.offline and args.model:
        raise SystemExit("--offline 与 --model 不能同时使用")

    model: Model = OpenAIModel(args.model) if args.model else ScriptedModel()
    agent = Agent(model, build_registry(), max_steps=args.max_steps)

    try:
        answer = agent.run(args.question)
    except Exception as exc:
        print(f"Agent 失败：{type(exc).__name__}: {exc}")
        return 1

    print(f"最终回答：{answer}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
