"""可选 FastAPI/SSE 适配层。"""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from core import RunService


app = FastAPI(title="Agent Course Service")
service = RunService()


class RunRequest(BaseModel):
    question: str


@app.post("/runs")
async def create_run(request: RunRequest) -> dict:
    run = service.create(request.question)
    asyncio.create_task(service.execute(run.id))
    return {"run_id": run.id, "status": run.status}


@app.get("/runs/{run_id}")
async def get_run(run_id: str) -> dict:
    if run_id not in service.runs: raise HTTPException(404, "run not found")
    return asdict(service.runs[run_id])


@app.get("/runs/{run_id}/events")
async def events(run_id: str) -> StreamingResponse:
    if run_id not in service.runs: raise HTTPException(404, "run not found")
    async def stream():
        sent = 0
        while True:
            run = service.runs[run_id]
            while sent < len(run.events):
                event = run.events[sent]; sent += 1
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
            if run.status in {"completed", "failed", "cancelled"}: break
            await asyncio.sleep(0.1)
    return StreamingResponse(stream(), media_type="text/event-stream")

