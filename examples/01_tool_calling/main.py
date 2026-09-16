"""四工具 Registry：离线演示 Tool Calling 的程序边界。"""

from __future__ import annotations

import ast
import json
import operator
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: Callable[..., Any]


class Registry:
    def __init__(self, tools: list[Tool]) -> None:
        self.tools = {tool.name: tool for tool in tools}

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tool = self.tools.get(name)
        if not tool:
            return {"ok": False, "error": "unknown_tool", "name": name}
        try:
            return {"ok": True, "value": tool.handler(**arguments)}
        except TypeError as exc:
            return {"ok": False, "error": "invalid_arguments", "message": str(exc)}
        except Exception as exc:
            return {"ok": False, "error": "tool_error", "message": str(exc)}


OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def calculate(expression: str) -> int | float:
    tree = ast.parse(expression, mode="eval")

    def walk(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError("只支持数字和加减乘除")

    return walk(tree)


def weather(city: str) -> dict[str, Any]:
    sample = {"tokyo": 31, "beijing": 28, "shanghai": 30}
    value = sample.get(city.strip().lower())
    if value is None:
        raise ValueError("离线样例只包含 Tokyo、Beijing、Shanghai")
    return {"city": city.strip(), "temperature_c": value, "source": "offline_sample"}


def local_search(query: str, limit: int = 3) -> list[dict[str, Any]]:
    terms = [term.lower() for term in query.split() if term]
    results = []
    for path in DOCS.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        score = sum(text.lower().count(term) for term in terms)
        if score:
            results.append({"file": path.name, "score": score})
    return sorted(results, key=lambda item: item["score"], reverse=True)[:limit]


def read_doc(relative_path: str) -> str:
    target = (DOCS / relative_path).resolve()
    if DOCS.resolve() not in target.parents:
        raise PermissionError("只允许读取 docs 目录")
    if target.suffix.lower() != ".md":
        raise PermissionError("只允许 Markdown")
    return target.read_text(encoding="utf-8")[:1000]


def build_registry() -> Registry:
    return Registry([
        Tool("calculator", "安全计算加减乘除", calculate),
        Tool("weather", "查询离线样例天气", weather),
        Tool("local_search", "搜索课程文档", local_search),
        Tool("file_reader", "读取 docs 下 Markdown", read_doc),
    ])


def route(text: str) -> tuple[str, dict[str, Any]]:
    prefix, separator, value = text.partition(":")
    if not separator:
        return "missing", {}
    mapping = {
        "calc": ("calculator", {"expression": value.strip()}),
        "weather": ("weather", {"city": value.strip()}),
        "search": ("local_search", {"query": value.strip()}),
        "file": ("file_reader", {"relative_path": value.strip()}),
    }
    return mapping.get(prefix.strip().lower(), ("missing", {}))


def main() -> int:
    request = " ".join(sys.argv[1:]) or "calc: (8 + 4) / 2"
    name, arguments = route(request)
    call = {"name": name, "arguments": arguments}
    print("Tool Call:", json.dumps(call, ensure_ascii=False))
    result = build_registry().execute(name, arguments)
    print("Observation:", json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
