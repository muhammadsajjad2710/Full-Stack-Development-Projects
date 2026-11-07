from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"

def add_frontend(app):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class IssueIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = ""

def create_app() -> FastAPI:
    app = FastAPI(title="Issue Tracker")
    app.state.issues = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/issues", status_code=201)
    def create_issue(payload: IssueIn):
        issue = {"id": app.state.next_id, "title": payload.title, "description": payload.description, "open": True}
        app.state.next_id += 1
        app.state.issues[issue["id"]] = issue
        return issue

    @app.get("/issues")
    def list_issues():
        return list(app.state.issues.values())

    @app.post("/issues/{issue_id}/close")
    def close_issue(issue_id: int):
        issue = app.state.issues.get(issue_id)
        if issue is None:
            raise HTTPException(404, "Issue not found")
        issue["open"] = False
        return issue

    add_frontend(app)
    return app

app = create_app()
