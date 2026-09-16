"""Project 07：Multi-Agent 通信与成本对照 Harness。"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass
class Artifact:
    author: str
    content: str
    evidence: list[str]


class Researcher:
    def run(self, task: str) -> Artifact:
        return Artifact("researcher", "Agent 适合动态多步决策；Workflow 适合固定流程。", ["docs/00_agent_overview.md", "docs/05_workflow.md"])


class Developer:
    def run(self, task: str, research: Artifact) -> Artifact:
        content = "建议架构：确定性 Workflow 包围有限 Agent 节点，并设置 max_steps、Trace 和 Evidence Gate。"
        return Artifact("developer", content, research.evidence)


class Reviewer:
    def run(self, draft: Artifact) -> Artifact:
        finding = "通过：包含边界、停止条件和可观察性。" if "max_steps" in draft.content else "失败：缺少停止条件。"
        return Artifact("reviewer", finding, draft.evidence)


def multi_agent(task: str) -> dict:
    messages = [task]
    research = Researcher().run(task); messages.append(json.dumps(research.__dict__, ensure_ascii=False))
    draft = Developer().run(task, research); messages.append(json.dumps(draft.__dict__, ensure_ascii=False))
    review = Reviewer().run(draft); messages.append(json.dumps(review.__dict__, ensure_ascii=False))
    return {"answer": draft.content, "review": review.content, "steps": 3, "communication_chars": sum(map(len, messages))}


def single_agent(task: str) -> dict:
    answer = "固定流程用 Workflow；动态决策用受控 Agent，并设置 max_steps、Trace 和证据验证。"
    return {"answer": answer, "review": None, "steps": 1, "communication_chars": len(task) + len(answer)}


if __name__ == "__main__":
    task = "设计一个调研 Agent，并说明与 Workflow 的边界。"
    print(json.dumps({"single": single_agent(task), "multi": multi_agent(task)}, ensure_ascii=False, indent=2))
