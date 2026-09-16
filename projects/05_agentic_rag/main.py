"""Project 05：带有限 Query Rewrite 和 Evidence Gate 的离线 RAG。"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DOCS = Path(__file__).resolve().parents[2] / "docs"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str


def tokenize(text: str) -> set[str]:
    latin = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text.lower())
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    return set(latin + cjk)


def load_chunks() -> list[Chunk]:
    chunks = []
    for path in DOCS.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for index, section in enumerate(text.split("\n## ")):
            if section.strip(): chunks.append(Chunk(f"{path.name}#{index}", section[:1800]))
    return chunks


def retrieve(query: str, chunks: list[Chunk], k: int = 4) -> list[dict]:
    q = tokenize(query)
    ranked = []
    for chunk in chunks:
        overlap = len(q & tokenize(chunk.text))
        if overlap: ranked.append({"id": chunk.id, "score": overlap / max(1, len(q)), "text": chunk.text})
    return sorted(ranked, key=lambda x: x["score"], reverse=True)[:k]


def rewrite(query: str) -> str:
    return query + " Agent Workflow 动态决策 状态机 工具调用"


def run(query: str) -> dict:
    chunks = load_chunks(); attempts = []
    current = query
    for attempt in range(2):
        candidates = retrieve(current, chunks, k=12)
        hits = []
        seen_sources = set()
        for candidate in candidates:
            source = candidate["id"].split("#", 1)[0]
            if source not in seen_sources:
                seen_sources.add(source); hits.append(candidate)
            if len(hits) == 4: break
        attempts.append({"query": current, "hits": [{"id": h["id"], "score": h["score"]} for h in hits]})
        if len(hits) >= 2 and hits[0]["score"] >= 0.25:
            answer = "固定且可预测的步骤优先 Workflow；只有下一步依赖运行中的 Observation 并需要动态选择时，才引入 Agent。"
            return {"answer": answer, "citations": [h["id"] for h in hits[:2]], "attempts": attempts}
        current = rewrite(query)
    return {"answer": None, "abstain": "证据不足", "attempts": attempts}


if __name__ == "__main__":
    result = run(" ".join(sys.argv[1:]) or "Agent 和 Workflow 有什么区别")
    print(json.dumps(result, ensure_ascii=False, indent=2))
