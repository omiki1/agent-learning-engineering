"""Project 02：显式 Action/Observation 的三步 ReAct Runtime。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DOCS = Path(__file__).resolve().parents[2] / "docs"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def search(query: str) -> list[str]:
    terms = query.lower().split()
    scored = []
    for path in DOCS.glob("*.md"):
        text = path.read_text(encoding="utf-8").lower()
        scored.append((sum(text.count(term) for term in terms), path.name))
    return [name for score, name in sorted(scored, reverse=True) if score > 0][:3]


def read(name: str) -> str:
    target = (DOCS / name).resolve()
    if DOCS.resolve() not in target.parents: raise PermissionError("路径越界")
    return target.read_text(encoding="utf-8")[:1500]


def decide(observations: list[dict]) -> tuple[str, dict] | str:
    if not observations: return "search", {"query": "Memory History State Context"}
    if len(observations) == 1:
        names = observations[0]["value"]
        return "read", {"name": names[0] if names else "04_memory.md"}
    return "History 是原始消息记录；Context 是本次模型实际看到的输入；State 是任务运行数据；Memory 是未来可选择性取回的信息。"


def run(max_steps: int = 4) -> str:
    observations: list[dict] = []
    seen: set[str] = set()
    tools = {"search": search, "read": read}
    for step in range(1, max_steps + 1):
        action = decide(observations)
        if isinstance(action, str):
            print(f"[{step}] FINAL {action}")
            return action
        name, arguments = action
        fingerprint = json.dumps(action, sort_keys=True, ensure_ascii=False)
        if fingerprint in seen: raise RuntimeError("repeated_action")
        seen.add(fingerprint)
        print(f"[{step}] ACTION {fingerprint}")
        try: result = {"ok": True, "value": tools[name](**arguments)}
        except Exception as exc: result = {"ok": False, "error": str(exc)}
        observations.append(result)
        print(f"[{step}] OBSERVATION {json.dumps(result, ensure_ascii=False)[:500]}")
    raise RuntimeError("step_limit")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-steps", type=int, default=4)
    args = parser.parse_args()
    try: run(args.max_steps)
    except RuntimeError as exc:
        print("STOP", exc)
        raise SystemExit(1)
