from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"

def add_frontend(app):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    author: str = Field(min_length=1, max_length=80)
    year: int = Field(ge=1400, le=2100)

def create_app() -> FastAPI:
    app = FastAPI(title="Bookstore")
    app.state.books = []
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/books", status_code=201)
    def add_book(payload: BookIn):
        book = {"id": app.state.next_id, **payload.model_dump()}
        app.state.next_id += 1
        app.state.books.append(book)
        return book

    @app.get("/books")
    def search(q: str = "", page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=50)):
        qn = q.lower().strip()
        matches = [b for b in app.state.books if qn in b["title"].lower() or qn in b["author"].lower()]
        start = (page - 1) * size
        return {"total": len(matches), "page": page, "items": matches[start:start + size]}

    add_frontend(app)
    return app

app = create_app()
