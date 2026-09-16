"""Project 10：离线 AI Research Agent 垂直切片。"""

from __future__ import annotations

import json
import re
import sys
import uuid
from pathlib import Path
from typing import Any


DOCS = Path(__file__).resolve().parents[2] / "docs"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def terms(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z][\w-]+|[\u4e00-\u9fff]", text.lower()))


def search(query: str, limit: int = 4) -> list[dict[str, Any]]:
    q = terms(query); hits = []
    for path in DOCS.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        score = len(q & terms(text)) / max(1, len(q))
        if score: hits.append({"source": path.name, "score": score, "excerpt": text[:1000]})
    return sorted(hits, key=lambda x: x["score"], reverse=True)[:limit]


def research(question: str) -> dict[str, Any]:
    state: dict[str, Any] = {"run_id": str(uuid.uuid4()), "question": question, "status": "running", "trace": []}
    state["plan"] = ["检索课程资料", "检查证据", "生成带引用报告"]
    state["trace"].append({"node": "plan", "plan": state["plan"]})
    state["evidence"] = search(question)
    state["trace"].append({"node": "search", "sources": [e["source"] for e in state["evidence"]]})
    sufficient = len(state["evidence"]) >= 2 and state["evidence"][0]["score"] >= 0.2
    state["trace"].append({"node": "evidence_gate", "sufficient": sufficient})
    if not sufficient:
        state.update({"status": "insufficient_evidence", "report": None}); return state
    sources = [item["source"] for item in state["evidence"][:3]]
    report = {
        "title": question,
        "summary": "优先从单 Agent 或显式 Workflow 开始。只有上下文隔离、独立权限、并行专业能力或真正独立审查带来可测收益时，才使用 Multi-Agent。",
        "citations": sources,
        "limitations": ["离线资料快照", "未进行互联网搜索"],
    }
    state.update({"status": "completed", "report": report})
    state["trace"].append({"node": "report", "citations": sources})
    return state


if __name__ == "__main__":
    result = research(" ".join(sys.argv[1:]) or "什么时候应该使用 Multi-Agent？")
    print(json.dumps(result, ensure_ascii=False, indent=2))
