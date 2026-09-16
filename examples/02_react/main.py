"""确定性 Mini ReAct：Action → Observation → 下一 Action。"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DOCS = Path(__file__).resolve().parents[2] / "docs"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Action:
    name: str
    arguments: dict[str, Any]


class PlanModel:
    def __init__(self, repeat: bool = False) -> None:
        self.repeat = repeat

    def decide(self, observations: list[dict[str, Any]]) -> Action | str:
        if self.repeat:
            return Action("search_docs", {"query": "Agent Loop"})
        if not observations:
            return Action("search_docs", {"query": "Agent Loop"})
        if len(observations) == 1:
            return Action("count_results", {"items": observations[0]["value"]})
        return f"找到 {observations[1]['value']} 份与 Agent Loop 相关的课程文档。"


def execute(action: Action) -> dict[str, Any]:
    if action.name == "search_docs":
        query = action.arguments["query"].lower()
        names = [p.name for p in DOCS.glob("*.md") if query in p.read_text(encoding="utf-8").lower()]
        return {"ok": True, "value": names}
    if action.name == "count_results":
        return {"ok": True, "value": len(action.arguments["items"])}
    return {"ok": False, "error": "unknown_tool"}


def run(model: PlanModel, max_steps: int) -> str:
    observations: list[dict[str, Any]] = []
    seen: set[str] = set()
    for step in range(1, max_steps + 1):
        decision = model.decide(observations)
        if isinstance(decision, str):
            print(f"[step {step}] final: {decision}")
            return decision
        fingerprint = json.dumps({"name": decision.name, "arguments": decision.arguments}, sort_keys=True, ensure_ascii=False)
        if fingerprint in seen:
            raise RuntimeError(f"检测到重复 Action：{fingerprint}")
        seen.add(fingerprint)
        print(f"[step {step}] action: {fingerprint}")
        observation = execute(decision)
        observations.append(observation)
        print(f"[step {step}] observation: {json.dumps(observation, ensure_ascii=False)}")
    raise RuntimeError(f"达到最大步数 {max_steps}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", action="store_true")
    parser.add_argument("--max-steps", type=int, default=4)
    args = parser.parse_args()
    try:
        run(PlanModel(args.repeat), args.max_steps)
    except RuntimeError as exc:
        print("STOP:", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
