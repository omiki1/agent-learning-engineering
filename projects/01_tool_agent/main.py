"""Project 01：离线 Tool Agent 参考实现。"""

from __future__ import annotations

import ast
import json
import operator
import re
import sys
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def calculator(expression: str) -> int | float:
    def walk(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression): return walk(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS: return OPS[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError("不支持的表达式")
    return walk(ast.parse(expression, mode="eval"))


def weather(city: str) -> dict[str, Any]:
    values = {"tokyo": 31, "beijing": 28}
    if city.lower() not in values: raise ValueError("离线数据无此城市")
    return {"city": city, "temperature_c": values[city.lower()], "source": "sample"}


def search(query: str) -> list[str]:
    return [p.name for p in DOCS.glob("*.md") if query.lower() in p.read_text(encoding="utf-8").lower()][:5]


def read_file(relative_path: str) -> str:
    target = (DOCS / relative_path).resolve()
    if DOCS.resolve() not in target.parents or target.suffix != ".md": raise PermissionError("路径越界")
    return target.read_text(encoding="utf-8")[:800]


TOOLS: dict[str, Callable[..., Any]] = {"calculator": calculator, "weather": weather, "search": search, "read_file": read_file}


def route(question: str) -> tuple[str, dict[str, Any]]:
    expression = re.search(r"[\d(][\d\s+\-*/().]+", question)
    if expression: return "calculator", {"expression": expression.group().strip()}
    lower = question.lower()
    if "天气" in question or "weather" in lower:
        city = "Tokyo" if "tokyo" in lower else "Beijing"
        return "weather", {"city": city}
    if "读取" in question or "read" in lower:
        name = next((part for part in question.split() if part.endswith(".md")), "00_agent_overview.md")
        return "read_file", {"relative_path": name}
    query = question.replace("搜索", "").replace("search", "").strip() or "Agent"
    return "search", {"query": query}


def run(question: str) -> dict[str, Any]:
    name, arguments = route(question)
    print("ACTION", json.dumps({"name": name, "arguments": arguments}, ensure_ascii=False))
    try:
        value = TOOLS[name](**arguments)
        result = {"ok": True, "value": value}
    except Exception as exc:
        result = {"ok": False, "error": type(exc).__name__, "message": str(exc)}
    print("OBSERVATION", json.dumps(result, ensure_ascii=False))
    return result


if __name__ == "__main__":
    run(" ".join(sys.argv[1:]) or "请计算 (9 + 3) * 2")
