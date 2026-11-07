from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"

def add_frontend(app):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

from fastapi import FastAPI
from pydantic import BaseModel, Field

class RecipeIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    ingredients: str = Field(min_length=1, max_length=2000)
    steps: str = Field(min_length=1, max_length=4000)

def create_app() -> FastAPI:
    app = FastAPI(title="Recipe Book")
    app.state.recipes = {}
    app.state.next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/recipes", status_code=201)
    def create_recipe(payload: RecipeIn):
        recipe = {"id": app.state.next_id, **payload.model_dump()}
        app.state.next_id += 1
        app.state.recipes[recipe["id"]] = recipe
        return recipe

    @app.get("/recipes")
    def list_recipes():
        return list(app.state.recipes.values())

    add_frontend(app)
    return app

app = create_app()
