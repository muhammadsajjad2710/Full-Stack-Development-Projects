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

class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)

def create_app() -> FastAPI:
    app = FastAPI(title="Todo App")
    app.state.tasks = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/tasks", status_code=201)
    def add(payload: TaskIn):
        task = {"id": app.state.next_id, "title": payload.title, "done": False}
        app.state.next_id += 1
        app.state.tasks[task["id"]] = task
        return task

    @app.get("/tasks")
    def listing():
        return list(app.state.tasks.values())

    @app.post("/tasks/{task_id}/toggle")
    def toggle(task_id: int):
        task = app.state.tasks.get(task_id)
        if task is None:
            raise HTTPException(404, "Task not found")
        task["done"] = not task["done"]
        return task

    add_frontend(app)
    return app

app = create_app()
