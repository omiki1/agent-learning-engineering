"""毕业项目可选 Web API。"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app import research


app = FastAPI(title="Offline Research Agent")


class ResearchRequest(BaseModel):
    question: str


@app.post("/research")
def create_research(request: ResearchRequest) -> dict:
    return research(request.question)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(__file__.replace("service.py", "web/index.html"))

