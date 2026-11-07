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

class PostIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    body: str = Field(min_length=1, max_length=5000)

class CommentIn(BaseModel):
    author: str = Field(min_length=1, max_length=40)
    body: str = Field(min_length=1, max_length=500)

def create_app() -> FastAPI:
    app = FastAPI(title="Blog App")
    app.state.posts = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/posts", status_code=201)
    def create_post(payload: PostIn):
        post = {"id": app.state.next_id, **payload.model_dump(), "comments": []}
        app.state.next_id += 1
        app.state.posts[post["id"]] = post
        return post

    @app.get("/posts")
    def list_posts():
        return list(app.state.posts.values())

    @app.post("/posts/{post_id}/comments", status_code=201)
    def add_comment(post_id: int, payload: CommentIn):
        if post_id not in app.state.posts:
            raise HTTPException(404, "Post not found")
        comment = {"id": len(app.state.posts[post_id]["comments"]) + 1, **payload.model_dump()}
        app.state.posts[post_id]["comments"].append(comment)
        return comment

    add_frontend(app)
    return app

app = create_app()
