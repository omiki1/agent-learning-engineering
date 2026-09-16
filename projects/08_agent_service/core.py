"""Project 08：与 Web 框架解耦的 Agent Service Core。"""

from __future__ import annotations

import asyncio
import json
import sys
import uuid
from dataclasses import asdict, dataclass, field

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass
class Run:
    id: str
    question: str
    status: str = "queued"
    events: list[dict] = field(default_factory=list)
    answer: str | None = None


class RunService:
    def __init__(self) -> None:
        self.runs: dict[str, Run] = {}

    def create(self, question: str) -> Run:
        run = Run(str(uuid.uuid4()), question)
        self.runs[run.id] = run
        return run

    async def execute(self, run_id: str) -> Run:
        run = self.runs[run_id]; run.status = "running"
        run.events.append({"type": "started", "run_id": run.id})
        await asyncio.sleep(0)
        run.events.append({"type": "tool", "name": "course_search", "status": "completed"})
        run.answer = "固定步骤优先 Workflow；动态多步决策才考虑 Agent。"
        run.status = "completed"
        run.events.append({"type": "final", "answer": run.answer})
        return run


async def demo() -> None:
    service = RunService(); run = service.create("什么时候使用 Agent？")
    await service.execute(run.id)
    print(json.dumps(asdict(run), ensure_ascii=False, indent=2))


if __name__ == "__main__": asyncio.run(demo())
