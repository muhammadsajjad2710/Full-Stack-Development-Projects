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
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

def encode(number: int) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if number == 0:
        return alphabet[0]
    chars = []
    while number:
        number, rem = divmod(number, len(alphabet))
        chars.append(alphabet[rem])
    return "".join(reversed(chars))

class UrlIn(BaseModel):
    url: HttpUrl

def create_app() -> FastAPI:
    app = FastAPI(title="URL Shortener")
    app.state.urls = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/links")
    def links():
        return [{"code": code, "url": url} for code, url in app.state.urls.items()]

    @app.post("/shorten")
    def shorten(payload: UrlIn):
        code = encode(app.state.next_id)
        app.state.next_id += 1
        app.state.urls[code] = str(payload.url)
        return {"code": code, "url": str(payload.url)}

    add_frontend(app)

    @app.get("/{code}")
    def resolve(code: str):
        if code in {"health", "links", "shorten", "static", "docs", "openapi.json"} or code not in app.state.urls:
            raise HTTPException(404, "Unknown code")
        return RedirectResponse(app.state.urls[code], status_code=307)

    return app

app = create_app()
