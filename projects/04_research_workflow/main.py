"""Project 04：框架无关的研究 Workflow。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


DOCS = Path(__file__).resolve().parents[2] / "docs"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def analyze(state: dict[str, Any]) -> dict[str, Any]: return {"intent": "agent_architecture", "keywords": ["Agent", "Workflow"]}
def plan(state: dict[str, Any]) -> dict[str, Any]: return {"plan": ["检索课程", "读取证据", "验证", "回答"]}
def search(state: dict[str, Any]) -> dict[str, Any]:
    hits = []
    for path in DOCS.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        score = sum(text.lower().count(k.lower()) for k in state["keywords"])
        if score: hits.append({"file": path.name, "score": score})
    return {"hits": sorted(hits, key=lambda x: x["score"], reverse=True)[:3], "search_round": state.get("search_round", 0) + 1}
def read(state: dict[str, Any]) -> dict[str, Any]:
    evidence = [{"file": hit["file"], "text": (DOCS / hit["file"]).read_text(encoding="utf-8")[:600]} for hit in state["hits"]]
    return {"evidence": evidence}
def verify(state: dict[str, Any]) -> dict[str, Any]: return {"sufficient": len(state.get("evidence", [])) >= 2}
def answer(state: dict[str, Any]) -> dict[str, Any]:
    return {"answer": "步骤固定时优先 Workflow；只有下一步必须依据运行中观察动态决定时才使用 Agent。"}


NODES = {"analyze": analyze, "plan": plan, "search": search, "read": read, "verify": verify, "answer": answer}


def route(node: str, state: dict[str, Any]) -> str:
    fixed = {"analyze": "plan", "plan": "search", "search": "read", "read": "verify", "answer": "END"}
    if node == "verify": return "answer" if state["sufficient"] else ("search" if state["search_round"] < 2 else "answer")
    return fixed[node]


def run(question: str) -> dict[str, Any]:
    state: dict[str, Any] = {"question": question}
    node = "analyze"
    while node != "END":
        update = NODES[node](state); state.update(update)
        print(json.dumps({"node": node, "update": update}, ensure_ascii=False)[:800])
        node = route(node, state)
    return state


if __name__ == "__main__":
    result = run(" ".join(sys.argv[1:]) or "什么时候应该用 Agent？")
    print("FINAL", result["answer"])
