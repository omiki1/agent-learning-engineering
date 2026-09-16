"""30 条样本的确定性 Agent Eval Harness。"""

from __future__ import annotations

import ast
import json
import operator
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


DATASET = Path(__file__).with_name("dataset.jsonl")
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass
class RunResult:
    answer: str
    tool: str | None
    steps: int
    tokens: int
    latency_ms: float


def calc(text: str) -> int | float:
    expression = re.search(r"[\d(][\d\s+\-*/().]+", text).group().strip()
    def walk(node):
        if isinstance(node, ast.Expression): return walk(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS: return OPS[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError("unsupported")
    value = walk(ast.parse(expression, mode="eval"))
    return int(value) if isinstance(value, float) and value.is_integer() else value


def candidate_agent(text: str) -> RunResult:
    start = time.perf_counter(); lower = text.lower(); tool = None; steps = 1
    if any(word in text for word in ["删除", "DROP", "汇款", "未经批准"]): answer = "拒绝：该动作需要明确权限和人工批准。"
    elif text.startswith("读取"):
        tool = "read_file"; answer = f"已读取 {text.removeprefix('读取').strip()}"; steps = 2
    elif "计算" in text and re.search(r"[\d(][\d\s+\-*/().]+", text): tool = "calculator"; answer = f"结果是 {calc(text)}"; steps = 2
    elif "天气" in text or "weather" in lower:
        tool = "weather"; city = "Tokyo" if "tokyo" in lower else "Beijing"; answer = f"{city} 离线天气样例"; steps = 2
    elif text.startswith("搜索"):
        tool = "search"; answer = f"已搜索 {text.removeprefix('搜索').strip()}"; steps = 2
    else: answer = "你好" if text == "你好" else text.replace("解释什么是 ", "") + " 是本课程的核心概念。"
    latency = (time.perf_counter() - start) * 1000
    return RunResult(answer, tool, steps, max(1, (len(text) + len(answer)) // 2), latency)


def main() -> None:
    cases = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line]
    rows = []; failures = Counter()
    for case in cases:
        run = candidate_agent(case["input"])
        tool_ok = run.tool == case["expected_tool"]
        answer_ok = case["expected_contains"] in run.answer
        steps_ok = run.steps <= case["max_steps"]
        success = tool_ok and answer_ok and steps_ok
        reason = None if success else ("tool" if not tool_ok else "answer" if not answer_ok else "steps")
        if reason: failures[reason] += 1
        rows.append({"success": success, "tool_ok": tool_ok, "steps": run.steps, "tokens": run.tokens, "latency_ms": run.latency_ms, "reason": reason})
    n = len(rows); total_tokens = sum(row["tokens"] for row in rows)
    report = {
        "cases": n,
        "task_success_rate": sum(row["success"] for row in rows) / n,
        "tool_selection_accuracy": sum(row["tool_ok"] for row in rows) / n,
        "average_steps": sum(row["steps"] for row in rows) / n,
        "average_tokens_estimate": total_tokens / n,
        "average_cost_estimate_usd": total_tokens * 0.000001 / n,
        "average_latency_ms": sum(row["latency_ms"] for row in rows) / n,
        "failure_reasons": dict(failures),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
