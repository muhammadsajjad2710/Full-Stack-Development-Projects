from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"

def add_frontend(app):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    body: str = Field(min_length=1, max_length=2000)

def create_app() -> FastAPI:
    app = FastAPI(title="Notes App")
    app.state.notes = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/notes", status_code=201)
    def create_note(payload: NoteIn):
        note = {"id": app.state.next_id, **payload.model_dump()}
        app.state.next_id += 1
        app.state.notes[note["id"]] = note
        return note

    @app.get("/notes")
    def list_notes():
        return list(app.state.notes.values())

    @app.delete("/notes/{note_id}", status_code=204)
    def delete_note(note_id: int) -> Response:
        if note_id not in app.state.notes:
            raise HTTPException(404, "Note not found")
        del app.state.notes[note_id]
        return Response(status_code=204)

    add_frontend(app)
    return app

app = create_app()
